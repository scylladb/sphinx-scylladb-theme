import Cookies from 'js-cookie';

export class DarkTheme {

    constructor() {
        this.cookieKey = "scylladb-docs-dark-theme";
        this.darkThemeClass = "dark";
        const isLocalHost = ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname);
        this.cookieOptions = {
            expires: 365,
            path: '/',
            ...(isLocalHost ? {} : { domain: '.scylladb.com' })
        };
        this.rootDocumentEl = $("html");
        this.darkThemeTogglerEl = $(".dark-theme-toggler");
    }

    getInitialState() {
        let state = Cookies.get(this.cookieKey);

        if (state === undefined) {
            return window.matchMedia('(prefers-color-scheme: dark)').matches;
        }
        return (state === 'true');
    }

    applyTheme(state) {
        if (state) {
            this.rootDocumentEl.addClass(this.darkThemeClass);
        } else {
            this.rootDocumentEl.removeClass(this.darkThemeClass);
        }
        this.rootDocumentEl.attr("data-theme", state ? "dark" : "light");
        this.rootDocumentEl.css("visibility","");
    }

    saveThemeState(state) {
        Cookies.set(this.cookieKey, state, this.cookieOptions);
    }

    init() {
        let state = this.getInitialState();
        this.applyTheme(state);

        this.darkThemeTogglerEl.on('click', () => {
            state = !state;
            this.saveThemeState(state);
            this.applyTheme(state);
        });
    }
}
