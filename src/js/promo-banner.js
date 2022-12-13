const localStorageKey = "scylladb-docs-hide-banner";

const setItemWithExpiry = (key, value, days) => {
  const now = new Date();
  const ttl = days * 24 * 60 * 60 * 1000;
  const item = {
    value: value,
    expiry: now.getTime() + ttl,
  };
  localStorage.setItem(key, JSON.stringify(item));
};

function getItemWithExpiry(key) {
  const itemStr = localStorage.getItem(key);
  if (!itemStr) {
    return null;
  }
  const item = JSON.parse(itemStr);
  const now = new Date();

  if (now.getTime() > item.expiry) {
    localStorage.removeItem(key);
    return null;
  }
  return item.value;
}

export const hideBanner = () => {
  const promoBanner = $(".promo-banner");
  const promoBannerHeight = promoBanner.outerHeight();
  if (promoBanner.length && !getItemWithExpiry(localStorageKey)) {
    promoBanner.show();
    $("body").css("margin-top", promoBannerHeight);
    $(".side-nav").css("margin-top", promoBannerHeight);
    $(".secondary-side-nav").css("margin-top", promoBannerHeight);
    $(".layout").addClass("layout--has-banner");
  } else {
    promoBanner.hide();
  }
};

export const onCloseBanner = () => {
  $(".promo-banner__close").on("click", function () {
    setItemWithExpiry(localStorageKey, "1", 30);
    $("body").css("margin-top", 0);
    $(".side-nav").css("margin-top", 0);
    $(".secondary-side-nav").css("margin-top", 0);
    $(".promo-banner").hide();
    $(".layout").removeClass("layout--has-banner");
  });
};

export const onResizeBanner = () => {
  $(window).resize(function () {
    const promoBanner = $(".promo-banner");
    const promoBannerHeight = promoBanner.outerHeight();
    if (promoBanner.is(":visible")) {
      $("body").css("margin-top", promoBannerHeight);
      $(".side-nav").css("margin-top", promoBannerHeight);
      $(".secondary-side-nav").css("margin-top", promoBannerHeight);
    }
  });
};
