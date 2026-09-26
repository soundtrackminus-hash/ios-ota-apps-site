#!/usr/bin/env python3
"""Генерация полного списка приложений для app-data.js"""
import json
import os
import zipfile
from pathlib import Path

SITE_DIR = '/root/projects/ios-ota-apps-site'
CACHE_DIR = '/root/.hermes/cache/scratch/ios-apps'
ICON_DIR = f'{SITE_DIR}/icons'

# Словарь для маппинга имен файлов на slug
file_to_slug = {
    "ак-барс-онлайн.ipa": "ак-барс-онлайн",
    "афина-бюджет-псб-банк.ipa": "афина-бюджет-псб-банк",
    "без-наличных-mtc-pay.ipa": "без-наличных-mtc-pay",
    "делим-вместе-альфа-банк.ipa": "делим-вместе-альфа-банк",
    "spotluma.ipa": "spotluma",
    "teboil.ipa": "teboil",
    "учимся-словам.ipa": "учимся-словам",
    "atoy.ipa": "atoy",
    "anero-ваш-онлайн-помощник-авито.ipa": "анеро-ваш-онлайн-помощник-авито",
    "auction-au-ru-avito.ipa": "auction-au-ru-avito",
    "fuellntime-тбанк-инвестиции.ipa": "fuellntime-тбанк-инвестиции",
    "happ-proxy-utility-plus.ipa": "happ-proxy-utility-plus",
    "imanager-by-ins-invest-ингосстрах.ipa": "imanager-by-ins-invest-ингосстрах",
    "scb-notes-совкомбанк.ipa": "scb-notes-совкомбанк",
    "speakaboo-сберкидс.ipa": "speakaboo-сберкидс",
    "mobio-сбермобайл.ipa": "mobio-сбермобайл",
    "yandex-sim.ipa": "yandex-sim",
}

apps_data = []

for ipa_file in sorted(Path(CACHE_DIR).glob("*.ipa")):
    slug = file_to_slug.get(ipa_file.name, ipa_file.stem.replace(' ', '-').lower())
    
    # Получаем размер файла
    size = ipa_file.stat().st_size
    size_mb = round(size / (1024 * 1024), 1)
    size_formatted = f"{size_mb} МБ"
    
    # Проверяем наличие иконки
    icon_path = f"{ICON_DIR}/{slug}.png"
    has_icon = os.path.exists(icon_path)
    
    # Генерируем slug для URL
    url_slug = slug.replace(' ', '-').lower()
    
    app_data = {
        "name": slug.replace('-', ' ').title(),
        "version": "1.0.0",
        "slug": url_slug,
        "size": size,
        "sizeFormatted": size_formatted,
        "manifestUrl": f"https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/{url_slug}/manifest.plist",
        "downloadUrl": f"https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/{url_slug}-1.0.0/{ipa_file.name}",
        "iconUrl": f"icons/{slug}.png" if has_icon else "icons/hz-poster.svg",
        "searchTags": slug.replace('-', ' ')
    }
    apps_data.append(app_data)
    print(f"✓ {app_data['name']} ({size_formatted})")

# Сохраняем
output = f"""// Автоматически сгенерированный список приложений
const APPS = {json.dumps(apps_data, indent=2, ensure_ascii=False)};
"""

with open(f'{SITE_DIR}/app-data.js', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"\n✅ Всего приложений: {len(apps_data)}")
print(f"✅ Файл сохранен: {SITE_DIR}/app-data.js")
