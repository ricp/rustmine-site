(() => {
      const counter = document.getElementById('days-since-start');
      const firstCommit = document.getElementById('first-commit-date');
      if (!counter || !firstCommit) return;
      const start = new Date(firstCommit.dateTime);
      if (Number.isNaN(start.getTime())) return;
      const bangkokDate = new Intl.DateTimeFormat('en-US', {
        timeZone: 'Asia/Bangkok', year: 'numeric', month: '2-digit', day: '2-digit'
      });
      const calendarDay = date => {
        const parts = Object.fromEntries(bangkokDate.formatToParts(date).map(part => [part.type, part.value]));
        return Date.UTC(Number(parts.year), Number(parts.month) - 1, Number(parts.day));
      };
      const startDay = calendarDay(start);
      function update() {
        counter.textContent = String(Math.max(0, Math.round((calendarDay(new Date()) - startDay) / 86400000)));
      }
      update();
      setInterval(update, 60000);
      document.addEventListener('visibilitychange', () => { if (!document.hidden) update(); });
    })();
    (() => {
      const menu = document.getElementById('mobile-menu');
      if (!menu) return;
      const summary = menu.querySelector('summary');
      menu.querySelectorAll('a').forEach(link => link.addEventListener('click', () => { menu.open = false; }));
      document.addEventListener('keydown', event => {
        if (event.key === 'Escape' && menu.open) { event.preventDefault(); menu.open = false; summary.focus(); }
      });
      window.addEventListener('resize', () => { if (window.innerWidth > 1050) menu.open = false; });
    })();
    (() => {
      const buttons = [...document.querySelectorAll('[data-filter]')];
      const entries = [...document.querySelectorAll('.entry[data-category]')];
      const empty = document.getElementById('timeline-empty');
      buttons.forEach(button => button.addEventListener('click', () => {
        const selected = button.dataset.filter;
        buttons.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        let visible = 0;
        entries.forEach(entry => {
          entry.hidden = selected !== 'all' && entry.dataset.category !== selected;
          if (!entry.hidden) visible += 1;
        });
        empty.hidden = visible > 0;
      }));
    })();
    (() => {
      const viewer = document.getElementById('screen-viewer');
      const image = document.getElementById('viewer-image');
      const title = document.getElementById('viewer-title');
      const description = document.getElementById('viewer-description');
      const scroll = document.getElementById('viewer-scroll');
      const fit = document.getElementById('viewer-fit');
      const minus = document.getElementById('viewer-minus');
      const plus = document.getElementById('viewer-plus');
      const close = document.getElementById('viewer-close');
      const background = [document.querySelector('.site-header'), document.querySelector('main'), document.querySelector('.privacy-note'), document.querySelector('footer')].filter(Boolean);
      const zoomSteps = [.5, .75, 1, 1.25, 1.5, 2, 3];
      let opener = null;
      let nativeWidth = 0;
      let zoom = null;

      function setZoom(value) {
        zoom = value;
        image.style.width = value === null ? 'auto' : `${Math.round(nativeWidth * value)}px`;
        image.style.maxWidth = value === null ? '100%' : 'none';
        document.getElementById('viewer-zoom').textContent = value === null ? 'Fit' : `${Math.round(value * 100)}%`;
        minus.disabled = value !== null && value <= zoomSteps[0];
        plus.disabled = value !== null && value >= zoomSteps[zoomSteps.length - 1];
      }

      function changeZoom(direction) {
        if (zoom === null) { setZoom(direction > 0 ? 1 : .75); return; }
        const index = zoomSteps.indexOf(zoom);
        setZoom(zoomSteps[Math.max(0, Math.min(zoomSteps.length - 1, index + direction))]);
      }

      function openViewer(button) {
        const source = button.querySelector('img');
        const caption = button.closest('figure').querySelector('figcaption');
        opener = button;
        nativeWidth = source.naturalWidth || Number(source.getAttribute('width'));
        title.textContent = caption.querySelector('strong').textContent;
        description.textContent = caption.querySelector('.screen-caption').textContent;
        image.src = source.src;
        image.alt = source.alt;
        setZoom(null);
        scroll.scrollTop = 0;
        scroll.scrollLeft = 0;
        viewer.hidden = false;
        background.forEach(element => { element.inert = true; });
        document.body.classList.add('viewer-open');
        close.focus();
      }

      function closeViewer() {
        if (viewer.hidden) return;
        viewer.hidden = true;
        background.forEach(element => { element.inert = false; });
        document.body.classList.remove('viewer-open');
        image.removeAttribute('src');
        if (opener && opener.isConnected) opener.focus({ preventScroll: true });
        opener = null;
      }

      document.querySelectorAll('a.screen-open').forEach(link => link.addEventListener('click', event => { openViewer(link); event.preventDefault(); }));
      fit.addEventListener('click', () => { setZoom(null); scroll.scrollTop = 0; scroll.scrollLeft = 0; });
      minus.addEventListener('click', () => changeZoom(-1));
      plus.addEventListener('click', () => changeZoom(1));
      close.addEventListener('click', closeViewer);
      viewer.addEventListener('click', event => { if (event.target === viewer) closeViewer(); });
      document.addEventListener('keydown', event => {
        if (viewer.hidden) return;
        if (event.key === 'Escape') { event.preventDefault(); closeViewer(); return; }
        if (event.key !== 'Tab') return;
        const focusable = [...viewer.querySelectorAll('button:not(:disabled), [tabindex="0"]')];
        const first = focusable[0];
        const last = focusable[focusable.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      });
    })();
    (() => {
      document.querySelectorAll('.build-chart-day').forEach(link => link.addEventListener('click', () => {
        const note = document.getElementById(new URL(link.href).hash.slice(1));
        if (note) note.open = true;
      }));
    })();
  
    (() => {
      function revealHash() {
        const id = decodeURIComponent(location.hash.slice(1));
        const target = id && document.getElementById(id);
        if (!target) return;
        for (let node = target; node; node = node.parentElement) if (node.tagName === 'DETAILS') node.open = true;
        requestAnimationFrame(() => target.scrollIntoView());
      }
      window.addEventListener('hashchange', revealHash);
      if (location.hash) window.addEventListener('load', revealHash, { once: true });
    })();
