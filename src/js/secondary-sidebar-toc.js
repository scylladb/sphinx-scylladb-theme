export class SecondarySidebarTOC {
  constructor() {
    this.toc = document.querySelector('.secondary-side-nav__content ul');
    this.headers = [];
    this.tocItems = [];
  }

  init() {
    if (!this.toc) return;

    const content = document.querySelector('.content-body') ||
                    document.querySelector('.body-container') ||
                    document.querySelector('section[role="main"]') ||
                    document.querySelector('main');

    if (!content) return;

    const sections = Array.from(content.querySelectorAll('section[id]'));
    this.headers = sections.map(section => {
      const heading = section.querySelector('h1, h2, h3, h4, h5, h6');
      if (heading) {
        const level = parseInt(heading.tagName.charAt(1));
        if (level === 1) return null;

        return {
          id: section.id,
          element: section,
          level: level
        };
      }
      return null;
    }).filter(h => h !== null);

    const apiItems = Array.from(content.querySelectorAll('dt[id]'));
    apiItems.forEach(dt => {
      let parentSection = dt.closest('section[id]');
      let level = 4;

      // Check if this is a main API object (struct, class, function, etc.)
      // by checking if its parent is a direct child of the section
      const parentDl = dt.parentElement;
      const isMainApiObject = parentDl && parentSection && 
                              parentDl.parentElement === parentSection;

      if (parentSection) {
        const parentHeading = parentSection.querySelector('h1, h2, h3, h4, h5, h6');
        if (parentHeading) {
          const parentLevel = parseInt(parentHeading.tagName.charAt(1));
          // If this is the main API object under an h1, treat it as h2 level
          if (isMainApiObject && parentLevel === 1) {
            level = 2;
          } else {
            level = parentLevel + 1;
          }
        }
      }

      this.headers.push({
        id: dt.id,
        element: dt,
        level: Math.min(level, 4),
        parentSection: parentSection ? parentSection.id : null
      });
    });

    this.headers.sort((a, b) => {
      const aTop = a.element.getBoundingClientRect().top + window.scrollY;
      const bTop = b.element.getBoundingClientRect().top + window.scrollY;
      return aTop - bTop;
    });

    const tocLinks = Array.from(this.toc.querySelectorAll('a'));
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (!href || !href.includes('#')) return;

      const hash = '#' + href.split('#')[1];
      const li = link.closest('li');
      if (li) {
        this.tocItems.push({ hash, li, link });
      }
    });

    window.addEventListener('scroll', () => this.onScroll(), { passive: true });

    if (this.headers.length > 0 && window.scrollY < 200) {
      const firstH2 = this.headers.find(h => h.level === 2);
      if (firstH2) {
        const firstH2Item = this.tocItems.find(item => item.hash === '#' + firstH2.id);
        if (firstH2Item) {
          firstH2Item.li.classList.add('active');
        }
      }
    }

    setTimeout(() => this.onScroll(), 100);
  }

  onScroll() {
    const scrollPos = window.scrollY + 150;
    let currentHeader = null;

    for (let i = this.headers.length - 1; i >= 0; i--) {
      const headerTop = this.headers[i].element.getBoundingClientRect().top + window.scrollY;
      if (headerTop <= scrollPos) {
        currentHeader = this.headers[i];
        break;
      }
    }

    if (!currentHeader && this.headers.length > 0) {
      currentHeader = this.headers[0];
    }

    if (currentHeader) {
      this.updateTOC(currentHeader);
    }
  }

  updateTOC(currentHeader) {
    if (!currentHeader) return;

    // Clear all active/current states
    this.tocItems.forEach(item => {
      item.li.classList.remove('active', 'current');
    });

    // Find the level 2 parent for hierarchical navigation
    const h2Header = this.findParentH2(currentHeader);

    // Mark current item
    const currentItem = this.tocItems.find(item => item.hash === '#' + currentHeader.id);
    if (currentItem) {
      currentItem.li.classList.add('current');
      this.markParentLIsActive(currentItem.li);
    }

    // Mark h2 parent item
    const h2Item = this.tocItems.find(item => item.hash === '#' + h2Header.id);
    if (h2Item) {
      h2Item.li.classList.add('active');
      if (currentHeader === h2Header) {
        h2Item.li.classList.add('current');
      }
      this.markParentLIsActive(h2Item.li);
    }
  }

  findParentH2(currentHeader) {
    if (currentHeader.level <= 2) return currentHeader;

    const currentIndex = this.headers.indexOf(currentHeader);
    const parentSection = currentHeader.element.closest('section[id]');

    // For API docs (DT elements), find parent struct/class (also DT at level 2)
    if (currentHeader.element.tagName === 'DT') {
      for (let i = currentIndex - 1; i >= 0; i--) {
        const header = this.headers[i];
        if (header.level === 2 && header.element.tagName === 'DT') {
          const headerSection = header.element.closest('section[id]');
          if (headerSection === parentSection) {
            return header;
          }
        }
        if (header.level === 2 && header.element.tagName !== 'DT') break;
      }
    }

    // For regular content or fallback, find previous level 2 heading
    for (let i = currentIndex - 1; i >= 0; i--) {
      if (this.headers[i].level === 2) {
        return this.headers[i];
      }
    }

    return currentHeader;
  }

  markParentLIsActive(li) {
    let parent = li.parentElement;
    while (parent) {
      if (parent.tagName === 'LI') {
        parent.classList.add('active');
      }
      parent = parent.parentElement;
    }
  }
}

