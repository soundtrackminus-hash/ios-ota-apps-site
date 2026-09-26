#!/usr/bin/env python3
"""Полная синхронизация сайта с Google Drive"""
import json
import os
import zipfile
import re
import subprocess
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import io

SITE_DIR = '/root/projects/ios-ota-apps-site'
CACHE_DIR = '/root/.hermes/cache/scratch/ios-apps-full'
ICON_DIR = f'{SITE_DIR}/icons'
APPS_DIR = f'{SITE_DIR}/apps'
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(ICON_DIR, exist_ok=True)
os.makedirs(APPS_DIR, exist_ok=True)

# Загрузка токена
token_path = '/root/.hermes/google_token.json'
with open(token_path) as f:
    data = json.load(f)
creds = Credentials.from_authorized_user_info(data)
drive = build('drive', 'v3', credentials=creds)

print("🔄 Получение списка из Google Drive...")
results = drive.files().list(q="mimeType = 'application/x-itunes-ipa'", pageSize=100).execute()
drive_apps = results.get('files', [])

print(f"✅ Найдено {len(drive_apps)} IPA файлов\n")

# Массив для app-data.js
apps_list = []

for idx, file_info in enumerate(drive_apps, 1):
    raw_name = file_info['name']
    clean_name = raw_name.replace('.ipa', '').strip()
    
    # Нормализация для slug
    slug = re.sub(r'[^a-zа-яё0-9\-]', '-', clean_name.lower()).strip('-')
    slug = re.sub(r'-+', '-', slug)
    
    print(f"[{idx}/{len(drive_apps)}] Обработка: {clean_name}")
    
    # 1. Скачивание IPA
    ipa_path = f'{CACHE_DIR}/{slug}.ipa'
    if not os.path.exists(ipa_path):
        print(f"  ⬇ Скачивание...")
        try:
            request = drive.files().get_media(fileId=file_info['id'])
            fh = io.FileIO(ipa_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024*1024*5)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
            fh.close()
            print(f"  ✓ Скачано: {os.path.getsize(ipa_path)//(1024*1024)}MB")
        except Exception as e:
            print(f"  ✗ Ошибка скачивания: {e}")
            continue
    else:
        print(f"  ✓ Уже скачан")
    
    # 2. Извлечение иконки
    icon_path = f'{ICON_DIR}/{slug}.png'
    if not os.path.exists(icon_path):
        try:
            with zipfile.ZipFile(ipa_path, 'r') as z:
                icons = [n for n in z.namelist() if 'Icon' in n and n.endswith('.png')]
                if icons:
                    icons.sort(key=lambda x: z.getinfo(x).file_size, reverse=True)
                    icon_data = z.read(icons[0])
                    with open(icon_path, 'wb') as f:
                        f.write(icon_data)
                    print(f"  ✓ Иконка: {icons[0]} ({len(icon_data)//1024}KB)")
                else:
                    print(f"  ⚠ Иконка не найдена")
        except Exception as e:
            print(f"  ⚠ Ошибка иконки: {e}")
    
    # 3. Создание manifest.plist
    app_dir = f'{APPS_DIR}/{slug}'
    os.makedirs(app_dir, exist_ok=True)
    manifest_path = f'{app_dir}/manifest.plist'
    
    manifest_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>items</key>
	<array>
		<dict>
			<key>assets</key>
			<array>
				<dict>
					<key>kind</key>
					<string>software-package</string>
					<key>url</key>
					<string>https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/{slug}-1.0.0/{slug}.ipa</string>
				</dict>
			</array>
			<key>metadata</key>
			<dict>
				<key>bundle-identifier</key>
				<string>com.example.{slug}</string>
				<key>bundle-version</key>
				<string>1.0.0</string>
				<key>kind</key>
				<string>software</string>
				<key>title</key>
				<string>{clean_name}</string>
			</dict>
		</dict>
	</array>
</dict>
</plist>'''
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"  ✓ Manifest создан")
    
    # 4. Создание GitHub Release
    tag = f"{slug}-1.0.0"
    result = subprocess.run(
        ['gh', 'release', 'view', tag, '--repo', 'soundtrackminus-hash/ios-ota-apps-site'],
        capture_output=True
    )
    
    if result.returncode != 0:
        print(f"  🚀 Создание релиза...")
        release_result = subprocess.run(
            ['gh', 'release', 'create', tag, 
             '--repo', 'soundtrackminus-hash/ios-ota-apps-site',
             '--title', clean_name,
             '--notes', 'iOS IPA',
             ipa_path],
            capture_output=True,
            text=True
        )
        if release_result.returncode == 0:
            print(f"  ✓ Релиз создан")
        else:
            print(f"  ⚠ Ошибка: {release_result.stderr[:100]}")
    else:
        print(f"  ✓ Релиз уже существует")
    
    # 5. Добавление в список
    size_bytes = os.path.getsize(ipa_path)
    size_mb = round(size_bytes / (1024 * 1024), 1)
    
    apps_list.append({
        "name": clean_name,
        "version": "1.0.0",
        "slug": slug,
        "bundleId": f"com.example.{slug}",
        "size": size_bytes,
        "sizeFormatted": f"{size_mb} МБ",
        "manifestUrl": f"https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/{slug}/manifest.plist",
        "downloadUrl": f"https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/{slug}-1.0.0/{slug}.ipa",
        "iconUrl": f"icons/{slug}.png" if os.path.exists(icon_path) else "icons/hz-poster.svg",
        "searchTags": slug.replace('-', ' ')
    })

print(f"\n📊 Всего обработано: {len(apps_list)} приложений")

# Сохранение app-data.js
js_content = f"// Сгенерировано автоматически из Google Drive\nconst APPS = {json.dumps(apps_list, indent=2, ensure_ascii=False)};\n"

with open(f'{SITE_DIR}/app-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"✅ app-data.js обновлен")
print(f"📁 Иконок сохранено: {len(list(Path(ICON_DIR).glob('*.png')))}")
print(f"📁 Manifest файлов: {len(list(Path(APPS_DIR).glob('*/*/manifest.plist')))}")
