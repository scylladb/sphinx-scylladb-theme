export class SidebarHandler {

  calculateScrollOffset(element1Selector, element2Selector) {
    const element1 = document.querySelector(element1Selector);
    const element2 = document.querySelector(element2Selector);
    const element1Height = element1 ? element1.offsetHeight : 0;
    const element2Height = element2 ? element2.offsetHeight : 0;
    return element1Height + element2Height;
  }

  onLoadScrollToCurrentPosition() {
    const selectedItem = document.querySelector('.sidebar-left .current-page');
  
    if (selectedItem) {
      const selectedItemPosition = selectedItem.getBoundingClientRect();
      if (selectedItemPosition.top < 0 || selectedItemPosition.top > window.innerHeight) {
        setTimeout(() => {
          selectedItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }, 100);
      }
    }
  }
  
  adjustSidebarHeightFooter() {
    if ($(window).innerWidth() >= 1024) {
      const headerOffset = this.calculateScrollOffset('.header', '.promo-banner');
      const footer = document.querySelector('.footer');
      const sidebar = document.querySelector('.side-nav');
      const secondarySidebar = document.querySelector('.secondary-side-nav');
      if (footer && sidebar && secondarySidebar) {
        const footerRect = footer.getBoundingClientRect();
        const visibleFooterHeight = footerRect.top > $(window).innerHeight() ? 0 : $(window).innerHeight() - footerRect.top;
        const offset = headerOffset + visibleFooterHeight;

        if (visibleFooterHeight > 0 && footerRect.top < $(window).innerHeight()) {
          sidebar.style.height = `calc(100vh - ${offset}px)`;
          secondarySidebar.style.height = `calc(100vh - ${offset}px)`;
        } else {
          sidebar.style.height = '100vh';
          secondarySidebar.style.height = '100vh';
        }
      }
    } else {
      const sidebar = document.querySelector('.side-nav');
      const secondarySidebar = document.querySelector('.secondary-side-nav');
      if (sidebar) {
        sidebar.style.removeProperty('height');
        secondarySidebar.style.removeProperty('height');
      }
    }
  }
  
  init() {
    this.onLoadScrollToCurrentPosition();

    const adjustForDesktopView = () => {
      this.adjustSidebarHeightFooter();
    };

    $(window).scroll(adjustForDesktopView);
    $(window).resize(adjustForDesktopView);
  }
}