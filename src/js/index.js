import $ from "jquery";

window.jQuery = $;
window.$ = $;

require("../css/main.scss");
require("foundation-sites/dist/js/foundation");

import { CollapseHandler} from "./collapse";
import { ImagesHandler } from "./images";
import { LinksHandler } from "./links";
import { PromoBannerHandler } from "./promo-banner";
import { SecondarySidebarHandler } from "./secondary-sidebar";
import { SidebarHandler } from "./sidebar";
import { TablesHandler } from "./tables";

$(document).ready(function () {
  new ImagesHandler().init();
  $(document).foundation();
  new TablesHandler().init();
  new LinksHandler().init();
  new PromoBannerHandler().init();
  new CollapseHandler().init();
  new SidebarHandler().init();
  new SecondarySidebarHandler().init();
});
