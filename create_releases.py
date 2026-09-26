#!/usr/bin/env python3
"""Создание GitHub Release для всех приложений"""
import subprocess
import os
import json
from pathlib import Path

SITE_DIR = '/root/projects/ios-ota-apps-site'
CACHE_DIR = '/root/.hermes/cache/scratch/ios-apps'
REPO = 'soundtrackminus-hash/ios-ota-apps-site'

# Загрузка метаданных
with open(f'{SITE_DIR}/drive_apps.json') as f:
    metadata = json.load(f)

# Проверяем какие приложения уже имеют release
result = subprocess.run(['gh', 'release', 'list', '--repo', REPO], capture_output=True, text=True)
existing_releases = set()
for line in result.stdout.strip().split('\n'):
    if line:
        parts = line.split('\t')
        if parts:
            release_tag = parts[2]  # third column is tag
            existing_releases.add(release_tag)
            print(f"Уже есть: {parts[0]} ({release_tag})")

print(f"\nВсего релизов: {len(existing_releases)}")

created = []
for app in metadata['apps']:
    slug = app['slug']
    ipa_path = f'{CACHE_DIR}/{slug}.ipa'
    
    if not os.path.exists(ipa_path):
        print(f"⊘ Пропуск: {app['name']} (IPA не найден)")
        continue
    
    release_tag = f"{slug}-1.0.0"
    if release_tag in existing_releases:
        print(f"⊘ Пропуск: {app['name']} (релиз уже существует)")
        continue
    
    print(f"🚀 Создание релиза: {app['name']}...")
    
    cmd = [
        'gh', 'release', 'create', release_tag,
        '--repo', REPO,
        '--title', f"{app['name']} {app['version'] or '1.0.0'}",
        '--notes', f"{app['name']} iOS IPA",
        ipa_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        created.append(app['name'])
        print(f"  ✓ Создан: {release_tag}")
    else:
        print(f"  ✗ Ошибка: {result.stderr}")

print(f"\n✅ Создано релизов: {len(created)}")
if created:
    print("Список:", ', '.join(created[:5]) + ('...' if len(created) > 5 else ''))
