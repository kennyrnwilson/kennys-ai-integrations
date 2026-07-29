import argparse
import sys
from pathlib import Path

from marketplace_validator.manifest import validate_marketplace
from marketplace_validator.mcp import validate_mcp_configs, validate_tool_dependencies
from marketplace_validator.models import ERROR
from marketplace_validator.skills import validate_all_skills


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate the plugin marketplace structure.")
    parser.add_argument(
        "repo_root",
        nargs="?",
        default=".",
        type=Path,
        help="Path to the marketplace repository root (default: current directory)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors",
    )
    args = parser.parse_args(argv)
    root = args.repo_root.resolve()

    findings = [
        *validate_marketplace(root),
        *validate_all_skills(root),
        *validate_mcp_configs(root),
        *validate_tool_dependencies(root),
    ]

    errors = [f for f in findings if f.level == ERROR]
    warnings = [f for f in findings if f.level != ERROR]

    for finding in errors + warnings:
        print(finding, file=sys.stderr if finding.level == ERROR else sys.stdout)

    print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")

    if errors:
        return 1
    if warnings and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
