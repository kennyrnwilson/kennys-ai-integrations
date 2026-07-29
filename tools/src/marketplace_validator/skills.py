from pathlib import Path

import yaml

from marketplace_validator.models import ERROR, WARNING, Finding

MAX_DESCRIPTION_CHARS = 1024


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def parse_frontmatter(text: str) -> dict | None:
    """Return the YAML frontmatter mapping, or None if the file has no --- block.

    Raises yaml.YAMLError if the block is present but malformed.
    """
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    loaded = yaml.safe_load(parts[1])
    return loaded if isinstance(loaded, dict) else {}


def validate_skill(skill_path: Path, repo_root: Path) -> list[Finding]:
    """Validate one plugins/<plugin>/skills/<skill>/SKILL.md."""
    rel = _rel(skill_path, repo_root)

    try:
        frontmatter = parse_frontmatter(skill_path.read_text())
    except yaml.YAMLError as exc:
        return [Finding(ERROR, rel, f"frontmatter is not valid YAML: {exc}")]

    if frontmatter is None:
        return [Finding(ERROR, rel, "has no YAML frontmatter block")]

    findings: list[Finding] = []

    directory_name = skill_path.parent.name
    name = frontmatter.get("name")
    if not name:
        findings.append(Finding(ERROR, rel, "frontmatter is missing required field 'name'"))
    elif name != directory_name:
        findings.append(
            Finding(
                ERROR,
                rel,
                f"frontmatter name '{name}' does not match directory name '{directory_name}'",
            )
        )

    description = frontmatter.get("description")
    if not description:
        findings.append(Finding(ERROR, rel, "frontmatter is missing required field 'description'"))
    elif len(description) > MAX_DESCRIPTION_CHARS:
        findings.append(
            Finding(
                WARNING,
                rel,
                f"description is {len(description)} chars; keep it under "
                f"{MAX_DESCRIPTION_CHARS} — it is loaded into every session's context",
            )
        )

    return findings


def validate_all_skills(repo_root: Path) -> list[Finding]:
    """Validate every SKILL.md under plugins/*/skills/*/."""
    findings: list[Finding] = []
    for skill_path in sorted(repo_root.glob("plugins/*/skills/*/SKILL.md")):
        findings.extend(validate_skill(skill_path, repo_root))
    return findings
