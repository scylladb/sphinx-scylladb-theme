import Cookies from 'js-cookie';

export class CollapseHandler {

    constructor() {
        this.cookieKey = "scylladb-docs-collapse-side-nav";
        const isLocalHost = ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname);
        this.cookieOptions = {
            expires: 365,
            path: '/',
            ...(isLocalHost ? {} : { domain: '.scylladb.com' })
        };
    }

    collapseNavigation() {
        new Foundation.Tooltip($(".collapsible-button"), {
            position: "top",
            tipText: "Expand",
        });
        Cookies.set(this.cookieKey, "1", this.cookieOptions);
        $("#side-nav").addClass("side-nav--collapsed");
        $(".content").addClass("content--collapsed");
    }

    expandNavigation() {
        new Foundation.Tooltip($(".collapsible-button"), {
            position: "top",
            tipText: "Collapse",
        });
        Cookies.set(this.cookieKey, "0", this.cookieOptions);
        $("#side-nav").removeClass("side-nav--collapsed");
        $(".content").removeClass("content--collapsed");
    }

    loadCollapsibleNavigation() {
        const collapseState = Cookies.get(this.cookieKey);
        if (collapseState === "1") {
            this.collapseNavigation();
        } else {
            this.expandNavigation();
        }        
    }

    onClickCollapsibleNavigationButton() {
        $(".collapsible-button").on("click", () => {
            $(".collapsible-button").foundation("destroy");
            if ($("#side-nav").hasClass("side-nav--collapsed")) {
                this.expandNavigation();
            } else {
                this.collapseNavigation();
            }
        });
    }

    init() {
        this.loadCollapsibleNavigation();
        this.onClickCollapsibleNavigationButton();
    }
}
