(() => {
  const player = document.getElementById('admin-video-player');
  if (!player) return;
  const source = player.querySelector('source');
  const title = document.getElementById('admin-video-title');
  const description = document.getElementById('admin-video-description');
  const status = document.getElementById('admin-video-status');
  const buttons = [...document.querySelectorAll('.video-clip')];
  const base = '/assets/admin-videos/';

  buttons.forEach(button => button.addEventListener('click', () => {
    if (button.getAttribute('aria-pressed') === 'true') return;
    const name = button.dataset.video;
    const url = `${base}${name}.mp4`;
    player.pause();
    source.src = url;
    player.poster = `${base}${name}-poster.jpg`;
    player.setAttribute('aria-label', `${button.dataset.title} administration recording`);
    title.textContent = button.dataset.title;
    description.textContent = button.dataset.description;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    status.hidden = true;
    player.load();
  }));

  player.addEventListener('error', () => {
    status.textContent = 'This recording could not load. Please try again later.';
    status.hidden = false;
  });
})();
