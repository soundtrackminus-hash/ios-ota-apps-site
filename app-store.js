// Генерация карточек приложений
function renderApps(apps) {
  const container = document.getElementById('apps-container');
  container.innerHTML = apps.map(app => `
    <article class="app-card" data-search="${app.searchTags} ${app.name} ${app.bundleId}">
      <div class="app-card__icon">
        <img src="${app.iconUrl}" alt="${app.name}" loading="lazy">
      </div>
      <div class="app-card__body">
        <div class="app-card__topline">
          <h2>${app.name}</h2>
          <span class="version">v${app.version}</span>
        </div>
        <p class="app-card__size">Размер: ${app.sizeFormatted}</p>
        <div class="actions">
          <a class="install-button" href="itms-services://?action=download-manifest&url=${encodeURIComponent(app.manifestUrl)}">
            Установить на iPhone
          </a>
          <button class="copy-btn" onclick="copyLink('${app.manifestUrl}', this)" title="Копировать ссылку на установку">
            📋 Копировать ссылку
          </button>
        </div>
      </div>
    </article>
  `).join('');
}

// Копирование ссылки
function copyLink(url, btn) {
  navigator.clipboard.writeText(url).then(() => {
    const original = btn.textContent;
    btn.textContent = '✓ Скопировано!';
    setTimeout(() => btn.textContent = original, 1500);
  });
}

// Фильтрация и сортировка
function filterAndSort() {
  const query = document.getElementById('search').value.toLowerCase();
  const sort = document.getElementById('sort').value;
  
  let filtered = APPS.filter(app => 
    app.searchTags.toLowerCase().includes(query) ||
    app.name.toLowerCase().includes(query) ||
    app.bundleId.toLowerCase().includes(query)
  );
  
  // Сортировка
  filtered.sort((a, b) => {
    switch(sort) {
      case 'name-asc':
        return a.name.localeCompare(b.name, 'ru');
      case 'name-desc':
        return b.name.localeCompare(a.name, 'ru');
      case 'size-asc':
        return a.size - b.size;
      case 'size-desc':
        return b.size - a.size;
      default:
        return 0;
    }
  });
  
  renderApps(filtered);
  updateCounter(filtered.length, APPS.length);
}

function updateCounter(shown, total) {
  document.getElementById('shown-count').textContent = shown;
  document.getElementById('total-count-display').textContent = total;
  document.getElementById('total-count').textContent = total;
}

// Слушатели событий
document.getElementById('search').addEventListener('input', filterAndSort);
document.getElementById('sort').addEventListener('change', filterAndSort);

// Инициализация
renderApps(APPS);
updateCounter(APPS.length, APPS.length);
