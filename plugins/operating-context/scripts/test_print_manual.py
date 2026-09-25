import subprocess
from pathlib import Path

SCRIPT = Path(__file__).parent / "print-manual.sh"


def _run(plugin_root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [str(SCRIPT)],
        env={"CLAUDE_PLUGIN_ROOT": str(plugin_root), "PATH": "/usr/bin:/bin"},
        capture_output=True,
        text=True,
        check=False,
    )


def test_prints_manual_when_present(tmp_path):
    (tmp_path / "operating-manual.md").write_text("# Operating manual\n\nbody\n")
    result = _run(tmp_path)
    assert result.returncode == 0
    assert result.stdout.startswith("# Operating manual")


def test_prints_instructions_before_manual(tmp_path):
    (tmp_path / "standing-instructions.md").write_text("# Standing instructions\n")
    (tmp_path / "operating-manual.md").write_text("# Operating manual\n")
    result = _run(tmp_path)
    assert result.returncode == 0
    assert result.stdout.startswith("# Standing instructions")
    assert result.stdout.index("# Operating manual") > 0


def test_silent_when_missing(tmp_path):
    result = _run(tmp_path)
    assert result.returncode == 0
    assert result.stdout == ""
