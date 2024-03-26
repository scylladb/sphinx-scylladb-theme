export class TablesHandler {

	createResponsiveTables() {
		const tables = $("table.docutils");
		tables.wrap("<div class='table-wrapper'></div>");

		tables.each(function () {
			if ($(this).find("thead tr").length > 1) {
				$(this).addClass("thead-border");
			}
		});
	}

	init() {
		this.createResponsiveTables();
	}
}