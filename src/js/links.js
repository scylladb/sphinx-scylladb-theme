export class LinksHandler {

	openExternalLinksNewBrowserTab() {
		const isExternal = new RegExp("^(?:[a-z]+:)?//", "i");
		$("a.reference").each(function () {
			$(this).removeClass("internal external");

			if (isExternal.test($(this).attr("href"))) {
				$(this).addClass("external");
				$(this).attr("target", "_blank");
			} else {
				$(this).addClass("internal");
			}
		});
	}

	init() {
		this.openExternalLinksNewBrowserTab();
	}
}