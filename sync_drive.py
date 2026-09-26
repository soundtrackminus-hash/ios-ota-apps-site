#!/usr/bin/env python3
"""Синхронизация сайта iOS OTA Apps с Google Drive"""
import json
import os
import zipfile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Загрузка токена
token_path = '/root/.hermes/google_token.json'
with open(token_path) as f:
    data = json.load(f)
creds = Credentials.from_authorized_user_info(data)
drive = build('drive', 'v3', credentials=creds)

# Получение списка всех IPA файлов
results = drive.files().list(q="mimeType = 'application/x-itunes-ipa'", pageSize=100).execute()
files = results.get('files', [])

apps = []
for f in sorted(files, key=lambda x: x['name'].lower()):
    apps.append({
        'name': f['name'],
        'id': f['id'],
        'size': int(f.get('size', 0))
    })

print(f"Всего IPA в Drive: {len(apps)}")
for a in apps:
    size_mb = a['size'] // (1024*1024)
    print(f"  • {a['name']} ({size_mb}MB)")

# Сохранение списка
output = {
    'total': len(apps),
    'apps': apps
}
with open('/root/projects/ios-ota-apps-site/drive_apps.json', 'w') as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print(f"\nСохранено в drive_apps.json")
