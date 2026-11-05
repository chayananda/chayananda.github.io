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

  /* ---- Hologram credential cards ---- */
  document.querySelectorAll('.holo').forEach((card) => {
    let frame = 0;
    const MAX = 14; // degrees

    const apply = (x, y) => {
      // x, y in 0..1
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => {
        card.style.setProperty('--ry', `${(x - 0.5) * MAX * 2}deg`);
        card.style.setProperty('--rx', `${(0.5 - y) * MAX * 2}deg`);
        card.style.setProperty('--mx', `${x * 100}%`);
        card.style.setProperty('--my', `${y * 100}%`);
        card.style.setProperty('--o', '1');
      });
    };
    const reset = () => {
      cancelAnimationFrame(frame);
      card.classList.remove('is-active');
      card.style.setProperty('--rx', '0deg');
      card.style.setProperty('--ry', '0deg');
      card.style.setProperty('--mx', '50%');
      card.style.setProperty('--my', '50%');
      card.style.setProperty('--o', '0');
    };

    card.addEventListener('pointerenter', () => card.classList.add('is-active'));
    card.addEventListener('pointermove', (e) => {
      if (reduceMotion) return;
      const r = card.getBoundingClientRect();
      apply((e.clientX - r.left) / r.width, (e.clientY - r.top) / r.height);
    });
    card.addEventListener('pointerleave', reset);
    card.addEventListener('pointercancel', reset);

    // Keyboard: focus shows a gentle angled shine
    card.addEventListener('focus', () => { card.classList.add('is-active'); if (!reduceMotion) apply(0.72, 0.28); });
    card.addEventListener('blur', reset);
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
