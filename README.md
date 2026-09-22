# iPhone Apps OTA Site

Статический сайт-каталог iOS-приложений для установки через `itms-services` и `manifest.plist`.

Сайт: https://soundtrackminus-hash.github.io/ios-ota-apps-site/

## Приложения (15)

- OK 11.63.1 — `ru.odnoklassniki.iphone` — `apps/ok/manifest.plist`
- Яндекс Банк 0.234.4 — `com.yandex.fintech.bank-app` — `apps/yandeks-bank/manifest.plist`
- Сириус 2.0.1 — `com.sm.FlowTime` — `apps/sirius/manifest.plist`
- SplitActivities 28052025.3 — `com.splitactivities.app` — `apps/splitactivities/manifest.plist`
- Лента 6.81.0 — `com.icemobile.lenta` — `apps/lenta/manifest.plist`
- VK 8.183.1 — `com.vk.vkclient` — `apps/vk/manifest.plist`
- Автотека 2.5.3 — `ru.abd.autoteka.application` — `apps/avtoteka/manifest.plist`
- Бак+Бонус 1.1.1 — `ru.bakbonus.appstarter` — `apps/bak-bonus/manifest.plist`
- Toast 2.0.1 — `com.toastmaster.app` — `apps/toast/manifest.plist`
- SlicingDices 1.2.1 — `com.slicingdice.game` — `apps/slicingdices/manifest.plist`
- SilentFund 1.3.1 — `com.silentmap.app` — `apps/silentfund/manifest.plist`
- Relaxia 2.6 — `com.payIX.RelaxToSleepPaid` — `apps/relaxia/manifest.plist`
- MAX 26.17.3 — `ru.oneme.app` — `apps/max/manifest.plist`
- FileHub 10.3.5 — `com.imoreapps.portabledisk` — `apps/filehub/manifest.plist`
- Notion 0.4.2220 — `notion.id` — `apps/notion/manifest.plist`

## Схема

- Сайт и manifest-файлы: GitHub Pages.
- IPA-файлы: GitHub Releases.
- Кнопка установки ведёт на `itms-services://?action=download-manifest&url=https://.../manifest.plist`.

## Важно

- Все ссылки должны быть HTTPS.
- IPA должен быть подписан корректным сертификатом/provisioning profile, иначе iPhone может скачать файл, но не установить приложение.
