import $ from "jquery";

window.jQuery = $;
window.$ = $;

require("../css/main.scss");
require("foundation-sites/dist/js/foundation");

import {
  createEnlargeImagesButtons,
  createResponsiveTables,
  openExternalLinksNewBrowserTab,
} from "./body";
import { onScrollHighlightSecondarySidebar } from "./sidebar";
import { initBanner, onCloseBanner, onResizeBanner } from "./promo-banner";
import {
  loadCollapsibleNavigation,
  onClickCollapsibleNavigationButton,
  onScrollCollapsibleNavigation,
} from "./collapse";

$(document).ready(function () {
  /* Body */
  createEnlargeImagesButtons();
  $(document).foundation();
  createResponsiveTables();
  openExternalLinksNewBrowserTab();
  /* Banner */
  initBanner();
  onCloseBanner();
  onResizeBanner();
  /* Collapsible navigation */
  loadCollapsibleNavigation();
  onClickCollapsibleNavigationButton();
  onScrollCollapsibleNavigation();
  /* Sidebar */
  onScrollHighlightSecondarySidebar();
});
