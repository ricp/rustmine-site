(() => {
  const filters = document.querySelector('.works-filters');
  const entries = [...document.querySelectorAll('[data-works-area]')];
  const status = document.querySelector('.works-filter-status');
  if (!filters || !entries.length || !status) return;
  const buttons = [...filters.querySelectorAll('[data-works-filter]')];
  filters.addEventListener('click', event => {
    const button = event.target.closest('button[data-works-filter]');
    if (!button || !filters.contains(button)) return;
    const area = button.dataset.worksFilter;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    entries.forEach(entry => { entry.hidden = area !== 'all' && entry.dataset.worksArea !== area; });
    status.textContent = `${entries.filter(entry => !entry.hidden).length} of ${entries.length} areas shown · ${button.textContent}`;
  });
  filters.hidden = false;
  status.textContent = `${entries.length} of ${entries.length} areas shown · All areas`;
  status.hidden = false;
})();
