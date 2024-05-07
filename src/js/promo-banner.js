export class PromoBannerHandler {

	constructor() {
		this.localStorageKey = "scylladb-docs-hide-banner";
	}

	setItemWithExpiry(key, value, days) {
		const now = new Date();
		const ttl = days * 24 * 60 * 60 * 1000;
		const item = {
			value: value,
			expiry: now.getTime() + ttl,
		};
		localStorage.setItem(key, JSON.stringify(item));
	}

	getItemWithExpiry(key) {
		const itemStr = localStorage.getItem(key);
		if (!itemStr) {
			return null;
		}
		const item = JSON.parse(itemStr);
		const now = new Date();

		if (now.getTime() > item.expiry) {
			localStorage.removeItem(key);
			return null;
		}
		return item.value;
	}


	adjustScrollPaddingTop() {
		const headerHeight = $('.header').outerHeight() || 0;
		let promoBannerHeight = 0;
		if ($('.promo-banner').is(':visible')) {
			promoBannerHeight = $('.promo-banner').outerHeight();
		}
		const offset = 10;
		const totalHeight = headerHeight + promoBannerHeight + offset;
		$('html').css('scroll-padding-top', totalHeight + 'px');
	}

	initBanner() {
		const promoBanner = $(".promo-banner");
		const promoBannerHeight = promoBanner.outerHeight();
		let showBanner = false;

		const hideBanner = $('meta[name="scylladb-docs-hide_banner"]').attr('content');
		if (hideBanner && hideBanner === "false") {
			// The banner is enabled via the site metadata (e.g. Google Tag Manager)
			const bannerTitleText = $('meta[name="scylladb-docs-banner_title_text"]').attr('content');
			const bannerButtonText = $('meta[name="scylladb-docs-banner_button_text"]').attr('content');
			const bannerButtonUrl = $('meta[name="scylladb-docs-banner_button_url"]').attr('content');
			$(".promo-banner__title").text(bannerTitleText);
			$(".promo-banner__button").attr("href", bannerButtonUrl);
			$(".promo-banner__button").text(bannerButtonText);
			showBanner = true;
		} else if (!promoBanner.hasClass("promo-banner--hide")) {
			// The banner is enabled via conf.py and not hidden
			showBanner = true;
		}

		// The banner should be shown, but the user has already closed it
		if (showBanner && this.getItemWithExpiry(this.localStorageKey)) {
			showBanner = false;
		}

		if (showBanner) {
			promoBanner.show();
			$("body").css("margin-top", promoBannerHeight);
			$(".side-nav").css("margin-top", promoBannerHeight);
			$(".secondary-side-nav").css("margin-top", promoBannerHeight);
			$(".layout").addClass("layout--has-banner");
		}
		this.adjustScrollPaddingTop();
	}

	onChangeMetaBanner() {
		var targetNode = document;

		const observer = new MutationObserver((mutations) => {
			mutations.forEach((mutation) => {
				if (mutation.type === 'childList') {
					for (const addedNode of mutation.addedNodes) {
						if (addedNode.nodeName === 'META' && addedNode.name === 'scylladb-docs-hide_banner') {
							this.initBanner();
							observer.disconnect();
						}
					}
				}
			});
		});

		const config = {
			childList: true,
			subtree: true
		};

		observer.observe(targetNode, config);
	}

	onCloseBanner() {
		$(".promo-banner__close").on("click", () => {
			this.setItemWithExpiry(this.localStorageKey, "1", 30);
			$("body").css("margin-top", 0);
			$(".side-nav").css("margin-top", 0);
			$(".secondary-side-nav").css("margin-top", 0);
			$(".promo-banner").hide();
			$(".layout").removeClass("layout--has-banner");
			this.adjustScrollPaddingTop();
		});
	}

	onResizeBanner() {
		$(window).resize(() => {
			const promoBanner = $(".promo-banner");
			const promoBannerHeight = promoBanner.outerHeight();
			if (promoBanner.is(":visible")) {
				$("body").css("margin-top", promoBannerHeight);
				$(".side-nav").css("margin-top", promoBannerHeight);
				$(".secondary-side-nav").css("margin-top", promoBannerHeight);
			}
			this.adjustScrollPaddingTop();
		});
	}

	init() {
		this.initBanner();
		this.onChangeMetaBanner();
		this.onCloseBanner();
		this.onResizeBanner();
	}
}