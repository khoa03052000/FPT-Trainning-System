/*! intercooler  1.2.3 2019-11-05 */

!(function (a, b) {
  "function" == typeof define && define.amd
    ? define(["jquery"], function (c) {
        return (a.Intercooler = b(c));
      })
    : "object" == typeof module && module.exports
    ? (module.exports = b(require("jquery")))
    : (a.Intercooler = b(a.jQuery));
})(this, function ($) {
  var Intercooler =
    Intercooler ||
    (function () {
      "use strict";
      function remove(a) {
        a.remove();
      }
      function showIndicator(a) {
        a.closest(".ic-use-transition").length > 0
          ? (a.data("ic-use-transition", !0),
            a.removeClass("ic-use-transition"))
          : a.show();
      }
      function hideIndicator(a) {
        a.data("ic-use-transition") || a.data("ic-indicator-cleared")
          ? (a.data("ic-use-transition", null),
            a.addClass("ic-use-transition"),
            a.data("ic-indicator-cleared", !0))
          : a.hide();
      }
      function fixICAttributeName(a) {
        return USE_DATA ? "data-" + a : a;
      }
      function getICAttribute(a, b) {
        return a.attr(fixICAttributeName(b));
      }
      function setICAttribute(a, b, c) {
        a.attr(fixICAttributeName(b), c);
      }
      function prepend(a, b) {
        try {
          a.prepend(b);
        } catch (b) {
          log(a, formatError(b), "ERROR");
        }
        if (getICAttribute(a, "ic-limit-children")) {
          var c = parseInt(getICAttribute(a, "ic-limit-children"));
          a.children().length > c &&
            a.children().slice(c, a.children().length).remove();
        }
      }
      function append(a, b) {
        try {
          a.append(b);
        } catch (b) {
          log(a, formatError(b), "ERROR");
        }
        if (getICAttribute(a, "ic-limit-children")) {
          var c = parseInt(getICAttribute(a, "ic-limit-children"));
          a.children().length > c &&
            a
              .children()
              .slice(0, a.children().length - c)
              .remove();
        }
      }
      function triggerEvent(a, b, c) {
        $.zepto && (b = b.split(".").reverse().join(":")), a.trigger(b, c);
      }
      function log(a, b, c) {
        if (
          (null == a && (a = $("body")),
          triggerEvent(a, "log.ic", [b, c, a]),
          "ERROR" == c)
        ) {
          window.console && window.console.log("Intercooler Error : " + b);
          var d = closestAttrValue($("body"), "ic-post-errors-to");
          d && $.post(d, { error: b });
        }
      }
      function uuid() {
        return _UUID++;
      }
      function icSelectorFor(a) {
        return getICAttributeSelector("ic-id='" + getIntercoolerId(a) + "'");
      }
      function parseInterval(a) {
        return (
          log(null, "POLL: Parsing interval string " + a, "DEBUG"),
          "null" == a || "false" == a || "" == a
            ? null
            : a.lastIndexOf("ms") == a.length - 2
            ? parseFloat(a.substr(0, a.length - 2))
            : a.lastIndexOf("s") == a.length - 1
            ? 1e3 * parseFloat(a.substr(0, a.length - 1))
            : 1e3
        );
      }
      function getICAttributeSelector(a) {
        return "[" + fixICAttributeName(a) + "]";
      }
      function initScrollHandler() {
        null == _scrollHandler &&
          ((_scrollHandler = function () {
            $(
              getICAttributeSelector("ic-trigger-on='scrolled-into-view'")
            ).each(function () {
              var a = $(this);
              isScrolledIntoView(getTriggeredElement(a)) &&
                1 != a.data("ic-scrolled-into-view-loaded") &&
                (a.data("ic-scrolled-into-view-loaded", !0), fireICRequest(a));
            });
          }),
          $(window).scroll(_scrollHandler));
      }
      function currentUrl() {
        return (
          window.location.pathname +
          window.location.search +
          window.location.hash
        );
      }
      function createDocument(a) {
        var b = null;
        return (
          /<(html|body)/i.test(a)
            ? ((b = document.documentElement.cloneNode()), (b.innerHTML = a))
            : ((b = document.documentElement.cloneNode(!0)),
              (b.querySelector("body").innerHTML = a)),
          $(b)
        );
      }
      function getTarget(a) {
        return getTargetImpl(a, "ic-target");
      }
      function getTargetImpl(a, b) {
        var c = $(a).closest(getICAttributeSelector(b)),
          d = getICAttribute(c, b);
        return "this" == d
          ? c
          : d && 0 != d.indexOf("this.")
          ? 0 == d.indexOf("closest ")
            ? a.closest(d.substr(8))
            : 0 == d.indexOf("find ")
            ? a.find(d.substr(5))
            : $(d)
          : a;
      }
      function processHeaders(a, b) {
        (a = $(a)),
          triggerEvent(a, "beforeHeaders.ic", [a, b]),
          log(a, "response headers: " + b.getAllResponseHeaders(), "DEBUG");
        var c = null;
        if (
          (b.getResponseHeader("X-IC-Title") &&
            (document.title = b.getResponseHeader("X-IC-Title")),
          b.getResponseHeader("X-IC-Title-Encoded"))
        ) {
          var d = decodeURIComponent(
            b.getResponseHeader("X-IC-Title-Encoded").replace(/\+/g, "%20")
          );
          document.title = d;
        }
        if (b.getResponseHeader("X-IC-Refresh")) {
          var e = b.getResponseHeader("X-IC-Refresh").split(",");
          log(a, "X-IC-Refresh: refreshing " + e, "DEBUG"),
            $.each(e, function (b, c) {
              refreshDependencies(c.replace(/ /g, ""), a);
            });
        }
        if (
          (b.getResponseHeader("X-IC-Script") &&
            (log(
              a,
              "X-IC-Script: evaling " + b.getResponseHeader("X-IC-Script"),
              "DEBUG"
            ),
            globalEval(b.getResponseHeader("X-IC-Script"), [["elt", a]])),
          b.getResponseHeader("X-IC-Redirect") &&
            (log(
              a,
              "X-IC-Redirect: redirecting to " +
                b.getResponseHeader("X-IC-Redirect"),
              "DEBUG"
            ),
            (window.location = b.getResponseHeader("X-IC-Redirect"))),
          "true" == b.getResponseHeader("X-IC-CancelPolling") &&
            cancelPolling(a.closest(getICAttributeSelector("ic-poll"))),
          "true" == b.getResponseHeader("X-IC-ResumePolling"))
        ) {
          var f = a.closest(getICAttributeSelector("ic-poll"));
          setICAttribute(f, "ic-pause-polling", null), startPolling(f);
        }
        if (b.getResponseHeader("X-IC-SetPollInterval")) {
          var f = a.closest(getICAttributeSelector("ic-poll"));
          cancelPolling(f),
            setICAttribute(
              f,
              "ic-poll",
              b.getResponseHeader("X-IC-SetPollInterval")
            ),
            startPolling(f);
        }
        b.getResponseHeader("X-IC-Open") &&
          (log(
            a,
            "X-IC-Open: opening " + b.getResponseHeader("X-IC-Open"),
            "DEBUG"
          ),
          window.open(b.getResponseHeader("X-IC-Open")));
        var g = b.getResponseHeader("X-IC-Trigger");
        if (g)
          if (
            (log(a, "X-IC-Trigger: found trigger " + g, "DEBUG"),
            (c = getTarget(a)),
            b.getResponseHeader("X-IC-Trigger-Data"))
          ) {
            var h = $.parseJSON(b.getResponseHeader("X-IC-Trigger-Data"));
            triggerEvent(c, g, h);
          } else
            g.indexOf("{") >= 0
              ? $.each($.parseJSON(g), function (a, b) {
                  triggerEvent(c, a, b);
                })
              : triggerEvent(c, g, []);
        var i = b.getResponseHeader("X-IC-Set-Local-Vars");
        if (
          (i &&
            $.each($.parseJSON(i), function (a, b) {
              localStorage.setItem(a, b);
            }),
          b.getResponseHeader("X-IC-Remove") && a)
        ) {
          var j = b.getResponseHeader("X-IC-Remove");
          j += "";
          var k = parseInterval(j);
          log(a, "X-IC-Remove header found.", "DEBUG"),
            (c = getTarget(a)),
            "true" == j || null == k
              ? remove(c)
              : (c.addClass("ic-removing"),
                setTimeout(function () {
                  remove(c);
                }, k));
        }
        return triggerEvent(a, "afterHeaders.ic", [a, b]), !0;
      }
      function beforeRequest(a) {
        a.addClass("disabled"),
          a.addClass("ic-request-in-flight"),
          a.data("ic-request-in-flight", !0);
      }
      function requestCleanup(a, b, c) {
        a.length > 0 && hideIndicator(a),
          b.length > 0 && hideIndicator(b),
          c.removeClass("disabled"),
          c.removeClass("ic-request-in-flight"),
          c.data("ic-request-in-flight", !1),
          c.data("ic-next-request") &&
            (c.data("ic-next-request").req(), c.data("ic-next-request", null));
      }
      function replaceOrAddMethod(a, b) {
        if ("string" === $.type(a)) {
          var c = /(&|^)_method=[^&]*/,
            d = "&_method=" + b;
          return c.test(a) ? a.replace(c, d) : a + d;
        }
        return a.append("_method", b), a;
      }
      function isIdentifier(a) {
        return /^[$A-Z_][0-9A-Z_$]*$/i.test(a);
      }
      function globalEval(a, b) {
        var c = [],
          d = [];
        if (b)
          for (var e = 0; e < b.length; e++) c.push(b[e][0]), d.push(b[e][1]);
        return isIdentifier(a)
          ? window[a].apply(this, d)
          : window.eval
              .call(window, "(function (" + c.join(", ") + ") {" + a + "})")
              .apply(this, d);
      }
      function closestAttrValue(a, b) {
        var c = $(a).closest(getICAttributeSelector(b));
        return c.length > 0 ? getICAttribute(c, b) : null;
      }
      function formatError(a) {
        var b = a.toString() + "\n";
        try {
          b += a.stack;
        } catch (a) {}
        return b;
      }
      function getLocalURL(a, b, c) {
        if (b) {
          a += "?";
          var d = {};
          c.replace(/([^=&]+)=([^&]*)/gi, function (a, b, c) {
            d[b] = c;
          }),
            $(b.split(",")).each(function (b) {
              var c = $.trim(this),
                e = d[c] || "";
              (a += 0 == b ? "" : "&"), (a += c + "=" + e);
            });
        }
        return a;
      }
      function handleRemoteRequest(a, b, c, d, e) {
        beforeRequest(a), (d = replaceOrAddMethod(d, b));
        var f = findGlobalIndicator(a);
        f && f.length > 0 && showIndicator(f);
        var g = findIndicator(a);
        g.length > 0 && showIndicator(g);
        var h,
          i = uuid(),
          j = new Date();
        h = USE_ACTUAL_HTTP_METHOD ? b : "GET" == b ? "GET" : "POST";
        var k = {
          type: h,
          url: c,
          data: d,
          dataType: "text",
          headers: {
            Accept: "text/html-partial, */*; q=0.9",
            "X-IC-Request": !0,
            "X-HTTP-Method-Override": b,
          },
          beforeSend: function (e, f) {
            triggerEvent(a, "beforeSend.ic", [a, d, f, e, i]),
              log(
                a,
                "before AJAX request " + i + ": " + b + " to " + c,
                "DEBUG"
              );
            var g = closestAttrValue(a, "ic-on-beforeSend");
            g &&
              globalEval(g, [
                ["elt", a],
                ["data", d],
                ["settings", f],
                ["xhr", e],
              ]),
              maybeInvokeLocalAction(a, "-beforeSend");
          },
          success: function (b, c, h) {
            triggerEvent(a, "success.ic", [a, b, c, h, i]),
              log(a, "AJAX request " + i + " was successful.", "DEBUG");
            var j = closestAttrValue(a, "ic-on-success");
            if (
              !j ||
              0 !=
                globalEval(j, [
                  ["elt", a],
                  ["data", b],
                  ["textStatus", c],
                  ["xhr", h],
                ])
            ) {
              var k = new Date(),
                l = document.title;
              try {
                if (processHeaders(a, h)) {
                  log(
                    a,
                    "Processed headers for request " +
                      i +
                      " in " +
                      (new Date() - k) +
                      "ms",
                    "DEBUG"
                  );
                  var m = new Date();
                  if (
                    h.getResponseHeader("X-IC-PushURL") ||
                    "true" == closestAttrValue(a, "ic-push-url")
                  )
                    try {
                      requestCleanup(g, f, a);
                      var n = closestAttrValue(a, "ic-src"),
                        o = closestAttrValue(a, "ic-push-params"),
                        p =
                          h.getResponseHeader("X-IC-PushURL") ||
                          getLocalURL(n, o, d);
                      if (!_history) throw "History support not enabled";
                      _history.snapshotForHistory(p, l);
                    } catch (b) {
                      log(
                        a,
                        "Error during history snapshot for " +
                          i +
                          ": " +
                          formatError(b),
                        "ERROR"
                      );
                    }
                  e(b, c, a, h),
                    log(
                      a,
                      "Process content for request " +
                        i +
                        " in " +
                        (new Date() - m) +
                        "ms",
                      "DEBUG"
                    );
                }
                triggerEvent(a, "after.success.ic", [a, b, c, h, i]),
                  maybeInvokeLocalAction(a, "-success");
              } catch (b) {
                log(
                  a,
                  "Error processing successful request " +
                    i +
                    " : " +
                    formatError(b),
                  "ERROR"
                );
              }
            }
          },
          error: function (b, d, e) {
            triggerEvent(a, "error.ic", [a, d, e, b]);
            var f = closestAttrValue(a, "ic-on-error");
            f &&
              globalEval(f, [
                ["elt", a],
                ["status", d],
                ["str", e],
                ["xhr", b],
              ]),
              processHeaders(a, b),
              maybeInvokeLocalAction(a, "-error"),
              log(
                a,
                "AJAX request " +
                  i +
                  " to " +
                  c +
                  " experienced an error: " +
                  e,
                "ERROR"
              );
          },
          complete: function (b, c) {
            log(
              a,
              "AJAX request " + i + " completed in " + (new Date() - j) + "ms",
              "DEBUG"
            ),
              requestCleanup(g, f, a);
            try {
              $.contains(document, a[0])
                ? triggerEvent(a, "complete.ic", [a, d, c, b, i])
                : triggerEvent($("body"), "complete.ic", [a, d, c, b, i]);
            } catch (b) {
              log(
                a,
                "Error during complete.ic event for " +
                  i +
                  " : " +
                  formatError(b),
                "ERROR"
              );
            }
            var e = closestAttrValue(a, "ic-on-complete");
            e &&
              globalEval(e, [
                ["elt", a],
                ["xhr", b],
                ["status", c],
              ]),
              maybeInvokeLocalAction(a, "-complete");
          },
        };
        "string" != $.type(d) &&
          ((k.dataType = null), (k.processData = !1), (k.contentType = !1)),
          triggerEvent($(document), "beforeAjaxSend.ic", [k, a]),
          k.cancel ? requestCleanup(g, f, a) : $.ajax(k);
      }
      function findGlobalIndicator(a) {
        var b = $([]);
        a = $(a);
        var c = closestAttrValue(a, "ic-global-indicator");
        return c && "false" !== c && (b = $(c).first()), b;
      }
      function findIndicator(a) {
        var b = $([]);
        if (((a = $(a)), getICAttribute(a, "ic-indicator")))
          b = $(getICAttribute(a, "ic-indicator")).first();
        else if (((b = a.find(".ic-indicator").first()), 0 == b.length)) {
          var c = closestAttrValue(a, "ic-indicator");
          c
            ? (b = $(c).first())
            : a.next().is(".ic-indicator") && (b = a.next());
        }
        return b;
      }
      function processIncludes(a, b) {
        if (0 == $.trim(b).indexOf("{")) {
          var c = $.parseJSON(b);
          $.each(c, function (b, c) {
            a = appendData(a, b, c);
          });
        } else
          $(b).each(function () {
            var b = $(this).serializeArray();
            $.each(b, function (b, c) {
              a = appendData(a, c.name, c.value);
            });
          });
        return a;
      }
      function processLocalVars(a, b) {
        return (
          $(b.split(",")).each(function () {
            var b = $.trim(this),
              c = localStorage.getItem(b);
            c && (a = appendData(a, b, c));
          }),
          a
        );
      }
      function appendData(a, b, c) {
        return "string" === $.type(a)
          ? ("string" !== $.type(c) && (c = JSON.stringify(c)),
            a + "&" + b + "=" + encodeURIComponent(c))
          : (a.append(b, c), a);
      }
      function getParametersForElement(a, b, c) {
        var d = getTarget(b),
          e = null;
        if (b.is("form") && "multipart/form-data" == b.attr("enctype"))
          (e = new FormData(b[0])), (e = appendData(e, "ic-request", !0));
        else {
          e = "ic-request=true";
          var f = b.closest("form");
          if (b.is("form") || ("GET" != a && f.length > 0)) {
            e += "&" + f.serialize();
            var g = b.data("ic-last-clicked-button");
            g && (e = appendData(e, g.name, g.value));
          } else e += "&" + b.serialize();
        }
        var h = closestAttrValue(b, "ic-prompt");
        if (h) {
          var i = prompt(h);
          if (!i) return null;
          var j = closestAttrValue(b, "ic-prompt-name") || "ic-prompt-value";
          e = appendData(e, j, i);
        }
        b.attr("id") && (e = appendData(e, "ic-element-id", b.attr("id"))),
          b.attr("name") &&
            (e = appendData(e, "ic-element-name", b.attr("name"))),
          getICAttribute(d, "ic-id") &&
            (e = appendData(e, "ic-id", getICAttribute(d, "ic-id"))),
          d.attr("id") && (e = appendData(e, "ic-target-id", d.attr("id"))),
          c &&
            c.attr("id") &&
            (e = appendData(e, "ic-trigger-id", c.attr("id"))),
          c &&
            c.attr("name") &&
            (e = appendData(e, "ic-trigger-name", c.attr("name")));
        var k = closestAttrValue(b, "ic-include");
        k && (e = processIncludes(e, k));
        var l = closestAttrValue(b, "ic-local-vars");
        l && (e = processLocalVars(e, l)),
          $(getICAttributeSelector("ic-global-include")).each(function () {
            e = processIncludes(
              e,
              getICAttribute($(this), "ic-global-include")
            );
          }),
          (e = appendData(e, "ic-current-url", currentUrl()));
        var m = closestAttrValue(b, "ic-select-from-response");
        return (
          m && (e = appendData(e, "ic-select-from-response", m)),
          log(b, "request parameters " + e, "DEBUG"),
          e
        );
      }
      function maybeSetIntercoolerInfo(a) {
        getIntercoolerId(getTarget(a)),
          1 != a.data("elementAdded.ic") &&
            (a.data("elementAdded.ic", !0), triggerEvent(a, "elementAdded.ic"));
      }
      function getIntercoolerId(a) {
        return (
          getICAttribute(a, "ic-id") || setICAttribute(a, "ic-id", uuid()),
          getICAttribute(a, "ic-id")
        );
      }
      function processNodes(a) {
        (a = $(a)),
          a.length > 1
            ? a.each(function () {
                processNodes(this);
              })
            : (processMacros(a),
              processEnhancement(a),
              processSources(a),
              processPolling(a),
              processEventSources(a),
              processTriggerOn(a),
              processRemoveAfter(a),
              processAddClasses(a),
              processRemoveClasses(a));
      }
      function fireReadyStuff(a) {
        triggerEvent(a, "nodesProcessed.ic"),
          $.each(_readyHandlers, function (b, c) {
            try {
              c(a);
            } catch (b) {
              log(a, formatError(b), "ERROR");
            }
          });
      }
      function autoFocus(a) {
        a.find("[autofocus]").last().focus();
      }
      function processMacros(a) {
        $.each(_MACROS, function (b, c) {
          0 == a.closest(".ic-ignore").length &&
            (a.is("[" + c + "]") && processMacro(c, a),
            a.find("[" + c + "]").each(function () {
              var a = $(this);
              0 == a.closest(".ic-ignore").length && processMacro(c, a);
            }));
        });
      }
      function processSources(a) {
        0 == a.closest(".ic-ignore").length &&
          (a.is(getICAttributeSelector("ic-src")) && maybeSetIntercoolerInfo(a),
          a.find(getICAttributeSelector("ic-src")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && maybeSetIntercoolerInfo(a);
          }));
      }
      function processPolling(a) {
        0 == a.closest(".ic-ignore").length &&
          (a.is(getICAttributeSelector("ic-poll")) &&
            (maybeSetIntercoolerInfo(a), startPolling(a)),
          a.find(getICAttributeSelector("ic-poll")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length &&
              (maybeSetIntercoolerInfo(a), startPolling(a));
          }));
      }
      function processTriggerOn(a) {
        0 == a.closest(".ic-ignore").length &&
          (handleTriggerOn(a),
          a.find(getICAttributeSelector("ic-trigger-on")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && handleTriggerOn(a);
          }));
      }
      function processRemoveAfter(a) {
        0 == a.closest(".ic-ignore").length &&
          (handleRemoveAfter(a),
          a.find(getICAttributeSelector("ic-remove-after")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && handleRemoveAfter(a);
          }));
      }
      function processAddClasses(a) {
        0 == a.closest(".ic-ignore").length &&
          (handleAddClasses(a),
          a.find(getICAttributeSelector("ic-add-class")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && handleAddClasses(a);
          }));
      }
      function processRemoveClasses(a) {
        0 == a.closest(".ic-ignore").length &&
          (handleRemoveClasses(a),
          a.find(getICAttributeSelector("ic-remove-class")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && handleRemoveClasses(a);
          }));
      }
      function processEnhancement(a) {
        0 == a.closest(".ic-ignore").length &&
          ("true" === closestAttrValue(a, "ic-enhance")
            ? enhanceDomTree(a)
            : a.find(getICAttributeSelector("ic-enhance")).each(function () {
                enhanceDomTree($(this));
              }));
      }
      function processEventSources(a) {
        0 == a.closest(".ic-ignore").length &&
          (handleEventSource(a),
          a.find(getICAttributeSelector("ic-sse-src")).each(function () {
            var a = $(this);
            0 == a.closest(".ic-ignore").length && handleEventSource(a);
          }));
      }
      function startPolling(a) {
        if (
          null == a.data("ic-poll-interval-id") &&
          "true" != getICAttribute(a, "ic-pause-polling")
        ) {
          var b = parseInterval(getICAttribute(a, "ic-poll"));
          if (null != b) {
            var c = icSelectorFor(a),
              d = parseInt(getICAttribute(a, "ic-poll-repeats")) || -1,
              e = 0;
            log(a, "POLL: Starting poll for element " + c, "DEBUG");
            var f = setInterval(function () {
              var b = $(c);
              triggerEvent(a, "onPoll.ic", b),
                0 == b.length || e == d || a.data("ic-poll-interval-id") != f
                  ? (log(a, "POLL: Clearing poll for element " + c, "DEBUG"),
                    clearTimeout(f))
                  : fireICRequest(b),
                e++;
            }, b);
            a.data("ic-poll-interval-id", f);
          }
        }
      }
      function cancelPolling(a) {
        null != a.data("ic-poll-interval-id") &&
          (clearTimeout(a.data("ic-poll-interval-id")),
          a.data("ic-poll-interval-id", null));
      }
      function refreshDependencies(a, b) {
        log(b, "refreshing dependencies for path " + a, "DEBUG"),
          $(getICAttributeSelector("ic-src")).each(function () {
            var c = !1,
              d = $(this);
            "GET" == verbFor(d) &&
              "ignore" != getICAttribute(d, "ic-deps") &&
              (isDependent(a, getICAttribute(d, "ic-src"))
                ? (null != b && $(b)[0] == d[0]) || (fireICRequest(d), (c = !0))
                : (isICDepsDependent(a, getICAttribute(d, "ic-deps")) ||
                    "*" == getICAttribute(d, "ic-deps")) &&
                  ((null != b && $(b)[0] == d[0]) ||
                    (fireICRequest(d), (c = !0)))),
              c && log(d, "depends on path " + a + ", refreshing...", "DEBUG");
          });
      }
      function isICDepsDependent(a, b) {
        if (b)
          for (var c = b.split(","), d = 0; d < c.length; d++) {
            var e = c[d].trim();
            if (isDependent(a, e)) return !0;
          }
        return !1;
      }
      function isDependent(a, b) {
        return !!_isDependentFunction(a, b);
      }
      function verbFor(a) {
        return (
          (a = $(a)),
          getICAttribute(a, "ic-verb")
            ? getICAttribute(a, "ic-verb").toUpperCase()
            : "GET"
        );
      }
      function eventFor(a, b) {
        return "default" == a
          ? ((b = $(b)),
            b.is("button")
              ? "click"
              : b.is("form")
              ? "submit"
              : b.is("input, textarea, select, button")
              ? "change"
              : "click")
          : a;
      }
      function preventDefault(a, b) {
        return (
          a.is("form") ||
          (a.is('input[type="submit"], button') &&
            1 == a.closest("form").length) ||
          (a.is("a") && a.is("[href]") && 0 != a.attr("href").indexOf("#"))
        );
      }
      function handleRemoveAfter(a) {
        if (((a = $(a)), getICAttribute(a, "ic-remove-after"))) {
          var b = parseInterval(getICAttribute(a, "ic-remove-after"));
          setTimeout(function () {
            remove(a);
          }, b);
        }
      }
      function parseAndApplyClass(a, b, c) {
        var d = "",
          e = 50;
        if (a.indexOf(":") > 0) {
          var f = a.split(":");
          (d = f[0]), (e = parseInterval(f[1]));
        } else d = a;
        setTimeout(function () {
          b[c](d);
        }, e);
      }
      function handleAddClasses(a) {
        if (((a = $(a)), getICAttribute(a, "ic-add-class")))
          for (
            var b = getICAttribute(a, "ic-add-class").split(","),
              c = b.length,
              d = 0;
            d < c;
            d++
          )
            parseAndApplyClass($.trim(b[d]), a, "addClass");
      }
      function handleRemoveClasses(a) {
        if (((a = $(a)), getICAttribute(a, "ic-remove-class")))
          for (
            var b = getICAttribute(a, "ic-remove-class").split(","),
              c = b.length,
              d = 0;
            d < c;
            d++
          )
            parseAndApplyClass($.trim(b[d]), a, "removeClass");
      }
      function handleEventSource(a) {
        if (((a = $(a)), getICAttribute(a, "ic-sse-src"))) {
          var b = getICAttribute(a, "ic-sse-src"),
            c = "true" === getICAttribute(a, "ic-sse-with-credentials"),
            d = initEventSource(a, b, c);
          a.data("ic-event-sse-source", d), a.data("ic-event-sse-map", {});
        }
      }
      function initEventSource(a, b, c) {
        var d = Intercooler._internal.initEventSource(b, c);
        return (
          (d.onmessage = function (b) {
            processICResponse(b.data, a, !1);
          }),
          d
        );
      }
      function registerSSE(a, b) {
        var c = a.data("ic-event-sse-source"),
          d = a.data("ic-event-sse-map");
        c.addEventListener &&
          1 != d[b] &&
          c.addEventListener(b, function () {
            a.find(getICAttributeSelector("ic-trigger-on")).each(function () {
              var a = $(this);
              a.attr("ic-trigger-on") == "sse:" + b && fireICRequest(a);
            });
          });
      }
      function getTriggeredElement(a) {
        var b = getICAttribute(a, "ic-trigger-from");
        return b
          ? $("document" == b ? document : "window" == b ? window : b)
          : a;
      }
      function handleTriggerOn(a) {
        var b = getICAttribute(a, "ic-trigger-on");
        if (b) {
          a.is("form") &&
            a.on(
              "click focus",
              "input, button, select, textarea",
              function (b) {
                $(this).is('input[type="submit"], button') &&
                $(this).is("[name]")
                  ? a.data("ic-last-clicked-button", {
                      name: $(this).attr("name"),
                      value: $(this).val(),
                    })
                  : a.data("ic-last-clicked-button", null);
              }
            );
          for (var c = b.split(","), d = 0; d < c.length; d++) {
            var e = $.trim(c[d]),
              f = e.split(" "),
              g = eventFor(f[0], $(a)),
              h = f[1];
            if ("load" == e) fireICRequest(a);
            else if ("scrolled-into-view" == e)
              initScrollHandler(),
                setTimeout(function () {
                  triggerEvent($(window), "scroll");
                }, 100);
            else if (0 == g.indexOf("sse:")) {
              var i = a.closest(getICAttributeSelector("ic-sse-src"));
              i.length > 0 && registerSSE(i, f[0].substr(4));
            } else if (
              ($(getTriggeredElement(a)).on(g, function (b) {
                var c = closestAttrValue(a, "ic-on-beforeTrigger");
                if (
                  c &&
                  0 ==
                    globalEval(c, [
                      ["elt", a],
                      ["evt", b],
                      ["elt", a],
                    ])
                )
                  return (
                    log(
                      a,
                      "ic-trigger cancelled by ic-on-beforeTrigger",
                      "DEBUG"
                    ),
                    !1
                  );
                if ("changed" == h) {
                  var d = a.val(),
                    e = a.data("ic-previous-val");
                  a.data("ic-previous-val", d), d != e && fireICRequest(a);
                } else if ("once" == h) {
                  var f = a.data("ic-already-triggered");
                  a.data("ic-already-triggered", !0),
                    !0 !== f && fireICRequest(a);
                } else fireICRequest(a);
                return !preventDefault(a, b) || (b.preventDefault(), !1);
              }),
              g && 0 == g.indexOf("timeout:"))
            ) {
              var j = parseInterval(g.split(":")[1]);
              setTimeout(function () {
                $(getTriggeredElement(a)).trigger(g);
              }, j);
            }
          }
        }
      }
      function macroIs(a, b) {
        return a == fixICAttributeName(b);
      }
      function processMacro(a, b) {
        macroIs(a, "ic-post-to") &&
          (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-post-to")),
          setIfAbsent(b, "ic-verb", "POST"),
          setIfAbsent(b, "ic-trigger-on", "default"),
          setIfAbsent(b, "ic-deps", "ignore")),
          macroIs(a, "ic-put-to") &&
            (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-put-to")),
            setIfAbsent(b, "ic-verb", "PUT"),
            setIfAbsent(b, "ic-trigger-on", "default"),
            setIfAbsent(b, "ic-deps", "ignore")),
          macroIs(a, "ic-patch-to") &&
            (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-patch-to")),
            setIfAbsent(b, "ic-verb", "PATCH"),
            setIfAbsent(b, "ic-trigger-on", "default"),
            setIfAbsent(b, "ic-deps", "ignore")),
          macroIs(a, "ic-get-from") &&
            (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-get-from")),
            setIfAbsent(b, "ic-trigger-on", "default"),
            setIfAbsent(b, "ic-deps", "ignore")),
          macroIs(a, "ic-delete-from") &&
            (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-delete-from")),
            setIfAbsent(b, "ic-verb", "DELETE"),
            setIfAbsent(b, "ic-trigger-on", "default"),
            setIfAbsent(b, "ic-deps", "ignore")),
          macroIs(a, "ic-action") && setIfAbsent(b, "ic-trigger-on", "default");
        var c = null,
          d = null;
        if (macroIs(a, "ic-style-src")) {
          c = getICAttribute(b, "ic-style-src").split(":");
          var e = c[0];
          (d = c[1]),
            setIfAbsent(b, "ic-src", d),
            setIfAbsent(b, "ic-target", "this.style." + e);
        }
        if (macroIs(a, "ic-attr-src")) {
          c = getICAttribute(b, "ic-attr-src").split(":");
          var f = c[0];
          (d = c[1]),
            setIfAbsent(b, "ic-src", d),
            setIfAbsent(b, "ic-target", "this." + f);
        }
        macroIs(a, "ic-prepend-from") &&
          (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-prepend-from")),
          setIfAbsent(b, "ic-swap-style", "prepend")),
          macroIs(a, "ic-append-from") &&
            (setIfAbsent(b, "ic-src", getICAttribute(b, "ic-append-from")),
            setIfAbsent(b, "ic-swap-style", "append"));
      }
      function isLocalLink(a) {
        return (
          location.hostname === a[0].hostname &&
          a.attr("href") &&
          !a.attr("href").startsWith("#")
        );
      }
      function enhanceAnchor(a) {
        "true" === closestAttrValue(a, "ic-enhance") &&
          isLocalLink(a) &&
          (setIfAbsent(a, "ic-src", a.attr("href")),
          setIfAbsent(a, "ic-trigger-on", "default"),
          setIfAbsent(a, "ic-deps", "ignore"),
          setIfAbsent(a, "ic-push-url", "true"));
      }
      function determineFormVerb(a) {
        return (
          a.find('input[name="_method"]').val() ||
          a.attr("method") ||
          a[0].method
        );
      }
      function enhanceForm(a) {
        "true" === closestAttrValue(a, "ic-enhance") &&
          (setIfAbsent(a, "ic-src", a.attr("action")),
          setIfAbsent(a, "ic-trigger-on", "default"),
          setIfAbsent(a, "ic-deps", "ignore"),
          setIfAbsent(a, "ic-verb", determineFormVerb(a)));
      }
      function enhanceDomTree(a) {
        a.is("a") && enhanceAnchor(a),
          a.find("a").each(function () {
            enhanceAnchor($(this));
          }),
          a.is("form") && enhanceForm(a),
          a.find("form").each(function () {
            enhanceForm($(this));
          });
      }
      function setIfAbsent(a, b, c) {
        null == getICAttribute(a, b) && setICAttribute(a, b, c);
      }
      function isScrolledIntoView(a) {
        if (((a = $(a)), 0 == a.height() && 0 == a.width())) return !1;
        var b = $(window).scrollTop(),
          c = b + $(window).height(),
          d = a.offset().top,
          e = d + a.height();
        return e >= b && d <= c && e <= c && d >= b;
      }
      function maybeScrollToTarget(a, b) {
        if (
          "false" != closestAttrValue(a, "ic-scroll-to-target") &&
          ("true" == closestAttrValue(a, "ic-scroll-to-target") ||
            "true" == closestAttrValue(b, "ic-scroll-to-target"))
        ) {
          var c = -50;
          closestAttrValue(a, "ic-scroll-offset")
            ? (c = parseInt(closestAttrValue(a, "ic-scroll-offset")))
            : closestAttrValue(b, "ic-scroll-offset") &&
              (c = parseInt(closestAttrValue(b, "ic-scroll-offset")));
          var d = b.offset().top,
            e = $(window).scrollTop(),
            f = e + window.innerHeight;
          (d < e || d > f) &&
            ((c += d), $("html,body").animate({ scrollTop: c }, 400));
        }
      }
      function getTransitionDuration(a, b) {
        var c = closestAttrValue(a, "ic-transition-duration");
        if (c) return parseInterval(c);
        if ((c = closestAttrValue(b, "ic-transition-duration")))
          return parseInterval(c);
        b = $(b);
        var d = 0,
          e = b.css("transition-duration");
        e && (d += parseInterval(e));
        var f = b.css("transition-delay");
        return f && (d += parseInterval(f)), d;
      }
      function closeSSESource(a) {
        var b = a.data("ic-event-sse-source");
        try {
          b && b.close();
        } catch (b) {
          log(a, "Error closing ServerSentEvent source" + b, "ERROR");
        }
      }
      function beforeSwapCleanup(a) {
        a.find(getICAttributeSelector("ic-sse-src")).each(function () {
          closeSSESource($(this));
        }),
          triggerEvent(a, "beforeSwap.ic");
      }
      function processICResponse(a, b, c, d) {
        if (a && "" != a && " " != a) {
          log(b, "response content: \n" + a, "DEBUG");
          var e = getTarget(b),
            f = closestAttrValue(b, "ic-transform-response");
          f &&
            (a = globalEval(f, [
              ["content", a],
              ["url", d],
              ["elt", b],
            ]));
          var g = maybeFilter(
            a,
            closestAttrValue(b, "ic-select-from-response")
          );
          "true" == closestAttrValue(b, "ic-fix-ids") && fixIDs(g);
          var h = function () {
            if ("true" == closestAttrValue(b, "ic-replace-target")) {
              try {
                beforeSwapCleanup(e),
                  closeSSESource(e),
                  e.replaceWith(g),
                  (e = g);
              } catch (a) {
                log(b, formatError(a), "ERROR");
              }
              processNodes(g), fireReadyStuff(e), autoFocus(e);
            } else {
              if ("prepend" == getICAttribute(b, "ic-swap-style"))
                prepend(e, g), processNodes(g), fireReadyStuff(e), autoFocus(e);
              else if ("append" == getICAttribute(b, "ic-swap-style"))
                append(e, g), processNodes(g), fireReadyStuff(e), autoFocus(e);
              else {
                try {
                  beforeSwapCleanup(e), e.empty().append(g);
                } catch (a) {
                  log(b, formatError(a), "ERROR");
                }
                e.children().each(function () {
                  processNodes(this);
                }),
                  fireReadyStuff(e),
                  autoFocus(e);
              }
              1 != c && maybeScrollToTarget(b, e);
              var a = b.closest(getICAttributeSelector("ic-switch-class")),
                d = a.attr(fixICAttributeName("ic-switch-class"));
              d &&
                (a.children().removeClass(d),
                a.children().each(function () {
                  ($.contains($(this)[0], $(b)[0]) || $(this)[0] == $(b)[0]) &&
                    ($(this).addClass(d), $(this).addClass(d));
                }));
            }
          };
          if (0 == e.length)
            return void log(
              b,
              "Invalid target for element: " +
                getICAttribute(
                  b.closest(getICAttributeSelector("ic-target")),
                  "ic-target"
                ),
              "ERROR"
            );
          var i = getTransitionDuration(b, e);
          e.addClass("ic-transitioning"),
            setTimeout(function () {
              try {
                h();
              } catch (a) {
                log(
                  b,
                  "Error during content swap : " + formatError(a),
                  "ERROR"
                );
              }
              setTimeout(function () {
                try {
                  e.removeClass("ic-transitioning"),
                    _history && _history.updateHistory(),
                    triggerEvent(e, "complete_transition.ic", [e]);
                } catch (a) {
                  log(
                    b,
                    "Error during transition complete : " + formatError(a),
                    "ERROR"
                  );
                }
              }, 20);
            }, i);
        } else log(b, "Empty response, nothing to do here.", "DEBUG");
      }
      function maybeFilter(a, b) {
        var c;
        if ($.zepto) {
          var d = createDocument(a);
          c = $(d).find("body").contents();
        } else c = $($.parseHTML(a, null, !0));
        return b ? walkTree(c, b).contents() : c;
      }
      function walkTree(a, b) {
        return a.filter(b).add(a.find(b));
      }
      function fixIDs(a) {
        var b = {};
        walkTree(a, "[id]").each(function () {
          var a,
            c = $(this).attr("id");
          do {
            a = "ic-fixed-id-" + uuid();
          } while ($("#" + a).length > 0);
          (b[c] = a), $(this).attr("id", a);
        }),
          walkTree(a, "label[for]").each(function () {
            var a = $(this).attr("for");
            $(this).attr("for", b[a] || a);
          }),
          walkTree(a, "*").each(function () {
            $.each(this.attributes, function () {
              -1 !== this.value.indexOf("#") &&
                (this.value = this.value.replace(
                  /#([-_A-Za-z0-9]+)/g,
                  function (a, c) {
                    return "#" + (b[c] || c);
                  }
                ));
            });
          });
      }
      function getStyleTarget(a) {
        var b = closestAttrValue(a, "ic-target");
        return b && 0 == b.indexOf("this.style.") ? b.substr(11) : null;
      }
      function getAttrTarget(a) {
        var b = closestAttrValue(a, "ic-target");
        return b && 0 == b.indexOf("this.") ? b.substr(5) : null;
      }
      function fireICRequest(a, b) {
        a = $(a);
        var c = a;
        a.is(getICAttributeSelector("ic-src")) ||
          void 0 != getICAttribute(a, "ic-action") ||
          (a = a.closest(getICAttributeSelector("ic-src")));
        var d = closestAttrValue(a, "ic-confirm");
        if (
          (!d || confirm(d)) &&
          ("true" != closestAttrValue(a, "ic-disable-when-doc-hidden") ||
            !document.hidden) &&
          ("true" != closestAttrValue(a, "ic-disable-when-doc-inactive") ||
            document.hasFocus()) &&
          a.length > 0
        ) {
          var e = uuid();
          a.data("ic-event-id", e);
          var f = function () {
              if (1 == a.data("ic-request-in-flight"))
                return void a.data("ic-next-request", { req: f });
              if (a.data("ic-event-id") == e) {
                var d = getStyleTarget(a),
                  g = d ? null : getAttrTarget(a),
                  h = verbFor(a),
                  i = getICAttribute(a, "ic-src");
                if (i) {
                  var j =
                      b ||
                      function (b) {
                        d
                          ? a.css(d, b)
                          : g
                          ? a.attr(g, b)
                          : (processICResponse(b, a, !1, i),
                            "GET" != h &&
                              refreshDependencies(
                                getICAttribute(a, "ic-src"),
                                a
                              ));
                      },
                    k = getParametersForElement(h, a, c);
                  k && handleRemoteRequest(a, h, i, k, j);
                }
                maybeInvokeLocalAction(a, "");
              }
            },
            g = closestAttrValue(a, "ic-trigger-delay");
          g ? setTimeout(f, parseInterval(g)) : f();
        }
      }
      function maybeInvokeLocalAction(a, b) {
        var c = getICAttribute(a, "ic" + b + "-action");
        c && invokeLocalAction(a, c, b);
      }
      function invokeLocalAction(a, b, c) {
        var d = closestAttrValue(a, "ic" + c + "-action-target");
        null === d && "" !== c && (d = closestAttrValue(a, "ic-action-target"));
        var e = null;
        e = d ? getTargetImpl(a, "ic-action-target") : getTarget(a);
        var f = b.split(";"),
          g = [],
          h = 0;
        $.each(f, function (a, b) {
          var c = $.trim(b),
            d = c,
            f = [];
          c.indexOf(":") > 0 &&
            ((d = c.substr(0, c.indexOf(":"))),
            (f = computeArgs(c.substr(c.indexOf(":") + 1, c.length)))),
            "" == d ||
              ("delay" == d
                ? (null == h && (h = 0), (h += parseInterval(f[0] + "")))
                : (null == h && (h = 420),
                  g.push([h, makeApplyAction(e, d, f)]),
                  (h = null)));
        }),
          (h = 0),
          $.each(g, function (a, b) {
            (h += b[0]), setTimeout(b[1], h);
          });
      }
      function computeArgs(args) {
        try {
          return eval("[" + args + "]");
        } catch (a) {
          return [$.trim(args)];
        }
      }
      function makeApplyAction(a, b, c) {
        return function () {
          var d = a[b] || window[b];
          d ? d.apply(a, c) : log(a, "Action " + b + " was not found", "ERROR");
        };
      }
      function newIntercoolerHistory(a, b, c, d) {
        function e() {
          for (var b = [], e = 0; e < a.length; e++)
            0 == a.key(e).indexOf(r) && b.push(a.key(e));
          for (var f = 0; f < b.length; f++) a.removeItem(b[f]);
          a.removeItem(q),
            (s = { slotLimit: c, historyVersion: d, lruList: [] });
        }
        function f(b) {
          var c = s.lruList,
            d = c.indexOf(b),
            e = m($("body"));
          if (d >= 0)
            log(e, "URL found in LRU list, moving to end", "INFO"),
              c.splice(d, 1),
              c.push(b);
          else if (
            (log(e, "URL not found in LRU list, adding", "INFO"),
            c.push(b),
            c.length > s.slotLimit)
          ) {
            var f = c.shift();
            log(e, "History overflow, removing local history for " + f, "INFO"),
              a.removeItem(r + f);
          }
          return a.setItem(q, JSON.stringify(s)), c;
        }
        function g(b) {
          var d = JSON.stringify(b);
          try {
            a.setItem(b.id, d);
          } catch (f) {
            try {
              e(), a.setItem(b.id, d);
            } catch (a) {
              log(
                m($("body")),
                "Unable to save intercooler history with entire history cleared, is something else eating local storage? History Limit:" +
                  c,
                "ERROR"
              );
            }
          }
        }
        function h(a, b, c, d) {
          var e = {
            url: c,
            id: r + c,
            content: a,
            yOffset: b,
            timestamp: new Date().getTime(),
            title: d,
          };
          return f(c), g(e), e;
        }
        function i(a) {
          if (
            null == a.onpopstate ||
            1 != a.onpopstate["ic-on-pop-state-handler"]
          ) {
            var b = a.onpopstate;
            (a.onpopstate = function (a) {
              triggerEvent(m($("body")), "handle.onpopstate.ic"),
                l(a) || (b && b(a)),
                triggerEvent(m($("body")), "pageLoad.ic");
            }),
              (a.onpopstate["ic-on-pop-state-handler"] = !0);
          }
        }
        function j() {
          t &&
            (k(t.newUrl, currentUrl(), t.oldHtml, t.yOffset, t.oldTitle),
            (t = null));
        }
        function k(a, c, d, e, f) {
          var g = h(d, e, c, f);
          b.replaceState({ "ic-id": g.id }, "", "");
          var i = m($("body")),
            j = h(i.html(), window.pageYOffset, a, document.title);
          b.pushState({ "ic-id": j.id }, "", a),
            triggerEvent(i, "pushUrl.ic", [i, j]);
        }
        function l(b) {
          var c = b.state;
          if (c && c["ic-id"]) {
            var d = JSON.parse(a.getItem(c["ic-id"]));
            if (d)
              return (
                processICResponse(d.content, m($("body")), !0),
                d.yOffset &&
                  setTimeout(function () {
                    window.scrollTo(0, d.yOffset);
                  }, 100),
                d.title && (document.title = d.title),
                !0
              );
            $.get(currentUrl(), { "ic-restore-history": !0 }, function (a, b) {
              processICResponse(m(createDocument(a)).html(), m($("body")), !0);
            });
          }
          return !1;
        }
        function m(a) {
          var b = a.find(getICAttributeSelector("ic-history-elt"));
          return b.length > 0 ? b : a;
        }
        function n(a, b) {
          var c = m($("body"));
          triggerEvent(c, "beforeHistorySnapshot.ic", [c]),
            (t = {
              newUrl: a,
              oldHtml: c.html(),
              yOffset: window.pageYOffset,
              oldTitle: b,
            });
        }
        function o() {
          var b = "",
            c = [];
          for (var d in a) c.push(d);
          c.sort();
          var e = 0;
          for (var f in c) {
            var g = 2 * a[c[f]].length;
            (e += g),
              (b += c[f] + "=" + (g / 1024 / 1024).toFixed(2) + " MB\n");
          }
          return (
            b + "\nTOTAL LOCAL STORAGE: " + (e / 1024 / 1024).toFixed(2) + " MB"
          );
        }
        function p() {
          return s;
        }
        var q = "ic-history-support",
          r = "ic-hist-elt-",
          s = JSON.parse(a.getItem(q)),
          t = null;
        return (
          (function (a) {
            return (
              null == a ||
              a.slotLimit != c ||
              a.historyVersion != d ||
              null == a.lruList
            );
          })(s) &&
            (log(
              m($("body")),
              "Intercooler History configuration changed, clearing history",
              "INFO"
            ),
            e()),
          null == s && (s = { slotLimit: c, historyVersion: d, lruList: [] }),
          {
            clearHistory: e,
            updateHistory: j,
            addPopStateHandler: i,
            snapshotForHistory: n,
            _internal: {
              addPopStateHandler: i,
              supportData: p,
              dumpLocalStorage: o,
              updateLRUList: f,
            },
          }
        );
      }
      function getSlotLimit() {
        return 20;
      }
      function refresh(a) {
        return (
          "string" == typeof a || a instanceof String
            ? refreshDependencies(a)
            : fireICRequest(a),
          Intercooler
        );
      }
      function init() {
        var a = $("body");
        processNodes(a),
          fireReadyStuff(a),
          _history && _history.addPopStateHandler(window),
          $.zepto &&
            ($("body").data("zeptoDataTest", {}),
            "string" == typeof $("body").data("zeptoDataTest") &&
              log(
                null,
                "!!!! Please include the data module with Zepto!  Intercooler requires full data support to function !!!!",
                "ERROR"
              ));
      }
      "undefined" != typeof Zepto && null == $ && (window.$ = Zepto);
      var USE_DATA =
          "true" ==
          $('meta[name="intercoolerjs:use-data-prefix"]').attr("content"),
        USE_ACTUAL_HTTP_METHOD =
          "true" ==
          $('meta[name="intercoolerjs:use-actual-http-method"]').attr(
            "content"
          ),
        _MACROS = $.map(
          [
            "ic-get-from",
            "ic-post-to",
            "ic-put-to",
            "ic-patch-to",
            "ic-delete-from",
            "ic-style-src",
            "ic-attr-src",
            "ic-prepend-from",
            "ic-append-from",
            "ic-action",
          ],
          function (a) {
            return fixICAttributeName(a);
          }
        ),
        _scrollHandler = null,
        _UUID = 1,
        _readyHandlers = [],
        _isDependentFunction = function (a, b) {
          if (!a || !b) return !1;
          var c = a
              .split(/[\?#]/, 1)[0]
              .split("/")
              .filter(function (a) {
                return "" != a;
              }),
            d = b
              .split(/[\?#]/, 1)[0]
              .split("/")
              .filter(function (a) {
                return "" != a;
              });
          return (
            "" != c &&
            "" != d &&
            (d.slice(0, c.length).join("/") == c.join("/") ||
              c.slice(0, d.length).join("/") == d.join("/"))
          );
        },
        _history = null;
      try {
        _history = newIntercoolerHistory(localStorage, window.history, 20, 0.1);
      } catch (a) {
        log($("body"), "Could not initialize history", "WARN");
      }
      return (
        $.ajaxTransport &&
          $.ajaxTransport("text", function (a, b) {
            if ("#" == b.url[0]) {
              var c = fixICAttributeName("ic-local-"),
                d = $(b.url),
                e = [],
                f = 200,
                g = "OK";
              d.each(function (a, b) {
                $.each(b.attributes, function (a, b) {
                  if (b.name.substr(0, c.length) == c) {
                    var d = b.name.substring(c.length);
                    if ("status" == d) {
                      var h = b.value.match(/(\d+)\s?(.*)/);
                      null != h
                        ? ((f = h[1]), (g = h[2]))
                        : ((f = "500"), (g = "Attribute Error"));
                    } else e.push(d + ": " + b.value);
                  }
                });
              });
              var h = d.length > 0 ? d.html() : "";
              return {
                send: function (a, b) {
                  b(f, g, { html: h }, e.join("\n"));
                },
                abort: function () {},
              };
            }
            return null;
          }),
        $(function () {
          init();
        }),
        {
          refresh: refresh,
          history: _history,
          triggerRequest: fireICRequest,
          processNodes: processNodes,
          closestAttrValue: closestAttrValue,
          verbFor: verbFor,
          isDependent: isDependent,
          getTarget: getTarget,
          processHeaders: processHeaders,
          startPolling: startPolling,
          cancelPolling: cancelPolling,
          setIsDependentFunction: function (a) {
            _isDependentFunction = a;
          },
          ready: function (a) {
            _readyHandlers.push(a);
          },
          _internal: {
            init: init,
            replaceOrAddMethod: replaceOrAddMethod,
            initEventSource: function (a, b) {
              return new EventSource(a, { withCredentials: b });
            },
            globalEval: globalEval,
            getLocalURL: getLocalURL,
          },
        }
      );
    })();
  return Intercooler;
});
