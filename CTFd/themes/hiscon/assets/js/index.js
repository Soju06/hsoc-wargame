import CTFd from "@ctfdio/ctfd-js";

import dayjs from "dayjs";
import $ from "jquery";
import advancedFormat from "dayjs/plugin/advancedFormat";

import times from "./theme/times";
import styles from "./theme/styles";
import highlight from "./theme/highlight";

import alerts from "./utils/alerts";
import tooltips from "./utils/tooltips";
import collapse from "./utils/collapse";

import eventAlerts from "./utils/notifications/alerts";
import eventToasts from "./utils/notifications/toasts";
import eventRead from "./utils/notifications/read";
import MarkdownIt from "markdown-it";

dayjs.extend(advancedFormat);
CTFd.init(window.init);

CTFd.lib.markdown = function (config) {
  const md_config = { ...{ html: true, linkify: true }, ...config };
  const md = MarkdownIt(md_config);
  md.renderer.rules.link_open = function (tokens, idx, options, env, self) {
    tokens[idx].attrPush(["target", "_blank"]);
    return self.renderToken(tokens, idx, options);
  };
  return md;
};
CTFd.lib.jquery = $;


(() => {
  styles();
  times();
  highlight();

  alerts();
  tooltips();
  collapse();

  eventRead();
  eventAlerts();
  eventToasts();
})();

export default CTFd;