# iOS OTA Apps Site — Working State Lock

## Sberbank Card (LOCKED - DO NOT CHANGE)

### Layout Structure
```
┌─────────────────────────────────────┐
│ [Иконка]        [QR код]           │
│ [Скачать]                          │
├─────────────────────────────────────┤
│ СберБанк                            │
│ 507 MB                             │
├─────────────────────────────────────┤
│ [Скопировать ссылку]                │
└─────────────────────────────────────┘
```

### CSS Classes
- `.app-card__top` — flex row container
- `.app-card__left` — flex column (icon + download button)
- `.qr-btn` — QR code button (right side)
- `.copy-btn` — copy link button (bottom)
- `.install-button` — download button (below icon)

### Assets
- Icon: `icons/сбербанк.png`
- QR: `icons/сбербанк-qr.png`
- Manifest: `apps/online-com-inv-gen/manifest.plist`

### Install Link
```
itms-services://?action=download-manifest&url=https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/online-com-inv-gen/manifest.plist
```

### Git State
- Branch: main
- Last commit: 0f54607 "Add cache-busting version params to CSS and JS"
- Status: Clean, all changes pushed
