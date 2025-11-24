export class SidebarHandler {

  constructor() {
    this.localStorageKey = "scylladb-docs-sidebar-scroll-position";
  }

  initScrollEvent() {
    const sideNavContent = $('#side-nav .side-nav-content');
    sideNavContent.on('scroll', () => {
      const scrollPosition = sideNavContent.scrollTop();
      localStorage.setItem(this.localStorageKey, scrollPosition);
    });
  }

  onLoadRestoreScrollPosition() {
    const sideNavContent = $('#side-nav .side-nav-content');
    const savedPosition = localStorage.getItem(this.localStorageKey);
    if (savedPosition) {
      sideNavContent.scrollTop(savedPosition);
    }
  }

  initHamburgerToggle() {
    const hamburger = $('.side-nav-toggle__button');
    const sideNav = $('#side-nav');

    hamburger.on('click', function(e) {
      e.preventDefault();
      e.stopPropagation();
      sideNav.toggleClass('show');
    });
  }

  handleResize() {
    const sideNav = $('#side-nav');
    const mediaQuery = window.matchMedia('(min-width: 1024px)');

    const checkResize = (e) => {
      if (e.matches) {
        // Desktop view - remove the show class
        sideNav.removeClass('show');
      }
    };

    // Check on load
    checkResize(mediaQuery);

    // Listen for changes
    mediaQuery.addListener(checkResize);
  }

  init() {
    this.initScrollEvent();
    this.onLoadRestoreScrollPosition();
    this.initHamburgerToggle();
    this.handleResize();
  }
}
