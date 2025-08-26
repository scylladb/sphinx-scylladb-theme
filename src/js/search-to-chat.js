/**
 * Handles prepopulating Ask AI chat with search input
 */
export class SearchToChatHandler {
  init() {
    document.addEventListener('DOMContentLoaded', () => {
      this.setupListeners();
    });
    
    setTimeout(() => {
      this.setupListeners();
    }, 1000);
  }

  setupListeners() {
    const askAiButtons = document.querySelectorAll('biel-button');
    
    askAiButtons.forEach(button => {
      button.addEventListener('click', () => {
        const searchValue = this.getSearchValue();
        if (searchValue) {
          setTimeout(() => {
            this.populateChat(searchValue);
          }, 1000);
        }
      });
    });
  }

  getSearchValue() {
    const input = document.querySelector('.er_search_input_dummy');
    return input && input.value.trim() ? input.value.trim() : null;
  }

  populateChat(searchText, attempt = 1) {
    const bielBot = document.querySelector('biel-bot');
    
    if (bielBot && bielBot.shadowRoot) {
      const bielInput = bielBot.shadowRoot.querySelector('biel-input');
      
      if (bielInput && bielInput.shadowRoot) {
        const textarea = bielInput.shadowRoot.querySelector('.biel-input__textarea');
        
        if (textarea) {
          textarea.value = `I was searching for: "${searchText}". Can you help me with this?`;
          textarea.dispatchEvent(new Event('input', { bubbles: true }));
          textarea.focus();
          return;
        }
      }
    }
    
    if (attempt < 3) {
      setTimeout(() => this.populateChat(searchText, attempt + 1), 500);
    }
  }
} 