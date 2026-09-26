#!/usr/bin/env python3
"""Создание всех недостающих manifest файлов"""
import os
import subprocess
from pathlib import Path

SITE_DIR = '/root/projects/ios-ota-apps-site'
APPS_DIR = f'{SITE_DIR}/apps'
RELEASES_DIR = f'{SITE_DIR}/releases'

# Список всех приложений из app-data.js (берем из JavaScript файла)
apps_to_create = [
    ("анеро-ваш-онлайн-помощник-авито", "Анеро Ваш Онлайн Помощник Авито"),
    ("atoy", "Atoy"),
    ("craftersy", "Craftersy Тбанк"),
    ("fuellntime-тбанк-инвестиции", "Fuellntime Тбанк Инвестиции"),
    ("getquot", "Getquot Втб Инвестиции"),
    ("happ-proxy-utility-plus", "Happ Proxy Utility Plus"),
    ("imanager-by-ins-invest-ингосстрах", "Imanager By Ins Invest Ингосстрах"),
    ("incy", "Incy"),
    ("pianowave-премьер-кинотеатр", "Pianowave Премьер Кинотеатр"),
    ("scb-notes-совкомбанк", "Scb Notes Совкомбанк"),
    ("solar-sun-compass-сбер-инвестиции", "Solar Sun Compass Сбер Инвестиции"),
    ("speakaboo-сберкидс", "Speakaboo Сберкидс"),
    ("spotluma", "Spotluma"),
    ("teboil", "Teboil"),
    ("ак-барс-онлайн", "Ак Барс Онлайн"),
    ("аукцион-au-ru-авито", "Аукцион Au Ru Авито"),
    ("афина-бюджет-псб-банк", "Афина Бюджет Псб Банк"),
    ("без-наличных-mtc-pay", "Без Наличных Mtc Pay"),
    ("делим-вместе-альфа-банк", "Делим Вместе Альфа Банк"),
    ("mobio-сбермобайл", "Mobio Сбермобайл"),
    ("учимся-словам", "Учимся Словам"),
    ("яндекс-сим", "Яндекс Сим"),
]

os.makedirs(RELEASES_DIR, exist_ok=True)

for slug, name in apps_to_create:
    app_dir = f'{APPS_DIR}/{slug}'
    manifest_path = f'{app_dir}/manifest.plist'
    
    if os.path.exists(manifest_path):
        print(f"✓ Уже существует: {name}")
        continue
    
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
				<string>1.0.0</string>
				<key>kind</key>
				<string>software</string>
				<key>title</key>
				<string>{name}</string>
			</dict>
		</dict>
	</array>
</dict>
</plist>'''
    
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    
    print(f"✓ Создан: {name}")

print("\n✅ Готово!")
