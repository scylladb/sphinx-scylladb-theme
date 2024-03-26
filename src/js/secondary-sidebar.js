export class SecondarySidebarHandler {

	onScrollHighlightSecondarySidebar() {
		const sections = $(".content").find("h2").parent();
		const headerHeight = 80;
		const offset = 20;

		$(window).scroll(function () {
			const currentScroll = $(this).scrollTop();
			sections.each(function () {
				const sectionPosition = $(this).offset().top;
				if (sectionPosition - headerHeight - offset < currentScroll) {
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