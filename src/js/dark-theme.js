import Cookies from 'js-cookie';

export class DarkTheme {

    constructor() {
        this.cacheKey = "scylladb-docs-dark-theme";
        this.darkThemeClass = "dark";
        this.cookieOptions = {
            expires: 365,
            path: '/'
        };
        this.rootDocumentEl = $("html");
        this.darkThemeTogglerEl = $(".dark-theme-toggler");
    }

    getInitialState() {
        let state = Cookies.get(this.cacheKey);

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
    }

    saveThemeState(state) {
        Cookies.set(this.cacheKey, state, this.cookieOptions);
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
