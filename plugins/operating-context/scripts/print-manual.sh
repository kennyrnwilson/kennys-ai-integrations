#!/usr/bin/env bash
# Print the bundled operating manual so the agent adds it to the session.
# SessionStart stdout becomes session context. No network; if the file is
# missing, print nothing and exit cleanly so a session is never blocked.
set -euo pipefail

manual="${CLAUDE_PLUGIN_ROOT:-}/operating-manual.md"
if [[ -f "$manual" ]]; then
  cat "$manual"
fi
exit 0
