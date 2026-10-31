"""Checks that the layouts record the right answers. Run: python3 test_diagrams.py"""
from diagrams import D


def answer(draw):
    d = D()
    draw(d)
    return d.answer()


def test_chain_with_loop():
    a = answer(lambda d: d.chain(["Read", "Rank", ("Measure", "scorecards")], loop=(2, 1, "feeds back")))
    assert [b["label"] for b in a["boxes"]] == ["Read", "Rank", "Measure"]
    assert a["arrows"] == [["b1", "b2"], ["b2", "b3"], ["b3", "b2"]]


def test_red_arrow_means_no_answer():
    assert answer(lambda d: d.chain(["A", "B", "C"], loop=(2, 0, "never", "bad"))) is None
    assert answer(lambda d: d.row(["A", "B"], back="never")) is None


def test_nested():
    a = answer(lambda d: d.nested(["The house, 192.168.0.x", "The VM"], ["nginx", "uv"]))
    assert a["boxes"] == [
        {"id": "b1", "label": "The house", "aka": ["192.168.0.x"]},
        {"id": "b2", "label": "The VM", "inside": "b1"},
        {"id": "b3", "label": "nginx", "inside": "b2"},
        {"id": "b4", "label": "uv", "inside": "b2"},
    ]
    assert a["arrows"] == []


def test_tree_up_and_below():
    a = answer(lambda d: d.tree("main", ["Mini", "Air"], below=["serve/", None], up=True))
    assert a["arrows"] == [["b2", "b1"], ["b3", "b1"], ["b2", "b4"]]


def test_fan_inward_and_cycle():
    assert answer(lambda d: d.fan("hub", ["x", "y"], inward=True))["arrows"] == [["b2", "b1"], ["b3", "b1"]]
    assert answer(lambda d: d.cycle(["a", "b", "c"]))["arrows"] == [["b1", "b2"], ["b2", "b3"], ["b3", "b1"]]


def test_free_shapes_mean_no_answer():
    assert answer(lambda d: d.columns([("H", ["a"])])) is None
    assert answer(lambda d: (d.chain(["A", "B"]), d.box(10, 10, 50, "loose"))) is None


def test_aka():
    def draw(d):
        d.aka({"The ingress VM on the Mini": ["VM"]})
        d.chain(["Edge", "The ingress VM on the Mini"])
    assert answer(draw)["boxes"][1]["aka"] == ["VM"]


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
