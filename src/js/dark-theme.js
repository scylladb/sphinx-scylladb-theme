export class DarkTheme {


    init() {
        let state = localStorage.getItem('dark-theme') === 'true';
        let rootDocumentEl = $("html");
        let darkThemeTogglerEl = $(".dark-theme-toggler");


        const toggler = (state) => {
            if (state) {
                rootDocumentEl.addClass('dark')
            } else {
                rootDocumentEl.removeClass('dark')
            }
        }

        toggler(state);


        darkThemeTogglerEl.on('click', () => {
            state = !state;
            localStorage.setItem('dark-theme', state);
            toggler(state)
        });
    }

}