require("../css/main.scss");
require("foundation-sites/dist/js/foundation");
import Cookies from "js-cookie";

const openExternalLinkNewTab = () => {
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

const hideBanner = () => {
  if (!Cookies.get("hide-enterprise-banner")) {
    $(".custom-promo-banner-wrap").show();
    $("body").css("padding-top", $(".custom-promo-banner-wrap").outerHeight());
  } else {
    $(".custom-promo-banner-wrap").hide();
  }
};

const onCloseBanner = () => {
  $(".custom-promo-banner--close").on("click", function () {
    console.log("click");
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

const onScrollHighlightSecondarySidebar = () => {
  const sections = $(".content .section").find("h2").parent();
  const headerHeight = 83;

  $(window).scroll(function () {
    const currentScroll = $(this).scrollTop();
    sections.each(function () {
      const sectionPosition = $(this).offset().top;
      if (sectionPosition - headerHeight < currentScroll) {
        const id = $(this).attr("id");

        $(".secondary-sidenav a").removeClass("current");
        $('.secondary-sidenav a[href="#' + id + '"]').addClass("current");
      }
    });
  });
};

$(document).ready(function () {
  $(document).foundation();
  openExternalLinkNewTab();
  hideBanner();
  onResizeBanner();
  onCloseBanner();
  onScrollHighlightSecondarySidebar();
});
