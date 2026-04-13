import TurndownService from "turndown";
import { gfm } from "turndown-plugin-gfm";

/**
 * Page Actions: "Ask a question" button with dropdown next to the page title.
 * - Ask a question: opens the biel.ai chatbot
 * - Copy page as Markdown
 * - Open in ChatGPT (passes page URL)
 * - Open in Claude (passes page URL)
 */
export class PageActionsHandler {
  init() {
    // Don't show on landing pages
    if (document.querySelector(".landing")) return;

    const contentBody = document.querySelector(".content-body");
    if (!contentBody) return;

    const h1 = contentBody.querySelector("h1");
    if (!h1) return;

    const wrapper = document.createElement("div");
    wrapper.className = "page-actions-wrapper";

    const btnGroup = this._createButtonGroup();
    h1.parentNode.insertBefore(wrapper, h1);
    wrapper.appendChild(h1);
    wrapper.appendChild(btnGroup);

    this._bindEvents(btnGroup);
  }

  _createButtonGroup() {
    const group = document.createElement("div");
    group.className = "page-actions";

    const bielProject = document.querySelector("biel-search-button")?.getAttribute("project") || "";

    group.innerHTML = `
      <button class="page-actions__main" type="button">
        <i class="icon-copy"></i>
        <span>Copy page</span>
      </button>
      <button class="page-actions__toggle" type="button" aria-label="More actions" aria-expanded="false">
        <i class="icon-chevron-down"></i>
      </button>
      <div class="page-actions__dropdown" hidden>
        <biel-button class="page-actions__item page-actions__ask-ai"
          project="${bielProject}"
          header-title="ScyllaDB chatbot (beta)"
          button-position="default"
          modal-position="sidebar-right"
          button-style="default"
          hide-icon="true">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"></path><rect width="16" height="12" x="4" y="8" rx="2"></rect><path d="M2 14h2"></path><path d="M20 14h2"></path><path d="M15 13v2"></path><path d="M9 13v2"></path></svg>
          Ask a question
        </biel-button>
        <a class="page-actions__item" data-action="open-chatgpt" href="#" target="_blank" rel="noopener">
          <i class="icon-scale-up"></i>
          <span>Open in ChatGPT</span>
        </a>
        <a class="page-actions__item" data-action="open-claude" href="#" target="_blank" rel="noopener">
          <i class="icon-scale-up"></i>
          <span>Open in Claude</span>
        </a>
      </div>
    `;

    // Prepend "View source" link via DOM (avoid HTML injection from attribute)
    const contentBody = document.querySelector(".content-body");
    const viewSourceUrl = contentBody?.getAttribute("data-view-source-url");
    if (viewSourceUrl) {
      const dropdown = group.querySelector(".page-actions__dropdown");
      const link = document.createElement("a");
      link.className = "page-actions__item";
      link.href = viewSourceUrl;
      link.target = "_blank";
      link.rel = "noopener";
      const icon = document.createElement("i");
      icon.className = "icon-description";
      const label = document.createElement("span");
      label.textContent = "View source";
      link.appendChild(icon);
      link.appendChild(label);
      dropdown.insertBefore(link, dropdown.firstChild);
    }

    return group;
  }

  _bindEvents(group) {
    const mainBtn = group.querySelector(".page-actions__main");
    const toggleBtn = group.querySelector(".page-actions__toggle");
    const dropdown = group.querySelector(".page-actions__dropdown");

    mainBtn.addEventListener("click", () => this._copyPageAsMarkdown(mainBtn));

    toggleBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = !dropdown.hidden;
      this._closeDropdown(dropdown, toggleBtn);
      if (!isOpen) {
        dropdown.hidden = false;
        toggleBtn.setAttribute("aria-expanded", "true");
      }
    });

    document.addEventListener("click", (e) => {
      if (!group.contains(e.target)) {
        this._closeDropdown(dropdown, toggleBtn);
      }
    });

    const askAiBtn = group.querySelector(".page-actions__ask-ai");
    if (askAiBtn) {
      askAiBtn.addEventListener("click", () => {
        this._closeDropdown(dropdown, toggleBtn);
        this._populateChat();
      });
    }

    const viewSourceBtn = group.querySelector('[href*="/blob/"]');
    if (viewSourceBtn) {
      viewSourceBtn.addEventListener("click", () => {
        this._closeDropdown(dropdown, toggleBtn);
      });
    }

    group.querySelector('[data-action="open-chatgpt"]').addEventListener("click", (e) => {
      e.preventDefault();
      this._openInChatGPT();
      this._closeDropdown(dropdown, toggleBtn);
    });

    group.querySelector('[data-action="open-claude"]').addEventListener("click", (e) => {
      e.preventDefault();
      this._openInClaude();
      this._closeDropdown(dropdown, toggleBtn);
    });
  }

  _populateChat(attempt = 1) {
    const url = window.location.href;
    const msg = `I want to ask some questions about this page: ${url}`;
    const bots = document.querySelectorAll("biel-bot");
    for (const bot of bots) {
      if (!bot.shadowRoot) continue;
      const bi = bot.shadowRoot.querySelector("biel-input");
      if (!bi || !bi.shadowRoot) continue;
      const ta = bi.shadowRoot.querySelector("textarea");
      if (ta) {
        ta.value = msg;
        ta.dispatchEvent(new Event("input", { bubbles: true }));
        ta.focus();
        return;
      }
    }
    if (attempt < 20) {
      setTimeout(() => this._populateChat(attempt + 1), 500);
    }
  }

  _closeDropdown(dropdown, toggleBtn) {
    dropdown.hidden = true;
    toggleBtn.setAttribute("aria-expanded", "false");
  }

  _getPageMarkdown() {
    const contentBody = document.querySelector(".content-body");
    if (!contentBody) return "";

    const clone = contentBody.cloneNode(true);
    clone.querySelectorAll(".page-actions-wrapper .page-actions, .headerlink").forEach(el => el.remove());

    const turndown = new TurndownService({ headingStyle: "atx", codeBlockStyle: "fenced" });
    turndown.use(gfm);
    return turndown.turndown(clone.innerHTML).trim();
  }

  _copyPageAsMarkdown(btn) {
    const markdown = this._getPageMarkdown();
    navigator.clipboard.writeText(markdown).then(() => {
      const label = btn ? btn.querySelector("span") : null;
      if (label) {
        const original = label.textContent;
        label.textContent = "Copied!";
        setTimeout(() => { label.textContent = original; }, 2000);
      }
    });
  }

  _openInChatGPT() {
    const url = window.location.href;
    const prompt = encodeURIComponent("Read this documentation page: " + url + "\n\nI'll ask you some questions about it.");
    window.open("https://chat.openai.com/?q=" + prompt, "_blank");
  }

  _openInClaude() {
    const url = window.location.href;
    const prompt = encodeURIComponent("Read this documentation page: " + url + "\n\nI'll ask you some questions about it.");
    window.open("https://claude.ai/new?q=" + prompt, "_blank");
  }
}
