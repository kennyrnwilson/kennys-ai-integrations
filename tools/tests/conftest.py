import json
from pathlib import Path

import pytest


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """An empty marketplace skeleton that tests fill in as needed."""
    (tmp_path / ".claude-plugin").mkdir()
    (tmp_path / "plugins").mkdir()
    return tmp_path


def write_plugin(repo: Path, name: str, manifest: dict | None = None) -> Path:
    """Create plugins/<name>/.claude-plugin/plugin.json and return the manifest path."""
    plugin_dir = repo / "plugins" / name
    (plugin_dir / ".claude-plugin").mkdir(parents=True)
    if manifest is None:
        manifest = {
            "name": name,
            "version": "1.0.0",
            "description": "A test plugin.",
            "author": {"name": "kennyrnwilson"},
            "repository": "https://github.com/kennyrnwilson/kennys-ai-integrations",
            "license": "MIT",
            "keywords": ["test"],
        }
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    manifest_path.write_text(json.dumps(manifest))
    return manifest_path
