#!/usr/bin/env python3
"""Скачивание всех IPA из Google Drive и загрузка в GitHub Releases"""
import subprocess
import os
import json
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

print("🔄 Синхронизация сайта с Google Drive...\n")

# Читаем app-data.js
with open('/root/projects/ios-ota-apps-site/app-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

apps = re.findall(r'\{"name":"([^"]+)","version":"([^"]+)","slug":"([^"]+)"[^}]+\}', content)
print(f"📋 Приложений на сайте: {len(apps)}\n")

# Получаем список файлов из Google Drive
creds_path = '/root/.hermes/google_token.json'
drive_service = build('drive', 'v3', credentials=Credentials.from_authorized_user_file(creds_path))

# Ищем все IPA файлы
query = "mimeType='application/zip'"
results = drive_service.files().list(q=query, pageSize=100).execute().get('files', [])

print(f"📁 Всего IPA файлов в Google Drive: {len(results)}\n")

# Создаем маппинг по именам файлов
drive_map = {}
for f in results:
    name = f['name']
    if name.endswith('.ipa'):
        # Удаляем расширение для сравнения
        key = name[:-4]
        drive_map[key] = {'id': f['id'], 'name': name, 'size': f.get('size', 0)}

# Маппинг имен из app-data.js к именам файлов в Drive
name_mapping = {
    'Anero_ ваш онлайн помощник АВИТО': 'анеро-ваш-онлайн-помощник-авито',
    'Atoy': 'atoy',
    'Craftersy ТБАНК': 'craftersy-tbank',
    'FuellnTime ТБАНК ИНВЕСТИЦИИ': 'fuellntime-tbank-investitsii',
    'GetQuot ВТБ ИНВЕСТИЦИИ': 'getquot-vtb-investitsii',
    'GTA  SA 2.2.21': 'gta-sa-2-2-21',
    'GTA III 1.3.13': 'gta-iii-1-3-13',
    'Happ - Proxy Utility Plus': 'happ-proxy-utility-plus',
    'Infinity_Blade_1.4.3_iOS_6.0+_selimseidov@gmail.com': 'infinity-blade-1-4-3-ios-6-0-selimseidov-gmail-com',
    'Infinity_Blade_II_1.3.5_iOS_6.0+_selimseidov@gmail.com': 'infinity-blade-ii-1-3-5-ios-6-0-selimseidov-gmail-com',
    'Infinity_Blade_III_1.4.4_iOS_6.0+_selimseidov@gmail.com': 'infinity-blade-iii-1-4-4-ios-6-0-selimseidov-gmail-com',
    'Most Wanted 1.1.3': 'most-wanted-1-1-3',
    'Online 17.6.1 СБЕРБАНК': 'online-17-6-1-sberbank',
    'PianoWave ПРЕМЬЕР КИНОТЕАТР': 'pianowave-premer-kinoteatr',
    'Real Racing 2 1.13.50': 'real-racing-2-1-13-50',
    'SCB Notes СОВКОМБАНК': 'scb-notes-sovcombank',
    'Solar_ Sun Compass СБЕР ИНВЕСТИЦИИ': 'solar-sun-compass-sber-investitsii',
    'SpeakaBoo СБЕРКИДС': 'speakaboo-sberkids',
    'Spotluma': 'spotluma',
    'TEBOIL': 'teboil',
    'Учимся словам': 'учимся-словам',
    'Ак Барс Онлайн': 'ак-барс-онлайн',
    'Аукцион Au.ru АВИТО': 'аукцион-au-ru-авито',
    'Афина бюджет ПСБ БАНК': 'афина-бюджет-псб-банк',
    'Без наличных MTC PAY': 'без-наличных-mtc-pay',
    'ВК Видео_8.183': 'vk-video-8-183',
    'ВК Музыка_8.30.1': 'vk-music-8-30-1',
    'Делим Вместе АЛЬФА БАНК': 'делим-вместе-альфа-банк',
    'До вершины 5.6.0 ГАЗПРОМБАНК': 'до-вершины-5-6-0-газпромбанк',
    'Дом йоги 10.0.0 MTC': 'дом-йоги-10-0-0-mtc',
    'Здоровье и страхование СОГАЗ': 'здоровье-и-страхование-согаз',
    'INCY': 'incy',
    'Мобио СБЕРМОБАЙЛ': 'mobio-sbermobail',
    'ЮMoney_11.12.0_iOS_13.0+_selimseidov@gmail.com': 'yumoney-11-12-0-ios-13-0-selimseidov-gmail-com',
    'Юла_6.0': 'yula-6-0',
    'Яндекс Сим': 'yandeks-sim',
    'iManager by INS INVEST ИНГОССТРАХ': 'imanager-by-ins-invest-ingossstrakh'
}

cache_dir = Path('/root/.hermes/cache/scratch/ios-apps-full')
cache_dir.mkdir(parents=True, exist_ok=True)

# Скачиваем недостающие файлы
print("📥 Скачивание IPA файлов...\n")
downloaded = 0
for name, version, slug in apps:
    cache_file = cache_dir / f"{slug}.ipa"
    if not cache_file.exists():
        # Ищем в drive_map
        found = False
        for drive_name, data in drive_map.items():
            if slug in drive_name or drive_name in slug:
                print(f"Скачивание: {name}")
                try:
                    request = drive_service.files().get_media(fileId=data['id'])
                    fh = io.FileIO(str(cache_file), 'wb')
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                    fh.close()
                    print(f"  ✓ {data['name']}")
                    downloaded += 1
                    found = True
                    break
                except Exception as e:
                    print(f"  ✗ Ошибка: {e}")
        
        if not found:
            print(f"⚠ Не найден в Drive: {name}")

print(f"\n✅ Скачано {downloaded} файлов")
print(f"📊 Всего в кэше: {len(list(cache_dir.glob('*.ipa')))} IPA файлов")
