import json
from pathlib import Path

from marketplace_validator.manifest import validate_plugin_manifest

from conftest import write_plugin


def levels(findings) -> list[str]:
    return [f.level for f in findings]


def messages(findings) -> str:
    return " | ".join(f.message for f in findings)


def test_valid_manifest_produces_no_findings(repo: Path):
    manifest = write_plugin(repo, "good-plugin")
    assert validate_plugin_manifest(manifest, repo) == []


def test_missing_required_field_is_an_error(repo: Path):
    manifest = write_plugin(
        repo, "no-version", {"name": "no-version", "description": "x", "author": {"name": "k"}}
    )
    findings = validate_plugin_manifest(manifest, repo)
    assert "error" in levels(findings)
    assert "version" in messages(findings)


def test_name_must_match_directory_name(repo: Path):
    manifest = write_plugin(
        repo,
        "actual-dir",
        {
            "name": "claimed-name",
            "version": "1.0.0",
            "description": "x",
            "author": {"name": "k"},
            "repository": "r",
            "license": "MIT",
            "keywords": ["k"],
        },
    )
    findings = validate_plugin_manifest(manifest, repo)
    assert "error" in levels(findings)
    assert "claimed-name" in messages(findings)
    assert "actual-dir" in messages(findings)


def test_non_semver_version_is_an_error(repo: Path):
    manifest = write_plugin(
        repo,
        "bad-version",
        {
            "name": "bad-version",
            "version": "1.0",
            "description": "x",
            "author": {"name": "k"},
            "repository": "r",
            "license": "MIT",
            "keywords": ["k"],
        },
    )
    findings = validate_plugin_manifest(manifest, repo)
    assert "error" in levels(findings)
    assert "semver" in messages(findings).lower()


def test_missing_recommended_field_is_only_a_warning(repo: Path):
    # This is exactly the mermaid-diagrams defect: no repository/license/keywords.
    manifest = write_plugin(
        repo,
        "sparse",
        {"name": "sparse", "version": "1.0.0", "description": "x", "author": {"name": "k"}},
    )
    findings = validate_plugin_manifest(manifest, repo)
    assert levels(findings) == ["warning", "warning", "warning"]
    assert "error" not in levels(findings)


def test_malformed_json_is_an_error(repo: Path):
    manifest = write_plugin(repo, "broken")
    manifest.write_text("{ not json")
    findings = validate_plugin_manifest(manifest, repo)
    assert "error" in levels(findings)
