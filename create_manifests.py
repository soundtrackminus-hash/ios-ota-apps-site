#!/usr/bin/env python3
"""Создание manifest.plist для каждого приложения"""
import os
import json
from pathlib import Path

SITE_DIR = '/root/projects/ios-ota-apps-site'
APPS_DIR = f'{SITE_DIR}/apps'

# Загрузка данных
with open(f'{SITE_DIR}/app-data.js', 'r') as f:
    content = f.read()
    
# Парсинг из JavaScript файла (грубый, но быстрый)
apps = []
import re
matches = re.findall(r'\{\s*name:\s*"([^"]+)",\s*version:\s*"([^"]*)",\s*slug:\s*"([^"]+)"[^}]+\}', content)
for match in matches:
    apps.append({
        'name': match[0],
        'version': match[1],
        'slug': match[2]
    })

print(f"Найдено приложений для создания manifest: {len(apps)}")

# Создание директорий и manifest файлов
for app in apps:
    slug = app['slug']
    app_dir = f'{APPS_DIR}/{slug}'
    os.makedirs(app_dir, exist_ok=True)
    
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
				<string>{app['version'] or '1.0.0'}</string>
				<key>kind</key>
				<string>software</string>
				<key>title</key>
				<string>{app['name']}</string>
			</dict>
		</dict>
	</array>
</dict>
</plist>'''
    
    manifest_path = f'{app_dir}/manifest.plist'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    
    print(f"  ✓ {app['name']} -> {slug}")

print(f"\n✅ Создано {len(apps)} manifest файлов")
