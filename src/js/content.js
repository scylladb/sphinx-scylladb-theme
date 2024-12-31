export class ContentHandler {

    constructor() {}

    createTooltip(link) {
        const tooltip = document.createElement('span');
        tooltip.classList.add('tooltip');
        tooltip.textContent = 'Copy';
        link.appendChild(tooltip);
    }

    addHoverEvents(link) {
        const tooltip = link.querySelector('.tooltip');
        link.addEventListener('mouseenter', () => {
            tooltip.style.visibility = 'visible';
        });
        link.addEventListener('mouseleave', () => {
            tooltip.style.visibility = 'hidden';
        });
    }

    getFormattedURL(href) {
        const url = new URL(href);
        const formattedURL = `${url.origin}${url.pathname.split('/').slice(0, -1).join('/')}${url.hash}`;
        return formattedURL;
    }

    addClickEvent(link) {
        const tooltip = link.querySelector('.tooltip');
        link.addEventListener('click', () => {
            navigator.clipboard.writeText(this.getFormattedURL(link.href))
                .then(() => {
                    tooltip.textContent = 'Copied!';
                    setTimeout(() => {
                        tooltip.textContent = 'Copy';
                    }, 1000);
                })
                .catch(err => console.error('Failed to copy text: ', err));
        });
    }

    init() {
        const headerLinks = document.querySelectorAll('.headerlink');
        headerLinks.forEach(link => {
            link.innerHTML = '<i class="icon-link"></i>';
            this.createTooltip(link);
            this.addHoverEvents(link);
            this.addClickEvent(link);
        });
    }
}
