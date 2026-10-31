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
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import diagrams  # noqa: E402

BLOCK = re.compile(r'<!-- diagram -->\n.*?<!-- /diagram -->\n\n', re.S)


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
    files, count = {}, {}
    for f in figs:
        p = course / "teach" / "lessons" / f["lesson"]
        if p not in files:
            files[p] = BLOCK.sub("", p.read_text())
        count[p] = count.get(p, 0) + 1
        s = files[p]
        h = f"<h2>{f['h2']}</h2>"
        i = s.index(h)
        j = i + len(h) + 1 if f["where"] == "top" else s.index("<h2", i + len(h))
        files[p] = s[:j] + block(f, count[p]) + s[j:]
    for p, s in files.items():
        p.write_text(s)
    answers = sum(1 for f in figs if build(f)[1])
    print(f"{len(figs)} figures in {len(files)} files, {answers} with an answer")


if __name__ == "__main__":
    main(sys.argv)
