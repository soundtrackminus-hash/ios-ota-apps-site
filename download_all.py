#!/usr/bin/env python3
"""Скачивание всех IPA файлов из Google Drive и извлечение иконок"""
import json
import os
import zipfile
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SITE_DIR = '/root/projects/ios-ota-apps-site'
ICON_DIR = f'{SITE_DIR}/icons'
CACHE_DIR = '/root/.hermes/cache/scratch/ios-apps'
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)

# Загрузка токена
token_path = '/root/.hermes/google_token.json'
with open(token_path) as f:
    data = json.load(f)
creds = Credentials.from_authorized_user_info(data)
drive = build('drive', 'v3', credentials=creds)

# Загрузка метаданных
with open(f'{SITE_DIR}/drive_apps.json') as f:
    metadata = json.load(f)

print(f"Начинаю обработку {metadata['total']} приложений...")

processed = 0
for app in metadata['apps']:
    drive_id = app['drive_id']
    app_name = app['name']
    slug = app['slug']
    
    print(f"\n[{processed+1}/{metadata['total']}] {app_name} ({slug})")
    
    # Скачивание IPA
    ipa_path = f'{CACHE_DIR}/{slug}.ipa'
    if not os.path.exists(ipa_path):
        try:
            print(f"  ⬇ Скачивание из Google Drive...")
            request = drive.files().get_media(fileId=drive_id)
            fh = io.FileIO(ipa_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*10)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                downloaded_mb = int(status.resumable_progress) // (1024*1024)
                print(f"     {downloaded_mb}MB")
            fh.close()
            print(f"  ✓ Скачано: {ipa_path}")
        except Exception as e:
            print(f"  ✗ Ошибка скачивания: {e}")
            continue
    else:
        print(f"  ✓ Уже скачан")
    
    # Извлечение иконки
    icon_path = f'{ICON_DIR}/{slug}.png'
    if not os.path.exists(icon_path):
        try:
            with zipfile.ZipFile(ipa_path, 'r') as z:
                icon_files = [n for n in z.namelist() if 'Icon' in n and n.endswith('.png')]
                if icon_files:
                    # Берём самую большую иконку (3x)
                    icon_files.sort(key=lambda x: z.getinfo(x).file_size, reverse=True)
                    best_icon = icon_files[0]
                    icon_data = z.read(best_icon)
                    with open(icon_path, 'wb') as f:
                        f.write(icon_data)
                    print(f"  ✓ Иконка: {best_icon} ({len(icon_data)} байт)")
                else:
                    print(f"  ⚠ Иконка не найдена в IPA")
        except Exception as e:
            print(f"  ⚠ Ошибка извлечения иконки: {e}")
    
    processed += 1

print(f"\n✅ Обработка завершена!")
print(f"Обработано приложений: {processed}")
print(f"Иконок в папке icons/: {len(list(Path(ICON_DIR).glob('*.png')))}")
