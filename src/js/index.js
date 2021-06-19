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
  const tables = $("table.docutils");
  tables.wrap("<div class='table-wrapper'></div>");

  tables.each(function () {
    if ($(this).find("thead tr").length > 1) {
      console.log("in");
      $(this).addClass("thead-border");
    }
  });
};

const onScrollHighlightSecondarySidebar = () => {
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
};

const hideBanner = () => {
  const promoBanner = $(".promo-banner");
  const promoBannerHeight = promoBanner.outerHeight();
  if (!Cookies.get("scylladocs-hide-banner")) {
    promoBanner.show();
    $("body").css("padding-top", promoBannerHeight);
    $(".side-nav").css("padding-top", promoBannerHeight);
    $(".secondary-side-nav").css("padding-top", promoBannerHeight);
  } else {
    promoBanner.hide();
  }
};

const onCloseBanner = () => {
  $(".custom-promo-banner__close").on("click", function () {
    Cookies.set("scylladocs-hide-banner", "1");
    $("body").css("padding-top", 0);
    $(".sidebar-left").css("padding-top", 0);
    $(".sidebar-right").css("padding-top", 0);
    $(".promo-banner").hide();
  });
};

const onResizeBanner = () => {
  const promoBanner = $(".promo-banner");
  const promoBannerHeight = promoBanner.outerHeight();
  $(window).resize(function () {
    if (promoBanner.is(":visible")) {
      $("body").css("padding-top", promoBannerHeight);
      $(".side-nav").css("padding-top", promoBannerHeight);
      $(".secondary-side-nav").css("padding-top", promoBannerHeight);
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
