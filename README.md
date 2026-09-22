# iPhone Apps OTA Site

Статический сайт-каталог iOS-приложений для установки через `itms-services` и `manifest.plist`.

## Структура

```text
.
├── index.html
├── styles.css
├── icons/
│   └── hz-poster.svg
└── apps/
    └── hz-poster/
        └── manifest.plist
```

## Как пользоваться

1. Создай GitHub-репозиторий и включи GitHub Pages для ветки `main`.
2. Загрузи `.ipa` в GitHub Releases.
3. В `apps/hz-poster/manifest.plist` уже указаны данные FamilyBu:
   - `https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/v1.0.0/FamilyBu.ipa`
   - `selim.anna.company`
   - `1.0.0`
   - `FamilyBu`
4. В `index.html` замени ссылку установки:

```text
itms-services://?action=download-manifest&url=https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/hz-poster/manifest.plist
```

## Важно

- Все ссылки на manifest, IPA и иконки должны быть HTTPS.
- Ссылка на manifest должна быть через GitHub Pages, не `github.com/.../blob/...`.
- IPA должен быть подписан корректным сертификатом/provisioning profile, иначе iPhone может скачать файл, но не установить приложение.
