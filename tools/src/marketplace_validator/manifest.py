import json
import re
from pathlib import Path

from marketplace_validator.models import ERROR, WARNING, Finding

REQUIRED_FIELDS = ("name", "version", "description", "author")
RECOMMENDED_FIELDS = ("repository", "license", "keywords")
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?$")


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def validate_plugin_manifest(manifest_path: Path, repo_root: Path) -> list[Finding]:
    """Validate one plugins/<name>/.claude-plugin/plugin.json."""
    rel = _rel(manifest_path, repo_root)
    try:
        data = json.loads(manifest_path.read_text())
    except json.JSONDecodeError as exc:
        return [Finding(ERROR, rel, f"is not valid JSON: {exc}")]

    findings: list[Finding] = []

    for field in REQUIRED_FIELDS:
        if not data.get(field):
            findings.append(Finding(ERROR, rel, f"missing required field '{field}'"))

    for field in RECOMMENDED_FIELDS:
        if not data.get(field):
            findings.append(Finding(WARNING, rel, f"missing recommended field '{field}'"))

    # plugin_dir is .../plugins/<name>/.claude-plugin/plugin.json -> up two levels
    directory_name = manifest_path.parent.parent.name
    claimed = data.get("name")
    if claimed and claimed != directory_name:
        findings.append(
            Finding(
                ERROR,
                rel,
                f"name '{claimed}' does not match directory name '{directory_name}'",
            )
        )

    version = data.get("version")
    if version and not SEMVER.match(str(version)):
        findings.append(
            Finding(ERROR, rel, f"version '{version}' is not semver (expected MAJOR.MINOR.PATCH)")
        )

    return findings


def validate_marketplace(repo_root: Path) -> list[Finding]:
    """Validate marketplace.json and every plugin manifest, and cross-check them."""
    marketplace_path = repo_root / ".claude-plugin" / "marketplace.json"
    rel = _rel(marketplace_path, repo_root)

    if not marketplace_path.exists():
        return [Finding(ERROR, rel, "marketplace manifest is missing")]

    try:
        catalog = json.loads(marketplace_path.read_text())
    except json.JSONDecodeError as exc:
        return [Finding(ERROR, rel, f"is not valid JSON: {exc}")]

    findings: list[Finding] = []

    plugins_dir = repo_root / "plugins"
    on_disk: set[str] = set()
    if plugins_dir.is_dir():
        for child in sorted(plugins_dir.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            on_disk.add(child.name)
            manifest_path = child / ".claude-plugin" / "plugin.json"
            if not manifest_path.exists():
                findings.append(
                    Finding(ERROR, _rel(child, repo_root), "has no .claude-plugin/plugin.json")
                )
                continue
            findings.extend(validate_plugin_manifest(manifest_path, repo_root))

    listed: set[str] = set()
    for entry in catalog.get("plugins", []):
        name = entry.get("name")
        if not name:
            findings.append(Finding(ERROR, rel, "a plugins[] entry has no 'name'"))
            continue
        listed.add(name)

        source = entry.get("source", "")
        if not source:
            findings.append(Finding(ERROR, rel, f"'{name}' has no 'source'"))
        elif not (repo_root / source).is_dir():
            findings.append(
                Finding(ERROR, rel, f"'{name}' source '{source}' does not resolve to a directory")
            )

    for name in sorted(on_disk - listed):
        findings.append(
            Finding(ERROR, rel, f"plugin directory '{name}' exists but is not listed in plugins[]")
        )
    for name in sorted(listed - on_disk):
        findings.append(
            Finding(ERROR, rel, f"plugins[] lists '{name}' but plugins/{name}/ does not exist")
        )

    return findings
