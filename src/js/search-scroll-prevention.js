export class SearchScrollPrevention {
  constructor() {
    this.isSearchFocused = false;
    this.originalScrollPaddingTop = null;
    this.searchSelectors = [
      'ci-search input',
      '.er-dummy-search input',
      '.er-dummy-search-box input', 
      '.er-search-form input',
      'input[class*="er_search"]',
      'input[aria-label*="search" i]',
      '.er_search_input_dummy'
    ];
  }

  preventScrollToElement() {
    // Override scrollIntoView globally while search is focused
    const originalScrollIntoView = Element.prototype.scrollIntoView;
    Element.prototype.scrollIntoView = function(options) {
      // If a search element is focused, ignore scrollIntoView calls
      if (this.closest && this.closest('.search-box, .header-search-box, ci-search, .er-dummy-search')) {
        return;
      }
      return originalScrollIntoView.call(this, options);
    };
    
    return originalScrollIntoView;
  }

  restoreScrollIntoView(originalMethod) {
    Element.prototype.scrollIntoView = originalMethod;
  }

  isSearchInput(target) {
    return this.searchSelectors.some(selector => 
      target.matches && target.matches(selector)
    );
  }

  isInSearchContainer(target) {
    return target.closest('.search-box, .header-search-box, ci-search, .er-dummy-search');
  }

  handleFocusIn(event, originalScrollIntoViewRef) {
    const target = event.target;
    const isSearchInput = this.isSearchInput(target);
    const isInSearchContainer = this.isInSearchContainer(target);
    
    if (isSearchInput || (isInSearchContainer && target.tagName === 'INPUT')) {
      this.isSearchFocused = true;
      
      // Remove scroll-padding-top temporarily
      $('html').css('scroll-padding-top', '0px');
      
      // Override scrollIntoView to prevent any scrolling
      if (!originalScrollIntoViewRef.current) {
        originalScrollIntoViewRef.current = this.preventScrollToElement();
      }
    }
  }

  handleFocusOut(event, originalScrollIntoViewRef) {
    const target = event.target;
    const isInSearchContainer = this.isInSearchContainer(target);
    
    if (isInSearchContainer && target.tagName === 'INPUT') {
      // Small delay to allow new focus to register
      setTimeout(() => {
        const newFocusedElement = document.activeElement;
        const newIsSearchFocused = newFocusedElement && 
          this.isInSearchContainer(newFocusedElement);
        
        if (!newIsSearchFocused) {
          this.isSearchFocused = false;
          
          // Restore scroll-padding-top
          if (this.originalScrollPaddingTop) {
            $('html').css('scroll-padding-top', this.originalScrollPaddingTop);
          }
          
          // Restore scrollIntoView
          if (originalScrollIntoViewRef.current) {
            this.restoreScrollIntoView(originalScrollIntoViewRef.current);
            originalScrollIntoViewRef.current = null;
          }
        }
      }, 10);
    }
  }

  createScrollPreventionHandler() {
    let isPreventingScroll = false;
    
    return () => {
      if (this.isSearchFocused && !isPreventingScroll) {
        isPreventingScroll = true;
        const currentScrollY = window.scrollY;
        
        requestAnimationFrame(() => {
          if (window.scrollY !== currentScrollY) {
            window.scrollTo(0, currentScrollY);
          }
          isPreventingScroll = false;
        });
      }
    };
  }

  handleSearchSuggestionsDisplay() {
    // Observer to detect when search suggestions appear
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        mutation.addedNodes.forEach((node) => {
          if (node.nodeType === Node.ELEMENT_NODE) {
            // Check if it's a search suggestions container
            const suggestions = node.querySelector && node.querySelector('.er_search_suggestions');
            if (suggestions) {
              this.updateSuggestionsClasses(suggestions);
            }
            
            // Also check if the node itself is suggestions container
            if (node.classList && node.classList.contains('er_search_suggestions')) {
              this.updateSuggestionsClasses(node);
            }
          }
        });
        
        // Check for changes in existing suggestions
        if (mutation.target.classList && mutation.target.classList.contains('er_search_suggestions')) {
          this.updateSuggestionsClasses(mutation.target);
        }
      });
    });

    observer.observe(document.body, { 
      childList: true, 
      subtree: true,
      attributes: false
    });

    // Also check existing suggestions on page load
    setTimeout(() => {
      document.querySelectorAll('.er_search_suggestions').forEach(suggestions => {
        this.updateSuggestionsClasses(suggestions);
      });
    }, 100);
  }

  updateSuggestionsClasses(suggestionsContainer) {
    const children = Array.from(suggestionsContainer.children);
    const hasOnlyH3 = children.length === 1 && children[0].tagName === 'H3';
    
    if (hasOnlyH3) {
      suggestionsContainer.classList.add('er-no-results');
    } else {
      suggestionsContainer.classList.remove('er-no-results');
    }
  }

  init() {
    // Store original scroll-padding-top
    this.originalScrollPaddingTop = $('html').css('scroll-padding-top');
    
    // Use a ref-like object to store the original scrollIntoView method
    const originalScrollIntoViewRef = { current: null };

    // Prevent scrolling when focusing on search elements
    document.addEventListener('focusin', (event) => {
      this.handleFocusIn(event, originalScrollIntoViewRef);
    }, true); // Use capture phase to catch events early

    // Restore normal behavior when leaving search elements
    document.addEventListener('focusout', (event) => {
      this.handleFocusOut(event, originalScrollIntoViewRef);
    });

    // Monitor for any scroll attempts and prevent them
    const preventScroll = this.createScrollPreventionHandler();
    window.addEventListener('scroll', preventScroll, { passive: true });
    
    // Handle search suggestions display styling
    this.handleSearchSuggestionsDisplay();
  }
} 