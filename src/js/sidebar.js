export class SidebarHandler {

  constructor() {
    this.localStorageKey = "scylladb-docs-sidebar-scroll-position";
  }
  
  initScrollEvent() {
    $('#side-nav').scroll(() => {
      const scrollPosition = $('#side-nav').scrollTop();
      localStorage.setItem(this.localStorageKey, scrollPosition);
    });
  }

  onLoadRestoreScrollPosition() {
    const savedPosition = localStorage.getItem(this.localStorageKey);
    if (savedPosition) {
      $('#side-nav').scrollTop(savedPosition);
    }
    $('.side-nav-content').css('visibility', 'visible');
  }

  calculateScrollOffset(selectors) {
    let totalHeight = 0;
  
    selectors.forEach(selector => {
      const element = document.querySelector(selector);
      if (element) {
        totalHeight += element.offsetHeight;
      }
    });
    return totalHeight;
  }
  
  adjustSidebarHeightFooter() {
    const sidebar = document.querySelector('.side-nav');
    const secondarySidebar = document.querySelector('.secondary-side-nav');
    if ($(window).innerWidth() >= 1024) {
      const windowHeight =  $(window).innerHeight();
      const headerOffset = this.calculateScrollOffset(['.header', '.promo-banner']);
      const footerTop = document.querySelector('.footer').getBoundingClientRect().top;
      const visibleFooterHeight = footerTop > windowHeight ? 0 : windowHeight - footerTop;
      const offset = headerOffset + visibleFooterHeight;
      if (visibleFooterHeight > 0 && footerTop < windowHeight) {
        sidebar.style.height = `calc(100vh - ${offset}px)`;
        secondarySidebar.style.height = `calc(100vh - ${offset}px)`;
      } else {
        sidebar.style.height = '100vh';
        secondarySidebar.style.height = '100vh';
      }
    } else {
      sidebar.style.removeProperty('height');
      secondarySidebar.style.removeProperty('height');
    }
  }
  
  init() {
    this.initScrollEvent();
    this.onLoadRestoreScrollPosition();

    const adjustForDesktopView = () => {
      this.adjustSidebarHeightFooter();
    };

    $(window).scroll(adjustForDesktopView);
    $(window).resize(adjustForDesktopView);
  }
}
