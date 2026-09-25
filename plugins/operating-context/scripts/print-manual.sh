#!/usr/bin/env bash
# Print the standing instructions, then the operating manual, so the agent adds
# both to the session. SessionStart stdout becomes session context. The
# instructions come first so they read as instructions, not as background. No
# network; a missing file prints nothing, so a session is never blocked.
set -euo pipefail

root="${CLAUDE_PLUGIN_ROOT:-}"
first=1
for doc in standing-instructions.md operating-manual.md; do
  if [[ -f "$root/$doc" ]]; then
    [[ $first -eq 1 ]] || printf '\n---\n\n'
    cat "$root/$doc"
    first=0
  fi
done
exit 0
