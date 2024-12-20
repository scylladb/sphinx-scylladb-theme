export class ContentHandler {

    constructor() {
    }

    init() {
        const headerLinks = document.querySelectorAll('.headerlink');
        
        headerLinks.forEach(link => {
            link.innerHTML = '<i class="icon-link"></i>';
        });
    }
}
