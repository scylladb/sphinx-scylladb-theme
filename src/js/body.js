export const openExternalLinksNewBrowserTab = () => {
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
};

export const createResponsiveTables = () => {
  const tables = $("table.docutils");
  tables.wrap("<div class='table-wrapper'></div>");

  tables.each(function () {
    if ($(this).find("thead tr").length > 1) {
      $(this).addClass("thead-border");
    }
  });
};

export const createEnlargeImagesButtons = () => {
  $(".content img[width], .content img[style]").each(function () {
    // Update parent css
    const revealID = (Math.random() + 1).toString(36).substring(7);
    $(this).wrap(
      `<span class="enlarge-image"  data-open="` + revealID + `"></div>`,
    );
    // Add image reveal
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
};
