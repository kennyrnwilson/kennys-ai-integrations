import json
import re
from pathlib import Path
from typing import Any

import yaml

from marketplace_validator.models import ERROR, WARNING, Finding
from marketplace_validator.skills import parse_frontmatter

# mcp__plugin_<pluginName>_<serverName>__<toolName>
PLUGIN_TOOL = re.compile(r"^mcp__plugin_([A-Za-z0-9-]+)_[A-Za-z0-9-]+__")


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def _walk_strings(node: Any, trail: str = "") -> list[tuple[str, str]]:
    """Yield (json-ish path, value) for every string leaf in a nested structure."""
    found: list[tuple[str, str]] = []
    if isinstance(node, str):
        found.append((trail, node))
    elif isinstance(node, dict):
        for key, value in node.items():
            found.extend(_walk_strings(value, f"{trail}.{key}" if trail else str(key)))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            found.extend(_walk_strings(value, f"{trail}[{index}]"))
    return found


def validate_mcp_configs(repo_root: Path) -> list[Finding]:
    """Reject tilde-prefixed paths anywhere in a .mcp.json.

    MCP server args go straight to execve. A tilde is a shell feature and is
    NOT expanded, so "~/Library/..." creates a literal directory named "~"
    in the working directory. This is exactly how a 131 MB Chrome profile
    ended up in the repo root.
    """
    findings: list[Finding] = []
    for config_path in sorted(repo_root.glob("plugins/*/.mcp.json")):
        rel = _rel(config_path, repo_root)
        try:
            config = json.loads(config_path.read_text())
        except json.JSONDecodeError as exc:
            findings.append(Finding(ERROR, rel, f"is not valid JSON: {exc}"))
            continue

        for trail, value in _walk_strings(config):
            if value.startswith("~"):
                findings.append(
                    Finding(
                        ERROR,
                        rel,
                        f"{trail} = '{value}' starts with a tilde. Tilde is a shell "
                        f"feature and is not expanded in process arguments — use an "
                        f"absolute path or expand it at runtime.",
                    )
                )
    return findings


def _declared_plugins(repo_root: Path) -> set[str]:
    plugins_dir = repo_root / "plugins"
    if not plugins_dir.is_dir():
        return set()
    return {c.name for c in plugins_dir.iterdir() if c.is_dir() and not c.name.startswith(".")}


def _allowed_tools(frontmatter: dict) -> list[str]:
    raw = frontmatter.get("allowed-tools")
    if raw is None:
        return []
    if isinstance(raw, str):
        return [item.strip() for item in raw.split(",") if item.strip()]
    if isinstance(raw, list):
        return [str(item).strip() for item in raw]
    return []


def validate_tool_dependencies(repo_root: Path) -> list[Finding]:
    """Warn when a skill's allowed-tools names a plugin this marketplace does not ship.

    Depending on an externally-installed plugin is legitimate, but it must be a
    deliberate, documented choice rather than an accident.
    """
    declared = _declared_plugins(repo_root)
    findings: list[Finding] = []

    for skill_path in sorted(repo_root.glob("plugins/*/skills/*/SKILL.md")):
        rel = _rel(skill_path, repo_root)
        try:
            frontmatter = parse_frontmatter(skill_path.read_text())
        except yaml.YAMLError:
            continue  # already reported by validate_skill
        if not frontmatter:
            continue

        seen: set[str] = set()
        for tool in _allowed_tools(frontmatter):
            match = PLUGIN_TOOL.match(tool)
            if not match:
                continue
            plugin_name = match.group(1)
            if plugin_name in declared or plugin_name in seen:
                continue
            seen.add(plugin_name)
            findings.append(
                Finding(
                    WARNING,
                    rel,
                    f"allowed-tools references plugin '{plugin_name}', which this "
                    f"marketplace does not ship. Document it as an external "
                    f"dependency in the plugin README.",
                )
            )
    return findings
