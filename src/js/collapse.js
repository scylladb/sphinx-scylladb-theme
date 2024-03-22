export class CollapseHandler {

	constructor() {
		this.localStorageKey = "scylla-docs-collapse-side-nav";
	}
	
	calculateCollapsibleNavigationButtonPosition() {
		const collapsibleButton = $(".collapsible-button");
		const footer = $(".footer");
		const offset = 10;
		const footerOffset = footer.offset();
		const footerTop = footerOffset.top;
		const footerBottom = footerTop + footer.outerHeight();
		const screenBottom = $(window).scrollTop() + $(window).innerHeight();
		const screenTop = $(window).scrollTop();
		if (screenBottom > footerTop && screenTop < footerBottom) {
			collapsibleButton.css("bottom", screenBottom - footerTop + offset);
		} else {
			collapsibleButton.css("bottom", offset);
		}
	}

	collapseNavigation() {
		new Foundation.Tooltip($(".collapsible-button"), {
			position: "top",
			tipText: "Expand",
		});
		localStorage.setItem(this.localStorageKey, "1");
		$("#side-nav").addClass("side-nav--collapsed");
		$(".content").addClass("content--collapsed");
	}

	expandNavigation() {
		new Foundation.Tooltip($(".collapsible-button"), {
			position: "top",
			tipText: "Collapse",
		});
		localStorage.setItem(this.localStorageKey, "0");
		$("#side-nav").removeClass("side-nav--collapsed");
		$(".content").removeClass("content--collapsed");
	}

	loadCollapsibleNavigation() {
		if (localStorage.getItem(this.localStorageKey) == "1") {
			this.collapseNavigation();
		} else {
			this.expandNavigation();
		}
		this.calculateCollapsibleNavigationButtonPosition();
	}

	onClickCollapsibleNavigationButton() {
		$(".collapsible-button").on("click", () => {
			$(".collapsible-button").foundation("destroy");
			if ($("#side-nav").hasClass("side-nav--collapsed")) {
				this.expandNavigation();
			} else {
				this.collapseNavigation();
			}
			this.calculateCollapsibleNavigationButtonPosition();
		});
	}

	onScrollCollapsibleNavigation() {
		$(window).scroll(() => {
			this.calculateCollapsibleNavigationButtonPosition();
		});
	}

	init() {
		this.loadCollapsibleNavigation();
		this.onClickCollapsibleNavigationButton();
		this.onScrollCollapsibleNavigation();
	}
}