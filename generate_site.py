#!/usr/bin/env python3
"""Генерация сайта iOS OTA Apps из данных Google Drive"""
import json
import os
import zipfile
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Конфигурация
SITE_DIR = '/root/projects/ios-ota-apps-site'
ICON_DIR = f'{SITE_DIR}/icons'
APPS_DIR = f'{SITE_DIR}/apps'
PROJECT_NAME = 'ios-ota-apps-site'
GITHUB_USER = 'soundtrackminus-hash'
BASE_URL = f'https://soundtrackminus-hash.github.io/{PROJECT_NAME}'

# Загрузка токена
token_path = '/root/.hermes/google_token.json'
with open(token_path) as f:
    data = json.load(f)
creds = Credentials.from_authorized_user_info(data)
drive = build('drive', 'v3', credentials=creds)

# Получение списка IPA файлов
results = drive.files().list(q="mimeType = 'application/x-itunes-ipa'", pageSize=100).execute()
files = results.get('files', [])

print(f"Найдено IPA файлов в Drive: {len(files)}")

# Словарь для маппинга имени файла на App ID
app_data = []

for f in files:
    app_id = f['id']
    name = f['name']
    
    # Парсинг имени файла для получения метаданных
    # Формат: "AppName version.ipa" или "AppName.ipa"
    clean_name = name.replace('.ipa', '').strip()
    
    # Пытаемся извлечь версию
    version_match = re.search(r'(\d+\.\d+(\.\d+)?)', clean_name)
    version = version_match.group(1) if version_match else ''
    
    # Очистка имени приложения
    app_name = re.sub(r'\s*\d+\.\d+(\.\d+)?\.ipa$', '', clean_name).strip()
    app_name = re.sub(r'\s*[\-_]\s*(iOS|IOS)\s*.*$', '', app_name).strip()
    
    # Определение slug
    slug = re.sub(r'[^a-zа-яё0-9\-]', '-', app_name.lower()).strip('-')
    slug = re.sub(r'-+', '-', slug)
    
    app_data.append({
        'name': app_name,
        'version': version,
        'slug': slug,
        'drive_id': app_id,
        'drive_name': name,
        'size': int(f.get('size', 0))
    })

print(f"\nОбработано приложений: {len(app_data)}")
for a in app_data[:5]:
    print(f"  • {a['name']} (v{a['version']}) -> {a['slug']}")

# Создание директорий
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(APPS_DIR, exist_ok=True)

# Загрузка существующих иконок
existing_icons = {}
for icon_file in Path(ICON_DIR).glob('*.png'):
    existing_icons[icon_file.stem] = icon_file

print(f"\nНайдено существующих иконок: {len(existing_icons)}")

# Сохранение метаданных
metadata = {
    'total': len(app_data),
    'apps': [
        {
            'name': a['name'],
            'version': a['version'],
            'slug': a['slug'],
            'drive_id': a['drive_id'],
            'drive_name': a['drive_name'],
            'size': a['size'],
            'has_icon': a['slug'] in existing_icons
        }
        for a in app_data
    ]
}
with open(f'{SITE_DIR}/drive_apps.json', 'w') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"\nМетаданные сохранены в drive_apps.json")
print(f"\nСписок приложений (первые 10):")
for a in app_data[:10]:
    print(f"  • {a['name']} v{a['version']} ({a['slug']})")
