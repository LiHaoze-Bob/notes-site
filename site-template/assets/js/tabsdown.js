(() => {
  const directChild = (element, className) =>
    Array.from(element.children).find((child) => child.classList.contains(className));

  document.querySelectorAll('[data-tabsdown-site]').forEach((root) => {
    if (root.classList.contains('tabsdown-site--enhanced')) return;
    const tablist = directChild(root, 'tabsdown-site__tablist');
    const panelsRoot = directChild(root, 'tabsdown-site__panels');
    if (!tablist || !panelsRoot) return;
    const tabs = Array.from(tablist.children).filter((item) => item.classList.contains('tabsdown-site__tab'));
    const panels = Array.from(panelsRoot.children).filter((item) => item.classList.contains('tabsdown-site__panel'));
    if (tabs.length < 2 || tabs.length !== panels.length) return;

    tablist.setAttribute('role', 'tablist');
    tablist.setAttribute('aria-orientation',
      root.classList.contains('tabsdown-site--left') || root.classList.contains('tabsdown-site--right')
        ? 'vertical' : 'horizontal');

    const select = (index, focus = false) => {
      tabs.forEach((tab, position) => {
        const active = position === index;
        tab.setAttribute('role', 'tab');
        tab.setAttribute('aria-selected', String(active));
        tab.tabIndex = active ? 0 : -1;
        panels[position].setAttribute('role', 'tabpanel');
        panels[position].hidden = !active;
      });
      if (focus) tabs[index].focus();
    };

    tabs.forEach((tab, index) => {
      tab.addEventListener('click', () => select(index));
      tab.addEventListener('keydown', (event) => {
        let next;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = tabs.length - 1;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
        if (next === undefined) return;
        event.preventDefault();
        select(next, true);
      });
    });
    root.classList.add('tabsdown-site--enhanced');
    select(Math.max(0, tabs.findIndex((tab) => tab.getAttribute('aria-selected') === 'true')));
  });
})();
