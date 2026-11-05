// Chayananda Nagesh — portfolio interactions (no dependencies)
(() => {
  const doc = document.documentElement;
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---- Nav: scrolled state + mobile toggle ---- */
  const nav = document.querySelector('.nav');
  if (nav) {
    const onScroll = () => nav.classList.toggle('is-scrolled', window.scrollY > 8);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const toggle = nav.querySelector('.nav__toggle');
    toggle?.addEventListener('click', () => {
      const open = nav.classList.toggle('is-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('.nav__links a').forEach((a) =>
      a.addEventListener('click', () => {
        nav.classList.remove('is-open');
        toggle?.setAttribute('aria-expanded', 'false');
      })
    );
  }

  /* ---- Reveal on scroll (content is visible without JS; safety timer reveals all) ---- */
  const reveals = [...document.querySelectorAll('.reveal')];
  if (reveals.length && 'IntersectionObserver' in window && !reduceMotion) {
    doc.classList.add('js');
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      }),
      { rootMargin: '0px 0px -8% 0px', threshold: 0.05 }
    );
    reveals.forEach((el) => io.observe(el));
    setTimeout(() => reveals.forEach((el) => el.classList.add('is-in')), 2200);
  }

  /* ---- Spotlight on work cards ---- */
  if (finePointer) {
    document.querySelectorAll('.work-card').forEach((card) => {
      card.addEventListener('pointermove', (e) => {
        const r = card.getBoundingClientRect();
        card.style.setProperty('--px', `${e.clientX - r.left}px`);
        card.style.setProperty('--py', `${e.clientY - r.top}px`);
      });
    });
  }

  /* ---- Education badges: tilt, follow the light, spin on tap ---- */
  document.querySelectorAll('.holo').forEach((card) => {
    let frame = 0;
    const MAX = 18; // degrees of tilt at the edges
    const medal = card.querySelector('.badge__medal');

    const apply = (x, y) => {
      // x, y in 0..1 across the whole card
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        const dx = x - 0.5, dy = y - 0.5;
        card.style.setProperty('--ry', `${dx * MAX * 2}deg`);
        card.style.setProperty('--rx', `${-dy * MAX * 2}deg`);
        card.style.setProperty('--mx', `${x * 100}%`);
        card.style.setProperty('--my', `${y * 100}%`);
        card.style.setProperty('--a', `${Math.atan2(dy, dx) * 180 / Math.PI + 90}deg`);
        card.style.setProperty('--o', '1');
      });
    };
    const reset = () => {
      cancelAnimationFrame(frame);
      card.classList.remove('is-active');
      ['--rx', '--ry', '--a'].forEach((v) => card.style.setProperty(v, '0deg'));
      card.style.setProperty('--mx', '50%');
      card.style.setProperty('--my', '30%');
      card.style.setProperty('--o', '0');
    };
    const spin = () => {
      if (reduceMotion || card.classList.contains('is-spinning')) return;
      card.classList.add('is-spinning');
    };
    medal?.addEventListener('animationend', () => card.classList.remove('is-spinning'));

    card.addEventListener('pointerenter', () => card.classList.add('is-active'));
    card.addEventListener('pointermove', (e) => {
      if (reduceMotion) return;
      const r = card.getBoundingClientRect();
      apply((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height);
    });
    card.addEventListener('pointerleave', reset);
    card.addEventListener('pointercancel', reset);
    card.addEventListener('click', spin);
    card.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); spin(); }
    });

    // Keyboard focus: tip the badge toward the light
    card.addEventListener('focus', () => { card.classList.add('is-active'); if (!reduceMotion) apply(0.7, 0.3); });
    card.addEventListener('blur', reset);
  });

  /* ---- NID chip: hover the play button for a short, muted, looping preview ---- */
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
  document.querySelectorAll('.chip__play[data-yt]').forEach((btn) => {
    if (!canHover || reduceMotion) return; // touch / reduced motion: the link just opens YouTube
    const chip = btn.closest('.chip--nid');
    const { yt, from, to } = btn.dataset;
    let peek = null, frame = null, timer = 0;

    const send = (func, args = []) => frame?.contentWindow?.postMessage(
      JSON.stringify({ event: 'command', func, args, id: 'peek', channel: 'widget' }), '*');

    const onMessage = (e) => {
      if (!frame || e.source !== frame.contentWindow) return;
      let data; try { data = JSON.parse(e.data); } catch { return; }
      // Loop the clip: when playback reaches the end of the window (or the player stops), jump back.
      const t = data.info?.currentTime;
      const state = data.event === 'onStateChange' ? data.info : data.info?.playerState;
      if ((typeof t === 'number' && t >= Number(to) - 0.15) || state === 0) {
        send('seekTo', [Number(from), true]);
        send('playVideo');
      }
    };

    const open = () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        if (!peek) {
          peek = document.createElement('div');
          peek.className = 'yt-peek';
          peek.setAttribute('aria-hidden', 'true');
          const q = new URLSearchParams({
            autoplay: '1', mute: '1', controls: '0', playsinline: '1', rel: '0', modestbranding: '1',
            start: from, enablejsapi: '1', origin: location.origin,
          });
          frame = document.createElement('iframe');
          frame.src = `https://www.youtube-nocookie.com/embed/${yt}?${q}`;
          frame.title = 'NID convocation preview';
          frame.tabIndex = -1;
          frame.allow = 'autoplay; encrypted-media';
          frame.addEventListener('load', () => frame.contentWindow.postMessage(
            JSON.stringify({ event: 'listening', id: 'peek', channel: 'widget' }), '*'));
          const cap = document.createElement('span');
          cap.className = 'yt-peek__cap';
          cap.textContent = 'Click to watch';
          peek.append(frame, cap);
          chip.append(peek);
          window.addEventListener('message', onMessage);
        }
        requestAnimationFrame(() => peek.classList.add('is-open'));
      }, 120);
    };
    const close = () => {
      clearTimeout(timer);
      if (!peek) return;
      peek.classList.remove('is-open');
      timer = setTimeout(() => { // remove the player so nothing keeps playing or downloading
        window.removeEventListener('message', onMessage);
        peek.remove(); peek = null; frame = null;
      }, 220);
    };
    btn.addEventListener('pointerenter', open);
    btn.addEventListener('pointerleave', close);
    btn.addEventListener('focus', open);
    btn.addEventListener('blur', close);
  });

  /* ---- Case-study table of contents ---- */
  const tocLinks = [...document.querySelectorAll('.cs-toc a')];
  if (tocLinks.length && 'IntersectionObserver' in window) {
    const map = new Map(tocLinks.map((a) => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver(
      (entries) => entries.forEach((e) => {
        if (e.isIntersecting) {
          tocLinks.forEach((a) => a.classList.remove('is-active'));
          map.get(e.target.id)?.classList.add('is-active');
        }
      }),
      { rootMargin: '-30% 0px -60% 0px' }
    );
    map.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }

  /* ---- Images that fail to load show a designed placeholder ---- */
  document.querySelectorAll('.shot img').forEach((img) => {
    const fail = () => img.closest('.shot')?.classList.add('is-missing');
    if (img.complete && img.naturalWidth === 0) fail();
    img.addEventListener('error', fail, { once: true });
  });

  /* ---- Copy email ---- */
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    btn.addEventListener('click', async () => {
      const text = btn.getAttribute('data-copy');
      const label = btn.querySelector('span');
      try {
        await navigator.clipboard.writeText(text);
        if (label) label.textContent = 'Copied';
      } catch {
        const code = btn.parentElement?.querySelector('code');
        if (code) {
          const range = document.createRange();
          range.selectNodeContents(code);
          const sel = window.getSelection();
          sel.removeAllRanges(); sel.addRange(range);
        }
        if (label) label.textContent = 'Selected — press ⌘C';
      }
      setTimeout(() => { if (label) label.textContent = 'Copy email'; }, 2200);
    });
  });

  /* ---- Year ---- */
  document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
})();
