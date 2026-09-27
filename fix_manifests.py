#!/usr/bin/env python3
"""Пересборка manifest.plist по РЕАЛЬНЫМ данным из самих IPA.

Проблемы, которые это чинит:
  * create_manifests.py писал заглушки: bundle-identifier = com.example.<slug>,
    bundle-version = 1.0.0, title = имя из каталога. iOS отвергает пакет, если
    bundle-identifier в манифесте не совпадает с реальным.
  * URL ассета тоже был угадан ({slug}.ipa), хотя в релизах лежат другие имена
    (например online-com-inv-gen.ipa), и часть slug'ов вообще не совпадает с тегами
    (кириллица vs транслит).

Источник истины — app-data.js (именно эти приложения показывает сайт), а тег и
имя ассета берутся из уже готового downloadUrl. Метаданные приложения читаются
из самого IPA через HTTP Range, без скачивания сотен мегабайт.
"""
import json
import sys
import plistlib
import re
import struct
import subprocess
import urllib.request
import zlib
from pathlib import Path

SITE = Path("/root/projects/ios-ota-apps-site")
APPS = SITE / "apps"
REPO = "soundtrackminus-hash/ios-ota-apps-site"
UA = {"User-Agent": "fix-manifests/2.0"}

MANIFEST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
\t<key>items</key>
\t<array>
\t\t<dict>
\t\t\t<key>assets</key>
\t\t\t<array>
\t\t\t\t<dict>
\t\t\t\t\t<key>kind</key>
\t\t\t\t\t<string>software-package</string>
\t\t\t\t\t<key>url</key>
\t\t\t\t\t<string>{url}</string>
\t\t\t\t</dict>
\t\t\t</array>
\t\t\t<key>metadata</key>
\t\t\t<dict>
\t\t\t\t<key>bundle-identifier</key>
\t\t\t\t<string>{bundle_id}</string>
\t\t\t\t<key>bundle-version</key>
\t\t\t\t<string>{build}</string>
\t\t\t\t<key>kind</key>
\t\t\t\t<string>software</string>
\t\t\t\t<key>title</key>
\t\t\t\t<string>{title}</string>
\t\t\t</dict>
\t\t</dict>
\t</array>
</dict>
</plist>
"""


def get_range(url, a, b):
    req = urllib.request.Request(url, headers={**UA, "Range": "bytes=%d-%d" % (a, b)})
    with urllib.request.urlopen(req, timeout=180) as f:
        return f.read()


def zip64_fix(extra, csize, usize, off):
    """Если csize/usize/off = 0xFFFFFFFF, реальные значения лежат в extra field (id 1)."""
    if 0xFFFFFFFF not in (csize, usize, off):
        return csize, usize, off
    p = 0
    while p + 4 <= len(extra):
        hid, hsz = struct.unpack("<HH", extra[p:p + 4])
        body = extra[p + 4:p + 4 + hsz]
        if hid == 1:
            vals = list(struct.unpack("<%dQ" % (len(body) // 8), body[:len(body) // 8 * 8]))
            k = 0
            if usize == 0xFFFFFFFF and k < len(vals):
                usize = vals[k]; k += 1
            if csize == 0xFFFFFFFF and k < len(vals):
                csize = vals[k]; k += 1
            if off == 0xFFFFFFFF and k < len(vals):
                off = vals[k]; k += 1
            break
        p += 4 + hsz
    return csize, usize, off


def zip_entries(url, size):
    """-> {имя: (method, csize, usize, offset)} из central directory."""
    tail = b""
    for span in (65536, 1048576):
        tail = get_range(url, max(0, size - span), size - 1)
        i = tail.rfind(b"PK\x05\x06")
        if i >= 0:
            break
    else:
        raise ValueError("EOCD не найден даже в последних 1 МБ")
    _, cdsize, cdoff = struct.unpack("<HII", tail[i + 10:i + 20])
    if cdoff == 0xFFFFFFFF or cdsize == 0xFFFFFFFF:
        raise ValueError("ZIP64 в EOCD, не поддержан")
    cd = get_range(url, cdoff, cdoff + cdsize - 1)
    if len(cd) < cdsize:
        raise ValueError("central directory прочитан не полностью (%d из %d)" % (len(cd), cdsize))
    out, p = {}, 0
    while p + 46 <= len(cd) and cd[p:p + 4] == b"PK\x01\x02":
        method = struct.unpack("<H", cd[p + 10:p + 12])[0]
        csize, usize = struct.unpack("<II", cd[p + 20:p + 28])
        nlen, elen, clen = struct.unpack("<HHH", cd[p + 28:p + 34])
        off = struct.unpack("<I", cd[p + 42:p + 46])[0]
        extra = cd[p + 46 + nlen: p + 46 + nlen + elen]
        csize, usize, off = zip64_fix(extra, csize, usize, off)
        name = cd[p + 46:p + 46 + nlen].decode("utf-8", "replace")
        out[name] = (method, csize, usize, off)
        p += 46 + nlen + elen + clen
    return out


def read_entry(url, method, csize, off):
    """Два шага: сначала local header (30 байт), затем точный диапазон данных.
    Одним запросом 30+csize нельзя — nlen+elen бывает больше 30."""
    head = get_range(url, off, off + 29)
    if head[:4] != b"PK\x03\x04":
        raise ValueError("нет local file header по offset %d" % off)
    nlen, elen = struct.unpack("<HH", head[26:30])
    start = off + 30 + nlen + elen
    data = get_range(url, start, start + csize - 1)
    if len(data) != csize:
        raise ValueError("прочитано %d из %d байт данных" % (len(data), csize))
    if method == 8:
        data = zlib.decompress(data, -15)
    elif method != 0:
        raise ValueError("неподдерживаемый метод сжатия %d" % method)
    return data


def probe(url, size):
    """Реальные метаданные приложения + наличие подписи."""
    ents = zip_entries(url, size)
    info = next((n for n in ents if re.search(r"^Payload/[^/]+\.app/Info\.plist$", n)), None)
    if not info:
        raise ValueError("Info.plist не найден")
    method, csize, usize, off = ents[info]  # важно: off — 4-й элемент, не usize
    pl = plistlib.loads(read_entry(url, method, csize, off))
    prov = next((n for n in ents if n.endswith("embedded.mobileprovision")), None)
    title = pl.get("CFBundleDisplayName") or pl.get("CFBundleName") or ""
    if isinstance(title, str) and len(title.encode("utf-8")) > 255:
        title = str(pl.get("CFBundleName") or "")
    return {
        "bundleId": pl.get("CFBundleIdentifier", ""),
        "build": str(pl.get("CFBundleVersion", "")),
        "short": str(pl.get("CFBundleShortVersionString", "")),
        "title": title,
        "inner": pl.get("CFBundleName", ""),
        "minOS": str(pl.get("MinimumOSVersion", "")),
        "signed": prov is not None,
    }


def releases():
    out = subprocess.run(
        ["gh", "api", "repos/%s/releases?per_page=100" % REPO, "--paginate",
         "-q", '.[] | {tag: .tag_name, assets: [.assets[] | {name: .name, size: .size, url: .browser_download_url}]}'],
        capture_output=True, text=True, check=True).stdout
    raw, dec, depth = [], json.JSONDecoder(), 0
    while depth < len(out):
        try:
            obj, end = dec.raw_decode(out, depth)
        except ValueError:
            break
        raw.append(obj)
        depth = end
        while depth < len(out) and out[depth] in " \n\r\t":
            depth += 1
    return {r["tag"]: r["assets"] for r in raw}


def catalog(path):
    """Приложения, которые реально показывает сайт (app-data.js)."""
    txt = Path(path).read_text(encoding="utf-8")
    apps = []
    for block in re.findall(r"\{[^{}]*\}", txt):
        if '"slug"' not in block:
            continue
        d = {}
        for k in ("name", "slug", "downloadUrl", "manifestUrl", "version"):
            m = re.search(r'"%s"\s*:\s*"([^"]*)"' % k, block)
            if m:
                d[k] = m.group(1)
        if "slug" in d:
            apps.append(d)
    return apps


def pick_asset(tags, slug, dl_url):
    """Возвращает (asset, tag) — сначала по downloadUrl, потом подбором."""
    if dl_url:
        m = re.search(r"/releases/download/([^/]+)/([^/?#]+)", dl_url)
        if m:
            tag, asset_name = m.group(1), m.group(2)
            for a in tags.get(tag, []):
                if a["name"] == asset_name:
                    return a, tag
            pool = [a for a in tags.get(tag, []) if a["name"].endswith(".ipa")]
            if pool:
                return pool[0], tag
    # запасные варианты: тег по слагу, затем по префиксу
    for cand in ([("%s-1.0.0" % slug)] +
                 [t for t in tags if t.startswith(slug)] +
                 sorted(tags)):
        pool = [a for a in tags.get(cand, []) if a["name"].endswith(".ipa")]
        if pool:
            best = next((a for a in pool if a["name"] == "%s.ipa" % slug), max(pool, key=lambda a: a["size"]))
            return best, cand
    return None, None


def main():
    cat_path = sys.argv[1] if len(sys.argv) > 1 else SITE / "app-data.js"
    tags = releases()
    apps = catalog(cat_path)
    print("каталог: %s | релизов: %d | приложений: %d | каталогов в apps/: %d\n"
          % (cat_path, len(tags), len(apps), sum(1 for p in APPS.iterdir() if p.is_dir())))
    report, ok, signed, failed = [], 0, 0, 0
    for n, app in enumerate(apps, 1):
        slug = app["slug"]
        asset, tag = pick_asset(tags, slug, app.get("downloadUrl", ""))
        if not asset:
            failed += 1
            report.append({"slug": slug, "name": app.get("name"), "status": "нет .ipa в релизах"})
            print("[%2d/%d] %-42s НЕТ .ipa" % (n, len(apps), slug))
            continue
        try:
            info = probe(asset["url"], asset["size"])
        except Exception as e:
            failed += 1
            report.append({"slug": slug, "name": app.get("name"), "status": "ошибка: %s" % e,
                           "asset": asset["name"]})
            print("[%2d/%d] %-42s ОШИБКА %s" % (n, len(apps), slug, e))
            continue
        d = APPS / slug
        d.mkdir(parents=True, exist_ok=True)
        (d / "manifest.plist").write_text(MANIFEST.format(
            url=asset["url"], bundle_id=info["bundleId"], build=info["build"],
            title=info["title"] or info["inner"]), encoding="utf-8")
        ok += 1
        signed += bool(info["signed"])
        report.append({
            "slug": slug, "catName": app.get("name"), "title": info["title"] or info["inner"],
            "inner": info["inner"], "bundleId": info["bundleId"],
            "version": "%s (%s)" % (info["short"], info["build"]), "minOS": info["minOS"],
            "signed": info["signed"], "tag": tag, "asset": asset["name"], "size": asset["size"],
            "renamed": bool(info["title"] and info["title"] != app.get("name")),
        })
        print("[%2d/%d] %-42s %-11s %-28s %-24s %s (%s)" % (
            n, len(apps), slug, "подписан" if info["signed"] else "БЕЗ ПОДПИСИ",
            info["title"] or info["inner"], info["bundleId"], info["short"], info["build"]))

    (SITE / "manifest_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\nИТОГО: манифестов перезаписано %d | с подписью %d | без подписи %d | ошибок/нет IPA %d"
          % (ok, signed, ok - signed, failed))
    print("отчёт: manifest_audit.json")


if __name__ == "__main__":
    main()
