export class SidebarHandler {

  constructor() {
    this.localStorageKey = "scylladb-docs-sidebar-scroll-position";
  }
  
  initScrollEvent() {
    const sideNavContent = $('#side-nav .side-nav-content');
    sideNavContent.on('scroll', () => {
      const scrollPosition = sideNavContent.scrollTop();
      localStorage.setItem(this.localStorageKey, scrollPosition);
      console.log('scrollPosition', scrollPosition);
    });
  }

  onLoadRestoreScrollPosition() {
    const sideNavContent = $('#side-nav .side-nav-content');
    const savedPosition = localStorage.getItem(this.localStorageKey);
    console.log('savedPosition', savedPosition);
    if (savedPosition) {
      sideNavContent.scrollTop(savedPosition);
    }
    // $('.side-nav-content').css('visibility', 'visible');
  }

    
  init() {
    this.initScrollEvent();
    this.onLoadRestoreScrollPosition();
  }
}
