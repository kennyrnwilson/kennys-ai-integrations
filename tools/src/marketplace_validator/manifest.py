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
