require("../css/main.scss");
require("foundation-sites/dist/js/foundation");
import Cookies from "js-cookie";

const openExternalLinksNewBrowserTab = () => {
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

const createResponsiveTables = () => {
  $("table.docutils").wrap("<div class='table-wrapper'></div>");
};

const onScrollHighlightSecondarySidebar = () => {
  const sections = $(".content").find("h2").parent();
  console.log(sections);
  const headerHeight = 83;
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
};

const hideBanner = () => {
  if (!Cookies.get("hide-enterprise-banner")) {
    $(".custom-promo-banner-wrap").show();
    $("body").css("padding-top", $(".custom-promo-banner-wrap").outerHeight());
  } else {
    $(".custom-promo-banner-wrap").hide();
  }
};

const onCloseBanner = () => {
  $(".custom-promo-banner__close").on("click", function () {
    Cookies.set("hide-enterprise-banner", "1");
    $("body").css("padding-top", 0);
    $(".custom-promo-banner-wrap").hide();
  });
};

const onResizeBanner = () => {
  $(window).resize(function () {
    if ($(".custom-promo-banner-wrap").is(":visible")) {
      $("body").css(
        "padding-top",
        $(".custom-promo-banner-wrap").outerHeight()
      );
    }
  });
};

$(document).ready(function () {
  $(document).foundation();
  openExternalLinksNewBrowserTab();
  createResponsiveTables();
  onScrollHighlightSecondarySidebar();
  hideBanner();
  onResizeBanner();
  onCloseBanner();
});
