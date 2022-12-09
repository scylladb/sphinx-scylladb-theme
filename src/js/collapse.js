/* Collapse navigation */
const localStorageKey = "scylla-docs-collapse-side-nav";

const calculateCollapsibleNavigationButtonPosition = () => {
  const collapsibleButton = $(".collapsible-button");
  const footer = $(".footer");
  const offset = 10;
  const footerOffset = footer.offset();
  const footerTop = footerOffset.top;
  const footerBottom = footerTop + footer.outerHeight();
  const screenBottom = $(window).scrollTop() + $(window).innerHeight();
  const screenTop = $(window).scrollTop();
  if (screenBottom > footerTop && screenTop < footerBottom) {
    collapsibleButton.css("bottom", screenBottom - footerTop + offset);
  } else {
    collapsibleButton.css("bottom", offset);
  }
};

const collapseNavigation = () => {
  new Foundation.Tooltip($(".collapsible-button"), {
    position: "top",
    tipText: "Expand",
  });
  localStorage.setItem(localStorageKey, "1");
  $("#side-nav").addClass("side-nav--collapsed");
  $(".content").addClass("content--collapsed");
};

const expandNavigation = () => {
  new Foundation.Tooltip($(".collapsible-button"), {
    position: "top",
    tipText: "Collapse",
  });
  localStorage.setItem(localStorageKey, "0");
  $("#side-nav").removeClass("side-nav--collapsed");
  $(".content").removeClass("content--collapsed");
};

export const loadCollapsibleNavigation = () => {
  if (localStorage.getItem(localStorageKey) == "1") {
    collapseNavigation();
  } else {
    expandNavigation();
  }
  calculateCollapsibleNavigationButtonPosition();
};

export const onClickCollapsibleNavigationButton = () => {
  $(".collapsible-button").on("click", function () {
    $(".collapsible-button").foundation("destroy");
    if ($("#side-nav").hasClass("side-nav--collapsed")) {
      expandNavigation();
    } else {
      collapseNavigation();
    }
    calculateCollapsibleNavigationButtonPosition();
  });
};

export const onScrollCollapsibleNavigation = () => {
  $(window).scroll(function () {
    calculateCollapsibleNavigationButtonPosition();
  });
};
