export class ImagesHandler {

	createEnlargeImagesButtons() {
		$(".content img[width], .content img[style]").each(function () {
			const revealID = (Math.random() + 1).toString(36).substring(7);
			$(this).wrap(
				`<span class="enlarge-image"  data-open="` + revealID + `"></div>`
			);
			const imageReveal =
				`
                  <div class="reveal enlarge-image-reveal" id="` +
				revealID +
				`" data-reveal>
                  <img src="` +
				$(this).attr("src") +
				`" data-close aria-label="Close modal">
                  </div>
              `;
			$(this).after(imageReveal);
		});
		$(".content a.image-reference").click(function (event) {
			if ($(this).children(".enlarge-image").length > 0) {
				event.preventDefault();
			}
		});
	}

	init() {
		this.createEnlargeImagesButtons();
	}
}