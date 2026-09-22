# iPhone Apps OTA Site

Статический сайт-каталог iOS-приложений для установки через `itms-services` и `manifest.plist`.

Сайт: https://soundtrackminus-hash.github.io/ios-ota-apps-site/

## Приложения

- Яндекс Банк 0.234.4 — `com.yandex.fintech.bank-app` — `apps/yandex-pay-0-234-4/manifest.plist`
- SlicingDices 1.2.1 — `com.slicingdice.game` — `apps/slicingdices/manifest.plist`
- Relaxia 2.6 — `com.payIX.RelaxToSleepPaid` — `apps/relaxia/manifest.plist`
- MAX 26.17.3 — `ru.oneme.app` — `apps/max/manifest.plist`
- FileHub 10.3.5 — `com.imoreapps.portabledisk` — `apps/filehub/manifest.plist`

## Схема

- Сайт и manifest-файлы: GitHub Pages.
- IPA-файлы: GitHub Releases.
- Кнопка установки ведёт на `itms-services://?action=download-manifest&url=https://.../manifest.plist`.

## Важно

- Все ссылки должны быть HTTPS.
- IPA должен быть подписан корректным сертификатом/provisioning profile, иначе iPhone может скачать файл, но не установить приложение.
