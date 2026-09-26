#!/usr/bin/env python3
"""Синхронизация сайта с Google Drive - полное обновление"""
import json
import os
import zipfile
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SITE_DIR = '/root/projects/ios-ota-apps-site'
CACHE_DIR = '/root/.hermes/cache/scratch/ios-apps-sync'
ICON_DIR = f'{SITE_DIR}/icons'
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)

# Загрузка токена
token_path = '/root/.hermes/google_token.json'
with open(token_path) as f:
    data = json.load(f)
creds = Credentials.from_authorized_user_info(data)
drive = build('drive', 'v3', credentials=creds)

# Получение списка из Google Drive
results = drive.files().list(q="mimeType = 'application/x-itunes-ipa'", pageSize=100).execute()
drive_apps = results.get('files', [])

print(f"📁 В Google Drive: {len(drive_apps)} IPA файлов\n")

# Парсинг названий из Drive
drive_names = set()
for f in drive_apps:
    name = f['name'].replace('.ipa', '').strip()
    drive_names.add(name.lower())
    print(f"  • {f['name']}")

print(f"\n📊 Всего названий в Drive: {len(drive_names)}")

# Читаем текущий список с сайта
with open(f'{SITE_DIR}/app-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Извлекаем имена приложений из JS
current_apps = re.findall(r'"name":\s*"([^"]+)"', content)
current_slugs = re.findall(r'"slug":\s*"([^"]+)"', content)

# Создаем словарь для маппинга
site_apps = {}
for i, name in enumerate(current_apps):
    site_apps[name.lower()] = {
        'name': name,
        'slug': current_slugs[i] if i < len(current_slugs) else ''
    }

print(f"\n📊 На сайте сейчас: {len(site_apps)} приложений")
print("Текущие приложения:")
for name in sorted(site_apps.keys()):
    print(f"  • {name}")

# Определяем что нужно удалить (есть на сайте, нет в Drive)
to_remove = []
for name_lower in site_apps:
    # Проверяем, есть ли это название в Drive
    found = False
    for drive_name in drive_names:
        # Нормализуем для сравнения
        if name_lower.replace(' ', '') == drive_name.replace(' ', ''):
            found = True
            break
        # Или точное совпадение
        if name_lower == drive_name:
            found = True
            break
    
    if not found:
        to_remove.append(site_apps[name_lower])
        print(f"\n❌ УДАЛИТЬ (нет в Drive): {site_apps[name_lower]['name']}")

# Определяем что нужно добавить (есть в Drive, нет на сайте)
to_add = []
for drive_file in drive_apps:
    name = drive_file['name'].replace('.ipa', '').strip()
    name_lower = name.lower().replace(' ', '')
    
    found = False
    for site_name_lower in site_apps:
        if site_name_lower.replace(' ', '') == name_lower:
            found = True
            break
        if site_name_lower == name_lower:
            found = True
            break
    
    if not found:
        to_add.append({
            'name': name,
            'drive_id': drive_file['id'],
            'drive_name': drive_file['name']
        })
        print(f"\n➕ ДОБАВИТЬ (нет на сайте): {name}")

print(f"\n📋 Итого: удалить {len(to_remove)}, добавить {len(to_add)}")

# Сохраняем для использования
result = {
    'drive_count': len(drive_apps),
    'site_count': len(site_apps),
    'to_remove': to_remove,
    'to_add': to_add,
    'drive_files': [
        {
            'name': f['name'].replace('.ipa', ''),
            'id': f['id'],
            'slug': re.sub(r'[^a-zа-яё0-9\-]', '-', f['name'].replace('.ipa', '').lower()).strip('-')
        }
        for f in drive_apps
    ]
}

with open(f'{SITE_DIR}/sync_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ Результат сохранен в sync_result.json")
