/* Progressive enhancement. All project content and links work without JS. */
(() => {
  'use strict';
  document.body.classList.add('js');
  document.querySelectorAll('[data-js-only]').forEach(el => { el.hidden = false; });

  const menu = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('.nav-links');
  const closeMenu = () => {
    menu?.setAttribute('aria-expanded', 'false');
    navigation?.classList.remove('is-open');
  };
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu?.getAttribute('aria-expanded') === 'true') {
      closeMenu(); menu.focus();
    }
  });
  document.addEventListener('click', event => {
    if (menu && !event.target.closest('.navigation')) closeMenu();
  });
  navigation?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  matchMedia('(min-width: 521px)').addEventListener('change', closeMenu);

  const tabs = [...document.querySelectorAll('.project-tabs [role="tab"]')];
  function selectTab(index, focus = false) {
    tabs.forEach((tab, i) => {
      const selected = i === index;
      tab.setAttribute('aria-selected', String(selected)); tab.tabIndex = selected ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) tabs[index].focus();
  }
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => selectTab(i));
    tab.addEventListener('keydown', event => {
      let next = i;
      if (event.key === 'ArrowRight') next = (i + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (i + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault(); selectTab(next, true);
    });
  });

  const search = document.getElementById('project-search');
  if (search) {
    const rows = [...document.querySelectorAll('[data-project]')];
    const filters = [...document.querySelectorAll('[data-filter]')];
    const count = document.getElementById('result-count');
    const empty = document.querySelector('.empty-state');
    const params = new URLSearchParams(location.search);
    let active = params.get('discipline') || 'all';
    if (!filters.some(b => b.dataset.filter === active)) active = 'all';
    search.value = params.get('q') || '';
    const normalize = value => value.toLocaleLowerCase('en').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    function update(writeURL = true) {
      const terms = normalize(search.value).trim().split(/\s+/).filter(Boolean);
      let visible = 0;
      rows.forEach(row => {
        const match = (active === 'all' || JSON.parse(row.dataset.disciplines).includes(active)) && terms.every(term => normalize(row.dataset.search).includes(term));
        row.hidden = !match; if (match) visible++;
      });
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === active)));
      count.textContent = `${String(visible).padStart(2, '0')} ${visible === 1 ? 'study' : 'studies'}${visible !== rows.length ? ` / ${rows.length} selected` : ' selected'}`;
      empty.hidden = visible !== 0;
      if (writeURL && location.protocol !== 'file:') {
        const url = new URL(location.href);
        if (search.value.trim()) url.searchParams.set('q', search.value.trim()); else url.searchParams.delete('q');
        if (active !== 'all') url.searchParams.set('discipline', active); else url.searchParams.delete('discipline');
        history.replaceState(null, '', url);
      }
    }
    filters.forEach(button => button.addEventListener('click', () => { active = button.dataset.filter; update(); }));
    search.addEventListener('input', () => update());
    document.getElementById('clear-filters').addEventListener('click', () => { active = 'all'; search.value = ''; update(); search.focus(); });
    update(false);
  }

  const tocLinks = [...document.querySelectorAll('.desktop-toc a')];
  const headings = tocLinks.map(a => document.getElementById(a.hash.slice(1))).filter(Boolean);
  if (headings.length && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      const visible = entries.filter(e => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (!visible.length) return;
      tocLinks.forEach(a => { if (a.hash === '#' + visible[0].target.id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    }, { rootMargin: '-5% 0px -65% 0px' });
    headings.forEach(h => observer.observe(h));
  }
  document.querySelectorAll('.mobile-toc a').forEach(a => a.addEventListener('click', () => { a.closest('details').open = false; }));

  const dialog = document.querySelector('.lightbox');
  if (dialog && typeof dialog.showModal === 'function') {
    let trigger;
    document.querySelectorAll('.image-zoom').forEach(link => link.addEventListener('click', event => {
      event.preventDefault(); trigger = link;
      const image = link.querySelector('img');
      dialog.querySelector('img').src = image.src;
      dialog.querySelector('img').alt = image.alt;
      dialog.querySelector('p').textContent = link.closest('figure').querySelector('figcaption')?.textContent || image.alt;
      dialog.showModal();
    }));
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => trigger?.focus());
  }

  document.querySelectorAll('.prose pre').forEach(pre => {
    if (!navigator.clipboard) return;
    const button = document.createElement('button'); button.type = 'button'; button.className = 'copy-code'; button.textContent = 'Copy code';
    button.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(pre.querySelector('code').textContent); button.textContent = 'Copied'; }
      catch { button.textContent = 'Select text to copy'; }
      setTimeout(() => { button.textContent = 'Copy code'; }, 1800);
    });
    pre.append(button);
  });
})();
