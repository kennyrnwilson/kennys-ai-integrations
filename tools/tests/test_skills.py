from pathlib import Path

from marketplace_validator.skills import parse_frontmatter, validate_all_skills, validate_skill


def levels(findings) -> list[str]:
    return [f.level for f in findings]


def messages(findings) -> str:
    return " | ".join(f.message for f in findings)


def write_skill(repo: Path, plugin: str, skill: str, frontmatter: str, body: str = "# Body\n") -> Path:
    skill_dir = repo / "plugins" / plugin / "skills" / skill
    skill_dir.mkdir(parents=True)
    path = skill_dir / "SKILL.md"
    path.write_text(f"---\n{frontmatter}---\n\n{body}")
    return path


GOOD = "name: my-skill\ndescription: Does a specific thing. Use when the user asks for it.\n"


def test_parse_frontmatter_returns_mapping():
    assert parse_frontmatter("---\nname: x\n---\nbody") == {"name": "x"}


def test_parse_frontmatter_returns_none_without_a_block():
    assert parse_frontmatter("# Just a heading\n") is None


def test_valid_skill_produces_no_findings(repo: Path):
    path = write_skill(repo, "p", "my-skill", GOOD)
    assert validate_skill(path, repo) == []


def test_missing_frontmatter_is_an_error(repo: Path):
    skill_dir = repo / "plugins" / "p" / "skills" / "bare"
    skill_dir.mkdir(parents=True)
    path = skill_dir / "SKILL.md"
    path.write_text("# No frontmatter here\n")
    findings = validate_skill(path, repo)
    assert "error" in levels(findings)
    assert "frontmatter" in messages(findings)


def test_missing_description_is_an_error(repo: Path):
    path = write_skill(repo, "p", "my-skill", "name: my-skill\n")
    findings = validate_skill(path, repo)
    assert "error" in levels(findings)
    assert "description" in messages(findings)


def test_name_must_match_directory(repo: Path):
    path = write_skill(repo, "p", "on-disk", "name: in-frontmatter\ndescription: d\n")
    findings = validate_skill(path, repo)
    assert "error" in levels(findings)
    assert "on-disk" in messages(findings)
    assert "in-frontmatter" in messages(findings)


def test_overlong_description_is_a_warning(repo: Path):
    path = write_skill(repo, "p", "my-skill", f"name: my-skill\ndescription: {'x' * 1100}\n")
    findings = validate_skill(path, repo)
    assert levels(findings) == ["warning"]
    assert "1024" in messages(findings)


def test_malformed_yaml_is_an_error(repo: Path):
    path = write_skill(repo, "p", "my-skill", "name: [unclosed\n")
    findings = validate_skill(path, repo)
    assert "error" in levels(findings)


def test_validate_all_skills_walks_every_plugin(repo: Path):
    write_skill(repo, "alpha", "one", "name: one\ndescription: d\n")
    write_skill(repo, "beta", "two", "name: WRONG\ndescription: d\n")
    findings = validate_all_skills(repo)
    assert "error" in levels(findings)
    assert "two" in messages(findings)
