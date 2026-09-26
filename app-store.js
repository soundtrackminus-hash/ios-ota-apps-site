function renderApps(apps) {
  const container = document.getElementById('apps-container');
  container.innerHTML = apps.map(app => `
    <article class="app-card" data-search="${app.searchTags} ${app.name}">
      <div class="app-card__icon">
        <img src="${app.iconUrl}" alt="${app.name}" loading="lazy">
      </div>
      <div class="app-card__info">
        <h2 class="app-card__name">${app.name}</h2>
        <p class="app-card__size">${app.sizeFormatted}</p>
      </div>
      <div class="app-card__actions">
        <a class="install-button" href="itms-services://?action=download-manifest&url=${encodeURIComponent(app.manifestUrl)}">
          Установить
        </a>
        <button class="copy-btn" onclick="copyLink('${app.manifestUrl}', this)">
          Копировать
        </button>
      </div>
    </article>
  `).join('');
}

function copyLink(url, btn) {
  navigator.clipboard.writeText(url).then(() => {
    btn.classList.add('copied');
    btn.textContent = '✓ Готово';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.textContent = 'Копировать';
    }, 1500);
  });
}

function filterAndSort() {
  const query = document.getElementById('search').value.toLowerCase();
  const sort = document.getElementById('sort').value;
  
  let filtered = APPS.filter(app => 
    app.searchTags.toLowerCase().includes(query) ||
    app.name.toLowerCase().includes(query)
  );
  
  filtered.sort((a, b) => {
    switch(sort) {
      case 'name-asc': return a.name.localeCompare(b.name, 'ru');
      case 'size-asc': return a.size - b.size;
      case 'size-desc': return b.size - a.size;
      default: return 0;
    }
  });
  
  renderApps(filtered);
  updateCounter(filtered.length, APPS.length);
}

function updateCounter(shown, total) {
  document.getElementById('shown-count').textContent = shown;
  document.getElementById('total-count').textContent = total;
}

document.getElementById('search').addEventListener('input', filterAndSort);
document.getElementById('sort').addEventListener('change', filterAndSort);

renderApps(APPS);
updateCounter(APPS.length, APPS.length);
