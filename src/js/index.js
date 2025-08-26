import $ from "jquery";

window.jQuery = $;
window.$ = $;

require("../css/main.scss");
require("foundation-sites/dist/js/foundation");

import { CollapseHandler} from "./collapse";
import { ContentHandler} from "./content";
import { ImagesHandler } from "./images";
import { LinksHandler } from "./links";
import { PromoBannerHandler } from "./promo-banner";
import { SearchScrollPrevention } from "./search-scroll-prevention";
import { SearchToChatHandler } from "./search-to-chat";
import { SecondarySidebarHandler } from "./secondary-sidebar";
import { SidebarHandler } from "./sidebar";
import { TablesHandler } from "./tables";
import {DarkTheme} from "./dark-theme";

$(document).ready(function () {
  new ImagesHandler().init();
  $(document).foundation();
  new ContentHandler().init();
  new TablesHandler().init();
  new DarkTheme().init();
  new LinksHandler().init();
  new PromoBannerHandler().init();
  new CollapseHandler().init();
  new SidebarHandler().init();
  new SecondarySidebarHandler().init();
  new SearchScrollPrevention().init();
  new SearchToChatHandler().init();
});
