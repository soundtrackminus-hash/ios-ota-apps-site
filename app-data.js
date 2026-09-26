// Полный каталог iOS приложений
const APPS = [
  // Новые приложения из Google Drive
  {
    name: "Ак Барс Онлайн",
    version: "2.2.21",
    slug: "ак-барс-онлайн",
    bundleId: "ru.abb.akbarsonline",
    size: 89478485,
    sizeFormatted: "85.3 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/ак-барс-онлайн/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/ak-bars-v2.2.21/ak_bars_real.ipa",
    iconUrl: "icons/ак-барс-онлайн.png",
    searchTags: "ак барс банк акbars акбарс онлайн"
  },
  {
    name: "Афина Бюджет ПСБ Банк",
    version: "1.0.0",
    slug: "афина-бюджет-псб-банк",
    bundleId: "uz.svoybyudzhet",
    size: 45000000,
    sizeFormatted: "42.9 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/афина-бюджет-псб-банк/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/aфина-byudzhet-psb-bank-1.0.0/Aфина_бюджет_ПСБ_БАНК.ipa",
    iconUrl: "icons/афина-бюджет-псб-банк.png",
    searchTags: "афина бюджет псб банк"
  },
  {
    name: "Без наличных MTC PAY",
    version: "1.0.0",
    slug: "без-наличных-mtc-pay",
    bundleId: "ru.stream.pay",
    size: 67000000,
    sizeFormatted: "63.9 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/без-наличных-mtc-pay/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/bez-nalichnyh-mtc-pay-1.0.0/Без_наличных_MTC_PAY.ipa",
    iconUrl: "icons/без-наличных-mtc-pay.png",
    searchTags: "без наличных мтс pay"
  },
  {
    name: "Делим Вместе Альфа Банк",
    version: "1.0.0",
    slug: "делим-вместе-альфа-банк",
    bundleId: "com.alfabank.delimvmeste",
    size: 34000000,
    sizeFormatted: "32.4 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/делим-вместе-альфа-банк/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/delim-vmite-alfa-bank-1.0.0/Делим_Вместе_АЛЬФА_БАНК.ipa",
    iconUrl: "icons/делим-вместе-альфа-банк.png",
    searchTags: "делим вместе альфа банк"
  },
  {
    name: "Spotluma",
    version: "1.0.0",
    slug: "spotluma",
    bundleId: "app.cleanorder.hudorban",
    size: 12000000,
    sizeFormatted: "11.4 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/spotluma/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/spotluma-1.0.0/Spotluma.ipa",
    iconUrl: "icons/spotluma.png",
    searchTags: "spotluma order"
  },
  {
    name: "TEBOIL",
    version: "1.0.0",
    slug: "teboil",
    bundleId: "com.teboil.azs",
    size: 28000000,
    sizeFormatted: "26.7 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/teboil/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/teboil-1.0.0/TEBOIL.ipa",
    iconUrl: "icons/teboil.png",
    searchTags: "teboil бензин заправка"
  },
  {
    name: "Учимся словам",
    version: "1.0.0",
    slug: "учимся-словам",
    bundleId: "com.education.words",
    size: 15000000,
    sizeFormatted: "14.3 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/учимся-словам/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/учимся-словам-1.0.0/Учимся_словам.ipa",
    iconUrl: "icons/учимся-словам.png",
    searchTags: "учимся словам образование"
  },
  {
    name: "Atoy",
    version: "1.0.0",
    slug: "atoy",
    bundleId: "com.atoy.app",
    size: 22000000,
    sizeFormatted: "21.0 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/atoy/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/atoy-1.0.0/Atoy.ipa",
    iconUrl: "icons/atoy.png",
    searchTags: "atoy toy"
  },
  // Существующие приложения (GTA, Real Racing 2)
  {
    name: "GTA: San Andreas",
    version: "2.2.21",
    slug: "gta-sa",
    bundleId: "com.rockstargames.gta3sa",
    size: 1933511605,
    sizeFormatted: "1.84 ГБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/gta-sa/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/gta-sa-2.2.21/GTA_SA_2.2.21.ipa",
    iconUrl: "icons/gta-sa.png",
    searchTags: "gta san andreas rockstar gameplay"
  },
  {
    name: "Real Racing 2",
    version: "1.13.50",
    slug: "real-racing-2",
    bundleId: "com.firemint.realracing2",
    size: 315000000,
    sizeFormatted: "300.5 МБ",
    manifestUrl: "https://soundtrackminus-hash.github.io/ios-ota-apps-site/apps/real-racing-2/manifest.plist",
    downloadUrl: "https://github.com/soundtrackminus-hash/ios-ota-apps-site/releases/download/real-racing-2-1.13.50/racing2.ipa",
    iconUrl: "icons/real-racing-2.png",
    searchTags: "real racing realracing2"
  }
];
