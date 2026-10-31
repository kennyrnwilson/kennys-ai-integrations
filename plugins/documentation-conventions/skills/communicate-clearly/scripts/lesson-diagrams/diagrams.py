"""Inline SVG diagrams for the course lessons, drawn with the course.css tokens.

Every shape carries a class (.d-box, .d-t, .d-line ...) that course.css maps to
var(--surface), var(--text) and so on, so the diagrams follow light and dark mode.

The layouts that show structure (chain, row, fan, tree, nested, cycle) also
record it: the boxes, which box is inside which, and the arrows. That record is
the answer a Draw it exercise marks a drawing against (D.answer). A diagram
drawn with any other layout, with hand-placed shapes, or with a red "this does
not happen" arrow has no answer.

A course's specs file registers its diagrams with @fig; insert.py writes them
into the lessons.
"""
import html as _h
import json
import math

W = 360          # viewBox width
M = 10           # outer margin
LH_T, LH_S = 16, 14   # line heights: title, sub
CW_T, CW_S = 7.4, 6.1  # rough character widths at 13px bold and 11px
PAD = 8
WARN = []


def esc(s):
    return _h.escape(s, quote=True)


def wrap(s, px, cw):
    out = []
    n = max(3, int(px // cw))
    for para in s.split("\n"):
        cur = ""
        for w in para.split():
            t = f"{cur} {w}" if cur else w
            if len(t) <= n or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def norm(item):
    """str | (title, sub, cls, note)."""
    if isinstance(item, dict):
        return item
    if isinstance(item, str):
        item = (item,)
    t = list(item) + [None] * 4
    return dict(title=t[0], sub=t[1], cls=t[2] or "d-box", note=t[3])


FIGS = []


def fig(lesson, h2, where, caption):
    """Register a diagram: the lesson file, the <h2> it belongs to, "top" (just
    after the heading) or "end" (end of that section), and its caption."""
    def deco(fn):
        FIGS.append(dict(lesson=lesson, h2=h2, where=where, caption=caption, fn=fn))
        return fn
    return deco


def layout(fn):
    """Marks a structural layout: shapes it draws are recorded, not free."""
    def run(self, *a, **k):
        self._depth += 1
        try:
            return fn(self, *a, **k)
        finally:
            self._depth -= 1
    run.__doc__ = fn.__doc__
    return run


class D:
    def __init__(self):
        self.el = []
        self.y = M
        self.nodes = []      # [{id, label, aka, inside}]
        self.arrows = []     # [(from_id, to_id)]
        self.free = False    # drawn with something that records no structure
        self._depth = 0
        self._aka = {}

    # structure ----------------------------------------------------------
    def _free(self):
        if not self._depth:
            self.free = True

    def node(self, label, inside=None):
        label = " ".join(label.split())
        nid = f"b{len(self.nodes) + 1}"
        self.nodes.append(dict(id=nid, label=label, inside=inside))
        return nid

    def arrow(self, a, b):
        self.arrows.append((a, b))

    def aka(self, names):
        """Other names a learner may give a box: {label: [name, ...]}."""
        self._aka.update(names)

    def answer(self):
        """The diagram's structure for a Draw it exercise, or None."""
        if self.free or not self.nodes:
            return None
        boxes = []
        for n in self.nodes:
            b = dict(id=n["id"], label=n["label"])
            aka = list(self._aka.get(n["label"], []))
            # "The house, 192.168.0.x": the part before the comma is the name.
            if ", " in n["label"]:
                b["label"], rest = n["label"].split(", ", 1)
                aka.append(rest)
            if aka:
                b["aka"] = aka
            if n["inside"]:
                b["inside"] = n["inside"]
            boxes.append(b)
        return dict(boxes=boxes, arrows=[list(a) for a in self.arrows])

    # primitives ---------------------------------------------------------
    def rect(self, x, y, w, h, cls="d-box", rx=6):
        self._free()
        self.el.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}"/>')

    def text(self, x, y, s, cls="d-t", anchor="middle", extra=""):
        self.el.append(f'<text class="{cls}" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}"{extra}>{esc(s)}</text>')

    def lines(self, x, y, lines, cls, lh, anchor="middle"):
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, cls, anchor)

    def line(self, pts, head=True, cls="", dash=False):
        self._free()
        if "d-badl" in cls:
            self.free = True   # a "this does not happen" arrow: no answer
        c = "d-line" + (" d-dash" if dash else "") + (f" {cls}" if cls else "")
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.el.append(f'<polyline class="{c}" points="{p}"/>')
        if head:
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            self.head(x2, y2, x2 - x1, y2 - y1, cls)

    def head(self, x, y, dx, dy, cls=""):
        d = math.hypot(dx, dy) or 1
        ux, uy = dx / d, dy / d
        nx, ny = -uy, ux
        a = (x - 7 * ux + 3.8 * nx, y - 7 * uy + 3.8 * ny)
        b = (x - 7 * ux - 3.8 * nx, y - 7 * uy - 3.8 * ny)
        c = "d-head" + (f" {cls}" if cls else "")
        self.el.append(f'<polygon class="{c}" points="{x:.1f},{y:.1f} {a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f}"/>')

    def measure(self, w, it):
        it = norm(it)
        tl = wrap(it["title"], w - 2 * PAD, CW_T)
        sl = wrap(it["sub"], w - 2 * PAD, CW_S) if it["sub"] else []
        h = 2 * PAD + len(tl) * LH_T + (len(sl) * LH_S + 2 if sl else 0)
        return h, tl, sl

    def box(self, x, y, w, it, h=None, align="middle"):
        it = norm(it)
        h0, tl, sl = self.measure(w, it)
        h = h or h0
        for ln in tl:
            if len(ln) * CW_T > w - 6:
                WARN.append(f"title too wide ({w:.0f}px): {ln}")
        for ln in sl:
            if len(ln) * CW_S > w - 6:
                WARN.append(f"sub too wide ({w:.0f}px): {ln}")
        self.rect(x, y, w, h, it["cls"])
        self.last = self.node(it["title"])
        ty = y + (h - h0) / 2 + PAD + 12
        tx = x + w / 2 if align == "middle" else x + PAD + 2
        self.lines(tx, ty, tl, "d-t", LH_T, align)
        if sl:
            self.lines(tx, ty + len(tl) * LH_T + 1, sl, "d-s", LH_S, align)
        return h

    def note(self, s, cls="d-s"):
        ls = wrap(s, W - 2 * M, CW_S)
        self.lines(W / 2, self.y + 11, ls, cls, LH_S)
        self.y += len(ls) * LH_S + 6

    def space(self, n=10):
        self.y += n

    # layouts ------------------------------------------------------------
    @layout
    def chain(self, items, w=250, gap=26, via=None, loop=None, x=None):
        """Vertical boxes joined by arrows.
        via: labels for the arrows (len n-1, None to skip).
        loop: (from_index, to_index, label): an arrow back up the right side.
        An item's note is written to the right of its box."""
        items = [norm(i) for i in items]
        has_notes = any(i["note"] for i in items)
        if has_notes:
            w = min(w, 190)
            x0 = M
        elif loop:
            x0 = (W - w) / 2 - 22
        else:
            x0 = (W - w) / 2 if x is None else x
        cx = x0 + w / 2
        mids, ids = [], []
        for i, it in enumerate(items):
            if i:
                lbl = via[i - 1] if via else None
                g = gap + (6 if lbl else 0)
                self.line([(cx, self.y), (cx, self.y + g)])
                if lbl:
                    self.text(cx + 8, self.y + g / 2 + 4, lbl, "d-l", "start")
                self.y += g
            h = self.box(x0, self.y, w, it)
            ids.append(self.last)
            if i:
                self.arrow(ids[-2], ids[-1])
            mids.append(self.y + h / 2)
            if it["note"]:
                nx = x0 + w + 12
                ls = wrap(it["note"], W - M - nx, CW_S)
                self.lines(nx, self.y + h / 2 - (len(ls) - 1) * LH_S / 2 + 4, ls, "d-s", LH_S, "start")
            self.y += h
        if loop:
            a, b, lbl = loop[:3]
            bad = len(loop) > 3
            self.arrow(ids[a], ids[b])
            rx = x0 + w
            lx = rx + 24
            self.line([(rx, mids[a]), (lx, mids[a]), (lx, mids[b]), (rx + 1, mids[b])],
                      cls="d-badl" if bad else "", dash=bad)
            my = (mids[a] + mids[b]) / 2
            self.text(lx + 12, my, lbl, "d-bad-t" if bad else "d-l", "middle", f' transform="rotate(90 {lx + 12:.1f} {my:.1f})"')
        self.y += M

    @layout
    def row(self, items, gap=22, arrows=True, back=None, via=None):
        """Boxes side by side. back: label for a red dashed arrow from last to first."""
        n = len(items)
        w = (W - 2 * M - (n - 1) * gap) / n
        h = max(self.measure(w, i)[0] for i in items)
        y = self.y
        ids = []
        for k, it in enumerate(items):
            x = M + k * (w + gap)
            self.box(x, y, w, it, h)
            ids.append(self.last)
            if arrows and k:
                self.arrow(ids[-2], ids[-1])
                self.line([(x - gap + 2, y + h / 2), (x - 2, y + h / 2)])
                if via and via[k - 1]:
                    self.text(x - gap / 2, y + h / 2 - 6, via[k - 1], "d-l")
        self.y += h
        if back:
            x1, x2 = M + (n - 1) * (w + gap) + w / 2, M + w / 2
            yb = self.y + 18
            self.line([(x1, self.y), (x1, yb), (x2, yb), (x2, self.y + 2)], cls="d-badl", dash=True)
            self.text(W / 2, yb + 15, back, "d-bad-t")
            self.y = yb + 20
        self.y += M

    @layout
    def fan(self, root, children, rootw=112, gap=8, inward=False, elbow=None):
        """A root on the left, its children stacked on the right."""
        cx0 = M + rootw + 30
        cw = W - M - cx0
        hs = [self.measure(cw, c)[0] for c in children]
        total = sum(hs) + gap * (len(hs) - 1)
        rh = self.measure(rootw, root)[0]
        top = self.y
        tall = max(total, rh)
        ry = top + (tall - rh) / 2
        self.box(M, ry, rootw, root, rh)
        rid = self.last
        y = top + (tall - total) / 2
        rx, rmid = M + rootw, ry + rh / 2
        ex = rx + 15
        for c, h in zip(children, hs):
            self.box(cx0, y, cw, c, h)
            self.arrow(self.last, rid) if inward else self.arrow(rid, self.last)
            cm = y + h / 2
            if inward:
                self.line([(cx0, cm), (ex, cm), (ex, rmid), (rx + 1, rmid)])
            else:
                self.line([(rx, rmid), (ex, rmid), (ex, cm), (cx0 - 1, cm)])
            y += h + gap
        self.y = top + tall + M

    @layout
    def tree(self, root, children, below=None, edge=None, rootw=220, gap=10, up=False):
        """A root on top, children in a row beneath. below: per-child item under it."""
        rh = self.measure(rootw, root)[0]
        rx = (W - rootw) / 2
        self.box(rx, self.y, rootw, root, rh)
        rid = self.last
        ids = []
        rb = self.y + rh
        n = len(children)
        cw = (W - 2 * M - (n - 1) * gap) / n
        ch = max(self.measure(cw, c)[0] for c in children)
        cy = rb + (40 if edge else 30)
        midy = rb + 12
        for k, c in enumerate(children):
            x = M + k * (cw + gap)
            ccx = x + cw / 2
            self.box(x, cy, cw, c, ch)
            ids.append(self.last)
            self.arrow(self.last, rid) if up else self.arrow(rid, self.last)
            if up:
                self.line([(ccx, cy), (ccx, midy), (W / 2, midy), (W / 2, rb + 1)])
            else:
                self.line([(W / 2, rb), (W / 2, midy), (ccx, midy), (ccx, cy - 1)])
            if edge and edge[k]:
                self.text(ccx + 5, cy - 8, edge[k], "d-l", "start")
        self.y = cy + ch
        if below:
            bh = max((self.measure(cw, b)[0] for b in below if b), default=0)
            if bh:
                by = self.y + 26
                for k, b in enumerate(below):
                    if not b:
                        continue
                    x = M + k * (cw + gap)
                    self.line([(x + cw / 2, self.y), (x + cw / 2, by - 1)])
                    self.box(x, by, cw, b, bh)
                    self.arrow(ids[k], self.last)
                self.y = by + bh
        self.y += M

    def columns(self, cols, gap=10, flow=False):
        """cols: [(header_item, [items])]. flow: arrows down between items."""
        self.free = True
        n = len(cols)
        cw = (W - 2 * M - (n - 1) * gap) / n
        hh = max(self.measure(cw, h)[0] for h, _ in cols)
        vg = 18 if flow else 6
        depth = max(len(items) for _, items in cols)
        rh = [max(self.measure(cw, items[i])[0] for _, items in cols if i < len(items))
              for i in range(depth)]
        bottom = self.y
        for k, (hdr, items) in enumerate(cols):
            x = M + k * (cw + gap)
            y = self.y
            self.box(x, y, cw, hdr, hh)
            y += hh
            for i, it in enumerate(items):
                if flow:
                    self.line([(x + cw / 2, y), (x + cw / 2, y + vg)])
                y += vg
                y += self.box(x, y, cw, it, rh[i])
            bottom = max(bottom, y)
        self.y = bottom + M

    def ladder(self, rows, tagw=70, gap=6):
        """rows: (tag, text, cls). A tag box on the left, its text on the right."""
        self.free = True
        tx = M + tagw + 6
        tw = W - M - tx
        for tag, txt, cls in rows:
            h = max(self.measure(tw, (txt,))[0], self.measure(tagw, (tag,))[0])
            self.box(M, self.y, tagw, (tag, None, cls), h)
            self.box(tx, self.y, tw, (txt,), h, align="start")
            self.y += h + gap
        self.y += M - gap

    @layout
    def nested(self, layers, inner, step_x=12, step_y=26):
        """layers: labels from the outside in; inner: items in a row inside the last."""
        n = len(layers)
        iw = W - 2 * (M + n * step_x)
        top = self.y
        iy = top + n * step_y + 2
        k = len(inner)
        g = 8
        bw = (iw - (k - 1) * g) / k
        ih = max(self.measure(bw, i)[0] for i in inner)
        parent = None
        for i, lbl in enumerate(layers):
            parent = self.node(lbl, inside=parent)
            x = M + i * step_x
            y = top + i * step_y
            h = iy + ih + (n - i) * 10 - y
            self.rect(x, y, W - 2 * x, h, "d-wall", 8)
            self.text(x + 9, y + 17, lbl, "d-wl", "start")
        for j, it in enumerate(inner):
            self.box(M + n * step_x + j * (bw + g), iy, bw, it, ih)
            self.nodes[-1]["inside"] = parent
        self.y = iy + ih + n * 10 + M

    @layout
    def cycle(self, items, rx=118, ry=None, bw=104, center=None):
        n = len(items)
        hs = [self.measure(bw, i)[0] for i in items]
        mh = max(hs)
        ry = ry or rx
        cx, cy = W / 2, self.y + mh / 2 + ry
        self.el.append(f'<ellipse class="d-line" cx="{cx}" cy="{cy:.1f}" rx="{rx}" ry="{ry:.1f}"/>')
        for k in range(n):
            m = math.radians(-90 + (k + 0.5) * 360 / n)
            px, py = cx + rx * math.cos(m), cy + ry * math.sin(m)
            self.head(px, py, -rx * math.sin(m), ry * math.cos(m))
        for k, (it, h) in enumerate(zip(items, hs)):
            a = math.radians(-90 + k * 360 / n)
            px, py = cx + rx * math.cos(a), cy + ry * math.sin(a)
            self.box(px - bw / 2, py - mh / 2, bw, it, mh)
        ids = [nd["id"] for nd in self.nodes[-n:]]
        for k in range(n):
            self.arrow(ids[k], ids[(k + 1) % n])
        if center:
            self.lines(cx, cy - 2, wrap(center, 84, CW_S), "d-l", LH_S)
        self.y = cy + ry + mh / 2 + M

    def versus(self, left, right, verdict):
        self.free = True
        self.row([left, right], gap=34, arrows=False)
        self.y -= M
        self.text(W / 2, self.y - 18, "vs", "d-l")
        vy = self.y + 24
        self.line([(W / 4, self.y), (W / 4, vy - 8), (W / 2, vy - 8)], head=False)
        self.line([(3 * W / 4, self.y), (3 * W / 4, vy - 8), (W / 2, vy - 8), (W / 2, vy - 1)])
        self.y = vy
        self.y += self.box(M + 30, vy, W - 2 * M - 60, verdict) + M

    # output -------------------------------------------------------------
    def svg(self, caption):
        h = math.ceil(self.y)
        body = "\n".join(self.el)
        return (f'<figure class="diagram">\n'
                f'<svg viewBox="0 0 {W} {h}" role="img" aria-label="{esc(caption)}">\n{body}\n</svg>\n'
                f'<figcaption>{esc(caption)}</figcaption>\n</figure>')


CSS = """
/* Diagrams: inline SVG in the page's own colours (follows dark mode) */
figure.diagram { margin: 1.5rem auto 1.75rem; max-width: 30rem; }
figure.diagram svg { display: block; width: 100%; height: auto; }
figure.diagram figcaption { font-family: var(--sans); font-size: .8rem; color: var(--muted);
  margin-top: .5rem; line-height: 1.4; }
.d-box { fill: var(--surface); stroke: var(--rule); stroke-width: 1.2; }
.d-accent { fill: var(--surface); stroke: var(--accent); stroke-width: 1.8; }
.d-good { fill: var(--good-bg); stroke: var(--good); stroke-width: 1.2; }
.d-bad { fill: var(--bad-bg); stroke: var(--bad); stroke-width: 1.2; }
.d-ghost { fill: none; stroke: var(--muted); stroke-width: 1; stroke-dasharray: 4 3; }
.d-wall { fill: none; stroke: var(--accent); stroke-width: 1.2; stroke-opacity: .55; }
.d-t { font-family: var(--sans); font-size: 13px; font-weight: 600; fill: var(--text); }
.d-s { font-family: var(--sans); font-size: 11px; fill: var(--muted); }
.d-l { font-family: var(--sans); font-size: 11px; font-style: italic; fill: var(--accent); }
.d-wl { font-family: var(--sans); font-size: 11px; font-weight: 600; fill: var(--accent); }
.d-bad-t { font-family: var(--sans); font-size: 11px; font-weight: 600; fill: var(--bad); }
.d-line { fill: none; stroke: var(--muted); stroke-width: 1.4; }
.d-dash { stroke-dasharray: 4 3; }
.d-head { fill: var(--muted); }
.d-line.d-badl { stroke: var(--bad); }
.d-head.d-badl { fill: var(--bad); }
"""
