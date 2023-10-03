import $ from "jquery";

window.jQuery = $;
window.$ = $;

require("../css/main.scss");
require("foundation-sites/dist/js/foundation");

import {
  adjustScrollPaddingTop,
  createEnlargeImagesButtons,
  createResponsiveTables,
  openExternalLinksNewBrowserTab,
} from "./body";
import { onScrollHighlightSecondarySidebar } from "./sidebar";
import { initBanner, onChangeMetaBanner, onCloseBanner, onResizeBanner } from "./promo-banner";
import {
  loadCollapsibleNavigation,
  onClickCollapsibleNavigationButton,
  onScrollCollapsibleNavigation,
} from "./collapse";

$(document).ready(function () {
  /* Body */
  adjustScrollPaddingTop();
  createEnlargeImagesButtons();
  $(document).foundation();
  createResponsiveTables();
  openExternalLinksNewBrowserTab();
  /* Banner */
  initBanner();
  onChangeMetaBanner();
  onCloseBanner();
  onResizeBanner();
  /* Collapsible navigation */
  loadCollapsibleNavigation();
  onClickCollapsibleNavigationButton();
  onScrollCollapsibleNavigation();
  /* Sidebar */
  onScrollHighlightSecondarySidebar();
});
