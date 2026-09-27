#!/usr/bin/env python3
"""Загрузка IPA из Google Drive прямо в GitHub Releases (без кэша)"""
import re
import subprocess
import json
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

print("🔄 Синхронизация IPA: Google Drive → GitHub Releases\n")

# Читаем app-data.js
with open('/root/projects/ios-ota-apps-site/app-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

apps = re.findall(r'"slug":\s*"([^"]+)"', content)
print(f"📋 Приложений на сайте: {len(apps)}\n")

# Получаем релизы
releases = subprocess.run(
    ['gh', 'release', 'list', '--repo', 'soundtrackminus-hash/ios-ota-apps-site', '--json', 'tagName'],
    capture_output=True
)
release_data = json.loads(releases.stdout)
release_map = {r['tagName']: r for r in release_data}

# Создаем Google Drive сервис
creds_path = '/root/.hermes/google_token.json'
drive_service = build('drive', 'v3', credentials=Credentials.from_authorized_user_file(creds_path))

# Получаем все IPA файлы из Drive
results = drive_service.files().list(q="mimeType='application/zip'", pageSize=100).execute().get('files', [])
print(f"📁 IPA файлов в Drive: {len(results)}\n")

# Маппинг slug к именам файлов в Drive
slug_to_drive_names = {
    'craftersy-tbank': ['Craftersy ТБАНК.ipa'],
    'fuellntime-tbank-investitsii': ['FuellnTime ТБАНК ИНВЕСТИЦИИ.ipa'],
    'getquot-vtb-investitsii': ['GetQuot ВТБ ИНВЕСТИЦИИ.ipa'],
    'gta-sa-2-2-21': ['GTA SA 2.2.21.ipa'],
    'gta-iii-1-3-13': ['GTA III 1.3.13.ipa'],
    'happ-proxy-utility-plus': ['Happ - Proxy Utility Plus.ipa'],
    'infinity-blade-1-4-3-ios-6-0-selimseidov-gmail-com': ['Infinity_Blade_1.4.3_iOS_6.0+_selimseidov@gmail.com.ipa'],
    'infinity-blade-ii-1-3-5-ios-6-0-selimseidov-gmail-com': ['Infinity_Blade_II_1.3.5_iOS_6.0+_selimseidov@gmail.com.ipa'],
    'infinity-blade-iii-1-4-4-ios-6-0-selimseidov-gmail-com': ['Infinity_Blade_III_1.4.4_iOS_6.0+_selimseidov@gmail.com.ipa'],
    'most-wanted-1-1-3': ['Most Wanted 1.1.3.ipa'],
    'online-17-6-1-sberbank': ['Online 17.6.1 СБЕРБАНК.ipa'],
    'pianowave-premer-kinoteatr': ['PianoWave ПРЕМЬЕР КИНОТЕАТР.ipa'],
    'real-racing-2-1-13-50': ['Real Racing 2 1.13.50.ipa'],
    'scb-notes-sovcombank': ['SCB Notes СОВКОМБАНК.ipa'],
    'solar-sun-compass-sber-investitsii': ['Solar_ Sun Compass СБЕР ИНВЕСТИЦИИ.ipa'],
    'speakaboo-sberkids': ['SpeakaBoo СБЕРКИДС.ipa'],
    'auktsion-au-ru-avito': ['Аукцион Au.ru АВИТО.ipa'],
    'vk-video-8-183': ['ВК Видео_8.183.ipa'],
    'vk-music-8-30-1': ['ВК Музыка_8.30.1.ipa'],
    'delim-vmeste-alfa-bank': ['Делим Вместе АЛЬФА БАНК.ipa'],
    'do-vershiny-5-6-0-gazprombank': ['До вершины 5.6.0 ГАЗПРОМБАНК.ipa'],
    'dom-yogi-10-0-0-mtc': ['Дом йоги 10.0.0 MTC.ipa'],
    'zdorove-i-strahovanie-sogaz': ['Здоровье и страхование СОГАЗ.ipa'],
    'incy': ['INCY.ipa'],
    'mobio-sbermobail': ['Мобио СБЕРМОБАЙЛ.ipa'],
    'yumoney-11-12-0-ios-13-0-selimseidov-gmail-com': ['ЮMoney_11.12.0_iOS_13.0+_selimseidov@gmail.com.ipa'],
    'yula-6-0': ['Юла_6.0.ipa'],
    'yandeks-sim': ['Яндекс Сим.ipa'],
    'imanager-by-ins-invest-ingossstrakh': ['iManager by INS INVEST ИНГОССТРАХ.ipa']
}

uploaded = 0
skipped = 0
failed = 0

for slug in apps:
    tag = f"{slug}-1.0.0"
    
    if tag not in release_map:
        print(f"⚠ Нет релиза: {tag}")
        skipped += 1
        continue
    
    # Проверяем есть ли уже IPA в релизе
    release_info = subprocess.run(
        ['gh', 'release', 'view', tag, '--repo', 'soundtrackminus-hash/ios-ota-apps-site', '--json', 'assets'],
        capture_output=True
    )
    if release_info.returncode == 0:
        assets = json.loads(release_info.stdout).get('assets', [])
        has_ipa = any(a['name'].endswith('.ipa') for a in assets)
        if has_ipa:
            print(f"✓ Уже есть IPA: {slug}")
            uploaded += 1
            continue
    
    # Ищем файл в Drive
    expected_names = slug_to_drive_names.get(slug, [f'{slug}.ipa'])
    found = False
    
    for expected_name in expected_names:
        for f in results:
            if f['name'] == expected_name:
                file_id = f['id']
                print(f"📥 Загрузка: {expected_name}")
                
                # Скачиваем в память
                request = drive_service.files().get_media(fileId=file_id)
                buffer = io.BytesIO()
                downloader = MediaIoBaseDownload(buffer, request)
                
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                
                # Загружаем в release через subprocess
                buffer.seek(0)
                result = subprocess.run(
                    ['gh', 'release', 'upload', tag, f'--repo', 'soundtrackminus-hash/ios-ota-apps-site', '-', '--clobber'],
                    input=buffer.read(),
                    capture_output=True
                )
                
                if result.returncode == 0:
                    size_mb = len(buffer.getvalue()) // 1024 // 1024
                    print(f"  ✓ Загружено ({size_mb} MB)")
                    uploaded += 1
                    found = True
                    break
                else:
                    print(f"  ✗ Ошибка загрузки: {result.stderr.decode()[:50]}")
                    failed += 1
                    found = True
                    break
    
    if not found:
        print(f"⚠ Не найден в Drive: {slug}")
        failed += 1

print(f"\n✅ Загружено: {uploaded}")
print(f"⚠ Пропущено: {skipped}")
print(f"❌ Ошибок: {failed}")
