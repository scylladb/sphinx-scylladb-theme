export class SecondarySidebarHandler {

	onScrollHighlightSecondarySidebar() {
		const sections = $(".content").find("h2").parent();

		$(window).scroll(function () {
			const dynamicPaddingTop = parseInt($('html').css('scroll-padding-top'));
			const currentScroll = $(this).scrollTop() + dynamicPaddingTop;
			sections.each(function () {
				const sectionPosition = $(this).offset().top;
				if (sectionPosition <= currentScroll) {
					const id = $(this).attr("id");

					$(".secondary-side-nav a").removeClass("current");
					$('.secondary-side-nav a[href="#' + id + '"]').addClass("current");
				}
			});
		});

	}

	init() {
		this.onScrollHighlightSecondarySidebar();
	}
}