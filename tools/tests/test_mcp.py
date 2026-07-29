import json
from pathlib import Path

from marketplace_validator.mcp import validate_mcp_configs, validate_tool_dependencies


def levels(findings) -> list[str]:
    return [f.level for f in findings]


def messages(findings) -> str:
    return " | ".join(f.message for f in findings)


def write_mcp(repo: Path, plugin: str, config: dict) -> Path:
    plugin_dir = repo / "plugins" / plugin
    plugin_dir.mkdir(parents=True, exist_ok=True)
    path = plugin_dir / ".mcp.json"
    path.write_text(json.dumps(config))
    return path


def write_skill(repo: Path, plugin: str, skill: str, frontmatter: str) -> Path:
    skill_dir = repo / "plugins" / plugin / "skills" / skill
    skill_dir.mkdir(parents=True)
    path = skill_dir / "SKILL.md"
    path.write_text(f"---\n{frontmatter}---\n\n# Body\n")
    return path


def test_absolute_paths_produce_no_findings(repo: Path):
    write_mcp(repo, "p", {"mcpServers": {"s": {"command": "npx",
                                               "args": ["pkg", "--dir", "/tmp/profile"]}}})
    assert validate_mcp_configs(repo) == []


def test_tilde_in_args_is_an_error(repo: Path):
    # The exact image-gen defect that created a 131MB ./~/ directory.
    write_mcp(
        repo,
        "image-gen",
        {"mcpServers": {"playwright": {"command": "npx",
                                       "args": ["@playwright/mcp@latest", "--user-data-dir",
                                                "~/Library/Caches/ms-playwright/profile"]}}},
    )
    findings = validate_mcp_configs(repo)
    assert "error" in levels(findings)
    assert "tilde" in messages(findings).lower()
    assert "--user-data-dir" in messages(findings) or "~/Library" in messages(findings)


def test_tilde_inside_a_nested_env_value_is_also_caught(repo: Path):
    write_mcp(repo, "p", {"mcpServers": {"s": {"command": "x", "args": [],
                                               "env": {"PROFILE": "~/somewhere"}}}})
    findings = validate_mcp_configs(repo)
    assert "error" in levels(findings)


def test_known_plugin_dependency_produces_no_findings(repo: Path):
    (repo / "plugins" / "playwright").mkdir(parents=True)
    write_skill(repo, "image-gen", "gen",
                "name: gen\ndescription: d\n"
                "allowed-tools: Read, mcp__plugin_playwright_playwright__browser_click\n")
    assert validate_tool_dependencies(repo) == []


def test_unknown_plugin_dependency_is_a_warning(repo: Path):
    write_skill(repo, "image-gen", "gen",
                "name: gen\ndescription: d\n"
                "allowed-tools: Read, mcp__plugin_playwright_playwright__browser_click\n")
    findings = validate_tool_dependencies(repo)
    assert levels(findings) == ["warning"]
    assert "playwright" in messages(findings)


def test_allowed_tools_accepts_a_yaml_list(repo: Path):
    write_skill(repo, "image-gen", "gen",
                "name: gen\ndescription: d\n"
                "allowed-tools:\n"
                "  - Read\n"
                "  - mcp__plugin_ghost_server__do_thing\n")
    findings = validate_tool_dependencies(repo)
    assert levels(findings) == ["warning"]
    assert "ghost" in messages(findings)


def test_builtin_tools_are_ignored(repo: Path):
    write_skill(repo, "p", "s", "name: s\ndescription: d\nallowed-tools: Read, Write, Bash, Glob\n")
    assert validate_tool_dependencies(repo) == []
