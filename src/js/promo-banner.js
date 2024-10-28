import Cookies from 'js-cookie';

export class PromoBannerHandler {

    constructor() {
        this.cookieKey = "scylladb-docs-hide-banner";
        const isLocalHost = ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname);
        this.cookieOptions = {
            expires: 30,
            path: '/',
            ...(isLocalHost ? {} : { domain: '.scylladb.com' })
        };

    }

    setCookieWithExpiry(key, value, days) {
        Cookies.set(key, value, { expires: days, path: '/' });
    }

    getCookieWithExpiry(key) {
        return Cookies.get(key) || null;
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

            // The banner is enabled via the site metadata (e.g. Google Tag Manager)
        const hideBannerMeta = $('meta[name="scylladb-docs-hide_banner"]').attr('content');
        if (hideBannerMeta && hideBannerMeta === "false") {
            this.setBannerContent();
            showBanner = true;
        } else if (!promoBanner.hasClass("promo-banner--hide")) {
			// The banner is enabled via conf.py and not hidden
            showBanner = true;
        }

        // The banner should be shown, but the user has already closed it
        if (showBanner && this.getCookieWithExpiry(this.cookieKey)) {
            showBanner = false;
        }

        if (showBanner) {
            this.showBanner(promoBannerHeight);
        }

        this.adjustScrollPaddingTop();
    }

    setBannerContent() {
        const bannerTitleText = $('meta[name="scylladb-docs-banner_title_text"]').attr('content');
        const bannerButtonText = $('meta[name="scylladb-docs-banner_button_text"]').attr('content');
        const bannerButtonUrl = $('meta[name="scylladb-docs-banner_button_url"]').attr('content');

        $(".promo-banner__title").text(bannerTitleText);
        $(".promo-banner__button").attr("href", bannerButtonUrl).text(bannerButtonText);
    }

    showBanner(promoBannerHeight) {
        const promoBanner = $(".promo-banner");
        promoBanner.show();
        $("body").css("margin-top", promoBannerHeight);
        $(".side-nav, .secondary-side-nav").css("margin-top", promoBannerHeight);
        $(".layout").addClass("layout--has-banner");
    }

    onChangeMetaBanner() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                mutation.addedNodes.forEach((node) => {
                    if (node.nodeName === 'META' && node.name === 'scylladb-docs-hide_banner') {
                        this.initBanner();
                        observer.disconnect();
                    }
                });
            });
        });

        const config = { childList: true, subtree: true };
        observer.observe(document, config);
    }

    onCloseBanner() {
        $(".promo-banner__close").on("click", () => {
            this.setCookieWithExpiry(this.cookieKey, "1", 30);
            this.hideBanner();
        });
    }

    hideBanner() {
        $(".promo-banner").hide();
        $("body, .side-nav, .secondary-side-nav").css("margin-top", 0);
        $(".layout").removeClass("layout--has-banner");
        this.adjustScrollPaddingTop();
    }

    onResizeBanner() {
        $(window).resize(() => {
            const promoBanner = $(".promo-banner");
            const promoBannerHeight = promoBanner.outerHeight();
            if (promoBanner.is(":visible")) {
                $("body, .side-nav, .secondary-side-nav").css("margin-top", promoBannerHeight);
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
