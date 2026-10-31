// Tests for draw.js's marking, against real lesson answers.
//   node test_draw.mjs
import { readFileSync } from "node:fs";
import vm from "node:vm";
import assert from "node:assert/strict";

const ctx = { window: {}, document: { readyState: "complete" }, location: { protocol: "file:" } };
vm.runInNewContext(readFileSync(new URL("./draw.js", import.meta.url), "utf8"), ctx);
const { mark } = ctx.window.DrawIt;

// Know the system, lesson 5, figure 1: a chain of arrows.
const chain = {"boxes":[{"id":"b1","label":"claude.ai or a cloud session"},{"id":"b2","label":"Cloudflare edge"},{"id":"b3","label":"Access"},{"id":"b4","label":"The tunnel"},{"id":"b5","label":"The ingress VM on the Mini"}],"arrows":[["b1","b2"],["b2","b3"],["b3","b4"],["b4","b5"]]};
// Lesson 6, figure 1: boxes inside boxes.
const walls = {"boxes":[{"id":"b1","label":"The house","aka":["192.168.0.x"]},{"id":"b2","label":"OrbStack's network","aka":["192.168.139.x"],"inside":"b1"},{"id":"b3","label":"The VM: ingress","inside":"b2"},{"id":"b4","label":"Loopback","aka":["127.0.0.1"],"inside":"b3"},{"id":"b5","label":"nginx on :80","inside":"b4"}],"arrows":[]};

let n = 0;
const els = [];
function box(label, x, y, w = 100, h = 40) {
  const id = "e" + ++n;
  els.push({ id, type: "rectangle", x, y, width: w, height: h });
  if (label) els.push({ id: id + "t", type: "text", containerId: id, text: label, x, y, width: 10, height: 10 });
  return id;
}
function arrow(from, to) {
  els.push({ id: "a" + ++n, type: "arrow", startBinding: from && { elementId: from }, endBinding: to && { elementId: to } });
}
function reset() { els.length = 0; n = 0; }

function drawChain(labels) {
  reset();
  const ids = labels.map((l, i) => box(l, 0, i * 60));
  for (let i = 0; i + 1 < ids.length; i++) arrow(ids[i], ids[i + 1]);
  return ids;
}

const tests = {
  "all right, with short names"() {
    drawChain(["claude.ai", "Cloudflare edge", "Access", "Tunnel", "VM"]);
    const r = mark(els, chain);
    assert.equal(r.verdict, "got-it", r.bad.join("; "));
  },
  "a word only one box uses is enough"() {
    drawChain(["cloud session", "edge", "Access", "tunnel", "ingress"]);
    assert.equal(mark(els, chain).verdict, "got-it");
  },
  "a reversed arrow"() {
    const ids = drawChain(["claude.ai", "Cloudflare edge", "Access", "Tunnel", "VM"]);
    els.pop();
    arrow(ids[4], ids[3]);
    const r = mark(els, chain);
    assert.deepEqual([...r.bad], ["Wrong way: The ingress VM on the Mini → The tunnel should point the other way"]);
    assert.equal(r.verdict, "partly");
  },
  "an unsnapped arrow"() {
    const ids = drawChain(["claude.ai", "Cloudflare edge", "Access", "Tunnel", "VM"]);
    els.pop();
    arrow(ids[3], null);
    const r = mark(els, chain);
    assert.ok(r.bad.includes("An arrow joins nothing at one end: drop both ends on a box"));
    assert.ok(r.bad.includes("Missing arrow: The tunnel → The ingress VM on the Mini"));
  },
  "a missing box and an extra box"() {
    drawChain(["claude.ai", "Cloudflare edge", "Tunnel", "VM", "Router"]);
    const r = mark(els, chain);
    assert.ok(r.bad.includes("Missing box: Access"));
    assert.ok(r.bad.includes("Extra box: “Router”"));
  },
  "nested walls, outer wall named by free text"() {
    reset();
    const house = box(null, 0, 0, 400, 300);
    els.push({ id: "ht", type: "text", text: "house", x: 5, y: 5, width: 40, height: 10 });
    box("OrbStack network", 10, 20, 380, 270);
    box("VM", 20, 40, 360, 240);
    box("loopback", 30, 60, 340, 200);
    box("nginx", 40, 80, 100, 40);
    assert.ok(house);
    assert.equal(mark(els, walls).verdict, "got-it", mark(els, walls).bad.join("; "));
  },
  "a box in the wrong wall"() {
    reset();
    box("house", 0, 0, 400, 300);
    box("OrbStack network", 10, 20, 380, 270);
    box("VM", 20, 40, 360, 240);
    box("loopback", 30, 60, 340, 200);
    box("nginx", 500, 80, 100, 40);
    assert.deepEqual([...mark(els, walls).bad], ["nginx on :80 should be inside Loopback"]);
  },
  "a drawing as text, for Design it"() {
    reset();
    box("house", 0, 0, 400, 300);
    const mini = box("Mini", 10, 20, 200, 100);
    const router = box("router", 250, 20, 100, 40);
    arrow(mini, router);
    arrow(router, null);
    assert.equal(ctx.window.DrawIt.describe(ctx.window.DrawIt.read(els)),
      "Boxes:\n- house\n- Mini, inside house\n- router, inside house\n" +
      "Arrows:\n- Mini → router\n- router → nothing");
  },
};

let failed = 0;
for (const [name, fn] of Object.entries(tests)) {
  try { fn(); console.log("ok  ", name); } catch (e) { failed++; console.log("FAIL", name, "\n     ", e.message); }
}
process.exit(failed ? 1 : 0);
