/*
 * Course workspaces: Draw it. Redraw one of the lesson's diagrams from memory
 * in Excalidraw, and have the drawing marked in the browser against the
 * diagram's answer. The attempt is then saved by learning-app
 * (POST /learning-api/drawing). There is no model call.
 *
 * Usage in a lesson, written by lesson-diagrams/insert.py:
 *   <figure class="diagram" id="fig-2"> … </figure>
 *   <script type="application/json" class="draw-answer" data-fig="2">{…}</script>
 *   …
 *   <div class="draw-it" data-fig="2"></div>     (before the Recall heading)
 *   <script src="../assets/draw.js"></script>
 *
 * The div is empty, so a lesson opened from a file, in Obsidian or on GitHub
 * shows nothing. Over http(s) the script builds the exercise in it. Excalidraw
 * loads only when the learner taps Start drawing.
 *
 * Marking reads boxes and arrows, not positions:
 *  - a box is a rectangle, ellipse, diamond or frame; its label is the text
 *    bound to it, a frame's name, or free text inside a box with no label;
 *  - a box is inside the smallest box that contains it;
 *  - an arrow's ends are the boxes it is snapped to.
 * A drawn label names an answer box when it holds all the words of the box's
 * label or of one of its other names (aka), or a word that no other box in
 * the answer uses.
 */
(function () {
  "use strict";

  var VENDOR = "/vendor/excalidraw/0.18.1/";
  var TIMEOUT_MS = 15000;
  var LABELS = { "got-it": "Got it", "partly": "Partly", "not-yet": "Not yet" };
  var SHAPES = { rectangle: 1, ellipse: 1, diamond: 1, frame: 1 };
  var SKIP = { the: 1, a: 1, an: 1, on: 1, or: 1, of: 1, "in": 1, to: 1, and: 1 };

  // ---- Marking -------------------------------------------------------------

  function words(s) {
    return String(s).toLowerCase().replace(/[^a-z0-9.:]+/g, " ").split(" ")
      .map(function (w) { return w.replace(/^[.:]+|[.:]+$/g, ""); })
      .filter(function (w) { return w && !SKIP[w]; });
  }

  function inside(a, b) {
    return a !== b && a.x >= b.x && a.y >= b.y &&
      a.x + a.width <= b.x + b.width && a.y + a.height <= b.y + b.height;
  }

  function smallest(list) {
    return list.sort(function (p, q) { return p.width * p.height - q.width * q.height; })[0] || null;
  }

  // Boxes, each with a label and the box it sits in; arrows, each with the
  // boxes at its two ends (null when an end is not snapped onto a box).
  function read(elements) {
    var live = elements.filter(function (e) { return !e.isDeleted; });
    var byId = {};
    live.forEach(function (e) { byId[e.id] = e; });
    var shapes = live.filter(function (e) { return SHAPES[e.type]; });
    var label = {};
    shapes.forEach(function (s) { if (s.type === "frame" && s.name) label[s.id] = s.name; });
    live.forEach(function (t) {
      if (t.type === "text" && t.containerId && byId[t.containerId]) label[t.containerId] = t.text;
    });
    // Free text inside a box with no label of its own labels that box: the
    // natural way to name an outer wall without centring text across it.
    live.forEach(function (t) {
      if (t.type !== "text" || t.containerId) return;
      var box = smallest(shapes.filter(function (s) { return inside(t, s); }));
      if (box && !label[box.id]) label[box.id] = t.text;
    });
    var boxes = shapes.map(function (s) {
      var parent = smallest(shapes.filter(function (p) { return inside(s, p) || s.frameId === p.id; }));
      return { id: s.id, label: (label[s.id] || "").replace(/\s+/g, " ").trim(), parent: parent ? parent.id : null };
    });
    var arrows = live.filter(function (e) { return e.type === "arrow"; }).map(function (a) {
      function end(b) { return b && byId[b.elementId] && SHAPES[byId[b.elementId].type] ? b.elementId : null; }
      return { from: end(a.startBinding), to: end(a.endBinding) };
    });
    return { boxes: boxes, arrows: arrows };
  }

  // Words that only one answer box uses, across its label and its akas.
  function uniqueWords(answer) {
    var owners = {};
    answer.boxes.forEach(function (b) {
      var seen = {};
      [b.label].concat(b.aka || []).forEach(function (n) {
        words(n).forEach(function (w) { seen[w] = 1; });
      });
      Object.keys(seen).forEach(function (w) { (owners[w] = owners[w] || []).push(b.id); });
    });
    var only = {};
    Object.keys(owners).forEach(function (w) { if (owners[w].length === 1) only[w] = owners[w][0]; });
    return only;
  }

  // How well a drawn label names an answer box: the number of words in the
  // longest of its names whose words all appear in the label; else 0.5 when
  // the label holds a word only this box uses; else 0.
  function score(drawn, box, only) {
    var have = words(drawn), set = {};
    have.forEach(function (w) { set[w] = 1; });
    var best = 0;
    [box.label].concat(box.aka || []).forEach(function (name) {
      var need = words(name);
      if (need.length && need.every(function (w) { return set[w]; })) best = Math.max(best, need.length);
    });
    if (!best && have.some(function (w) { return only[w] === box.id; })) best = 0.5;
    return best;
  }

  function mark(elements, answer) {
    var got = read(elements);
    var only = uniqueWords(answer);
    var pairs = [];
    got.boxes.forEach(function (d) {
      answer.boxes.forEach(function (a) {
        var s = d.label ? score(d.label, a, only) : 0;
        if (s) pairs.push({ d: d, a: a, s: s });
      });
    });
    pairs.sort(function (p, q) { return q.s - p.s; });
    var toAnswer = {}, toDrawn = {};
    pairs.forEach(function (p) {
      if (toAnswer[p.d.id] || toDrawn[p.a.id]) return;
      toAnswer[p.d.id] = p.a.id; toDrawn[p.a.id] = p.d;
    });
    var name = {};
    answer.boxes.forEach(function (a) { name[a.id] = a.label; });
    function drawnName(id) {
      var d = got.boxes.filter(function (b) { return b.id === id; })[0];
      return d && d.label ? "“" + d.label + "”" : "a box with no label";
    }

    var ok = [], bad = [];
    answer.boxes.forEach(function (a) {
      var d = toDrawn[a.id];
      if (!d) { bad.push("Missing box: " + a.label); return; }
      var parent = d.parent ? toAnswer[d.parent] || "?" : null;
      if (parent === (a.inside || null)) {
        ok.push(a.label + (a.inside ? ", inside " + name[a.inside] : ""));
      } else if (!a.inside) {
        bad.push(a.label + " should not be inside " + (parent === "?" ? drawnName(d.parent) : name[parent]));
      } else {
        bad.push(a.label + " should be inside " + name[a.inside]);
      }
    });
    got.boxes.forEach(function (d) {
      if (!toAnswer[d.id]) bad.push("Extra box: " + drawnName(d.id));
    });

    var want = {};
    answer.arrows.forEach(function (r) { want[r[0] + ">" + r[1]] = 1; });
    var seen = {}, flipped = {};
    got.arrows.forEach(function (r) {
      if (!r.from || !r.to) { bad.push("An arrow joins nothing at one end: drop both ends on a box"); return; }
      var f = toAnswer[r.from], t = toAnswer[r.to];
      if (f && t && want[f + ">" + t]) { seen[f + ">" + t] = 1; return; }
      if (f && t && want[t + ">" + f]) { flipped[t + ">" + f] = 1; bad.push("Wrong way: " + name[f] + " → " + name[t] + " should point the other way"); return; }
      bad.push("Extra arrow: " + (f ? name[f] : drawnName(r.from)) + " → " + (t ? name[t] : drawnName(r.to)));
    });
    answer.arrows.forEach(function (r) {
      var k = r[0] + ">" + r[1];
      if (seen[k]) ok.push(name[r[0]] + " → " + name[r[1]]);
      else if (!flipped[k]) bad.push("Missing arrow: " + name[r[0]] + " → " + name[r[1]]);
    });

    var verdict = !bad.length ? "got-it" : ok.length > bad.length ? "partly" : "not-yet";
    return { verdict: verdict, ok: ok, bad: bad, read: got };
  }

  // ---- The exercise --------------------------------------------------------

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }

  function button(text) {
    var b = el("button", null, text);
    b.type = "button";
    return b;
  }

  // A tap counts on pointerup as well as click: while Excalidraw is open, a
  // touch can lose its click.
  function onTap(b, fn) {
    var last = 0;
    function run(e) {
      var now = Date.now();
      if (now - last < 500 || b.disabled) return;
      last = now; e.preventDefault(); fn();
    }
    b.addEventListener("pointerup", run);
    b.addEventListener("click", run);
  }

  // The lesson's path inside the course projects, as recall.js sends it.
  function lessonPath() {
    var p = decodeURIComponent(location.pathname);
    var marker = "/knowledge/projects/";
    var i = p.indexOf(marker);
    return i >= 0 ? p.slice(i + marker.length) : p.replace(/^\//, "");
  }

  // What is saved with the attempt: the live elements, without freehand
  // points, which can be large and are never marked.
  function saved(elements) {
    return elements.filter(function (e) { return !e.isDeleted; }).slice(0, 500).map(function (e) {
      var c = {};
      Object.keys(e).forEach(function (k) { if (!(e.type === "freedraw" && k === "points")) c[k] = e[k]; });
      return c;
    });
  }

  function post(fig, r, elements) {
    var ctrl = window.AbortController ? new AbortController() : null;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, TIMEOUT_MS);
    return fetch("/learning-api/drawing", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        lesson: lessonPath(), fig: fig, verdict: r.verdict,
        ok: r.ok, bad: r.bad, elements: saved(elements)
      }),
      signal: ctrl ? ctrl.signal : undefined
    }).then(function (res) {
      clearTimeout(timer);
      if (!res.ok) throw new Error("status " + res.status);
    }, function (e) { clearTimeout(timer); throw e; });
  }

  var loading = null;
  function loadExcalidraw() {
    if (loading) return loading;
    window.EXCALIDRAW_ASSET_PATH = VENDOR;
    var css = el("link");
    css.rel = "stylesheet"; css.href = VENDOR + "draw-vendor.css";
    document.head.appendChild(css);
    loading = import(VENDOR + "draw-vendor.js");
    loading.catch(function () { loading = null; });
    return loading;
  }

  function build(host) {
    var fig = host.getAttribute("data-fig");
    var figure = document.getElementById("fig-" + fig);
    var data = document.querySelector('script.draw-answer[data-fig="' + fig + '"]');
    if (!figure || !data) return;
    var answer = JSON.parse(data.textContent);
    var caption = figure.querySelector("figcaption");

    host.appendChild(el("h2", null, "Draw it"));
    var intro = el("p", null, "Redraw this lesson's diagram from memory" +
      (caption ? ": “" + caption.textContent.trim() + "”" : ".") +
      " Start drawing hides the diagram until you check.");
    host.appendChild(intro);
    var how = el("details", "box draw-how");
    how.appendChild(el("summary", null, "How to draw it"));
    var ul = el("ul");
    [
      "Draw a box for each thing, and double-tap the box to type its name. Short names are fine.",
      "To put a box inside another, draw it inside. For a big outer box, write its name as text near its top edge, inside it.",
      "Draw each arrow from one box to the next. Drop each end on a box, so that the box outline lights up.",
      "Where things sit does not count: only the boxes, their names, what is inside what, and the arrows."
    ].forEach(function (t) { ul.appendChild(el("li", null, t)); });
    how.appendChild(ul);
    host.appendChild(how);

    var bar = el("div", "draw-bar");
    var start = button("Start drawing"), full = button("Full screen"), check = button("Check");
    full.disabled = check.disabled = true;
    bar.appendChild(start); bar.appendChild(full); bar.appendChild(check);
    host.appendChild(bar);
    var status = el("p", "draw-status");
    status.setAttribute("aria-live", "polite");
    host.appendChild(status);
    var area = el("div", "draw-area");
    host.appendChild(area);
    var fullBar = el("div", "draw-bar draw-full-bar");
    var check2 = button("Check"), done = button("Done");
    fullBar.appendChild(check2); fullBar.appendChild(done);
    host.appendChild(fullBar);
    var out = el("div", "recall-out");
    out.setAttribute("aria-live", "polite");
    host.appendChild(out);

    var drawing = null;

    function setFull(on) {
      area.classList.toggle("is-full", on);
      document.body.style.overflow = on ? "hidden" : "";
      if (drawing) setTimeout(drawing.refresh, 50);
    }

    // On a phone, a stroke that starts at the screen's left edge is the
    // browser's swipe back, which would leave the lesson and lose the drawing.
    // A history entry of the lesson's own takes that first back: it only
    // leaves full screen. A second back leaves the lesson as usual.
    var guarded = false;
    function guard() {
      if (guarded || !window.history || !history.pushState) return;
      guarded = true;
      history.pushState({ drawIt: fig }, "");
    }
    window.addEventListener("popstate", function () {
      if (!guarded) return;
      guarded = false;
      setFull(false);
      status.textContent = "Back again leaves this lesson, and the drawing with it.";
    });

    onTap(start, function () {
      start.disabled = true;
      guard();
      figure.hidden = true;
      out.className = "recall-out"; out.textContent = "";
      status.textContent = "Loading the drawing tool…";
      loadExcalidraw().then(function () {
        area.classList.add("is-open");
        drawing = window.LessonDraw.mount(area, function () {
          status.textContent = "";
          full.disabled = check.disabled = false;
        });
      }, function () {
        status.textContent = "Could not load the drawing tool. Try again.";
        figure.hidden = false;
        start.disabled = false;
      });
    });
    onTap(full, function () { guard(); status.textContent = ""; setFull(true); });
    onTap(done, function () { setFull(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && area.classList.contains("is-full")) setFull(false);
    });

    function runCheck() {
      if (!drawing) return;
      setFull(false);
      var elements = drawing.getElements();
      var r = mark(elements, answer);
      out.className = "recall-out is-" + r.verdict;
      out.textContent = "";
      out.appendChild(el("strong", "recall-verdict", LABELS[r.verdict]));
      var list = el("ul", "recall-points");
      r.bad.forEach(function (s) { list.appendChild(el("li", "is-missed", "✗ " + s)); });
      r.ok.forEach(function (s) { list.appendChild(el("li", "is-made", "✓ " + s)); });
      out.appendChild(list);
      // The diagram again, beside the mark, to compare.
      var copy = figure.cloneNode(true);
      copy.removeAttribute("id");
      copy.hidden = false;
      var d = el("details", "box draw-compare");
      d.open = true;
      d.appendChild(el("summary", null, "The diagram"));
      d.appendChild(copy);
      out.appendChild(d);
      figure.hidden = false;
      check.textContent = "Check again";
      var note = el("p", "draw-status");
      out.appendChild(note);
      post(fig, r, elements).then(null, function () {
        note.textContent = "This attempt could not be saved. The mark above still stands.";
      });
      out.scrollIntoView({ behavior: "smooth", block: "start" });
    }
    onTap(check, runCheck);
    onTap(check2, runCheck);
  }

  function mount() {
    if (!/^https?:$/.test(location.protocol)) return;
    Array.prototype.forEach.call(document.querySelectorAll("div.draw-it[data-fig]"), build);
  }

  // For tests: the marker without the page.
  window.DrawIt = { read: read, mark: mark };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mount);
  } else {
    mount();
  }
})();
