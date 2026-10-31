"""Write a course's diagrams into its lessons, each with its Draw it answer.

Usage:
  python3 insert.py <course>                      write the diagrams into the lessons
  python3 insert.py <course> --preview out.html   all diagrams on one page, to look at
        [--dark] [--only "h2 text|other h2"]

<course> is a course workspace folder, such as
knowledge-library/05-projects/know-the-system. Its diagrams are registered in
<course>/teach/diagrams/specs.py with diagrams.fig. Rerunning is safe: each
lesson's old diagram blocks are removed first.

A diagram block is the figure, given id="fig-N" (N counts the lesson's
diagrams from 1), followed by its answer as JSON when the layout records one.

Each lesson also gets one Draw it exercise, before its Recall heading: an
empty <div class="draw-it" data-fig="N"> for the first diagram whose answer
has at least DRAW_MIN_BOXES boxes, and draw.js loaded after recall.js. The
course's assets/draw.js and the Draw it part of assets/course.css are copied
from this folder, so every course runs the same marking.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagrams  # noqa: E402

BLOCK = re.compile(r'<!-- diagram -->\n.*?<!-- /diagram -->\n\n', re.S)
DRAW_BLOCK = re.compile(r'<!-- draw-it -->\n.*?<!-- /draw-it -->\n\n', re.S)
DRAW_SCRIPT = '<script src="../assets/draw.js"></script>\n'
RECALL_SCRIPT = '<script src="../assets/recall.js"></script>\n'
CSS_BLOCK = re.compile(r'\n?/\* Draw it \(assets/draw\.js\).*?/\* /Draw it \*/\n', re.S)
DRAW_MIN_BOXES = 4
HERE = Path(__file__).resolve().parent


def load_specs(course):
    path = course / "teach" / "diagrams" / "specs.py"
    spec = importlib.util.spec_from_file_location("specs", path)
    spec.loader.exec_module(importlib.util.module_from_spec(spec))
    return list(diagrams.FIGS)


def build(f, n=None):
    """The figure's HTML and its answer (or None)."""
    diagrams.WARN.clear()
    d = diagrams.D()
    f["fn"](d)
    for w in diagrams.WARN:
        print(f["lesson"][:30], "|", f["h2"], "|", w)
    if d.y > 640:
        print(f["lesson"][:30], "|", f["h2"], "| tall:", int(d.y))
    svg = d.svg(f["caption"])
    if n is not None:
        svg = svg.replace('<figure class="diagram">', f'<figure class="diagram" id="fig-{n}">', 1)
    return svg, d.answer()


def block(f, n):
    svg, answer = build(f, n)
    out = svg
    if answer:
        data = json.dumps(answer, ensure_ascii=False, separators=(",", ":"))
        out += f'\n<script type="application/json" class="draw-answer" data-fig="{n}">{data}</script>'
    return f"<!-- diagram -->\n{out}\n<!-- /diagram -->\n\n"


def preview(course, figs, out, dark, only):
    css = (course / "teach" / "assets" / "course.css").read_text()
    sel = [f for f in figs if not only or any(o in f["h2"] for o in only)]
    body = "\n".join(f'<h2>{f["lesson"]} · {f["h2"]}</h2>\n{build(f)[0]}' for f in sel)
    theme = 'data-theme="dark"' if dark else 'data-theme="light"'
    Path(out).write_text(
        f'<!doctype html><html {theme}><head><meta charset="utf-8"><style>{css}{diagrams.CSS}'
        f' main{{max-width:375px;padding:1rem 16px}} h2{{font-size:.8rem}}</style></head>'
        f'<body><main>{body}</main></body></html>')


def main(argv):
    course = Path(argv[1])
    figs = load_specs(course)
    if "--preview" in argv:
        only = argv[argv.index("--only") + 1].split("|") if "--only" in argv else None
        preview(course, figs, argv[argv.index("--preview") + 1], "--dark" in argv, only)
        return
    files, count, draw = {}, {}, {}
    for f in figs:
        p = course / "teach" / "lessons" / f["lesson"]
        if p not in files:
            s = BLOCK.sub("", DRAW_BLOCK.sub("", p.read_text()))
            files[p] = s.replace(DRAW_SCRIPT, "")
        count[p] = count.get(p, 0) + 1
        answer = build(f)[1]
        if p not in draw and answer and len(answer["boxes"]) >= DRAW_MIN_BOXES:
            draw[p] = count[p]
        s = files[p]
        h = f"<h2>{f['h2']}</h2>"
        i = s.index(h)
        j = i + len(h) + 1 if f["where"] == "top" else s.index("<h2", i + len(h))
        files[p] = s[:j] + block(f, count[p]) + s[j:]
    for p, n in draw.items():
        files[p] = add_draw_it(files[p], n, p)
    for p, s in files.items():
        p.write_text(s)
    copy_assets(course)
    answers = sum(1 for f in figs if build(f)[1])
    print(f"{len(figs)} figures in {len(files)} files, {answers} with an answer,"
          f" {len(draw)} with Draw it")


def add_draw_it(s, n, p):
    """Put lesson p's Draw it for figure n before its Recall heading."""
    if "<h2>Recall</h2>" not in s or RECALL_SCRIPT not in s:
        print(p.name, "| no Recall heading or recall.js: no Draw it")
        return s
    div = f'<!-- draw-it -->\n<div class="draw-it" data-fig="{n}"></div>\n<!-- /draw-it -->\n\n'
    s = s.replace("<h2>Recall</h2>", div + "<h2>Recall</h2>", 1)
    return s.replace(RECALL_SCRIPT, RECALL_SCRIPT + DRAW_SCRIPT, 1)


def copy_assets(course):
    assets = course / "teach" / "assets"
    (assets / "draw.js").write_text((HERE / "draw.js").read_text())
    css = assets / "course.css"
    s = CSS_BLOCK.sub("", css.read_text())
    css.write_text(s.rstrip("\n") + "\n\n" + (HERE / "draw.css").read_text())


if __name__ == "__main__":
    main(sys.argv)
