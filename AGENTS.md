## Project Overview

## Agent Protocol

- Fix root cause (not band-aid). Band-aids accumulate and cause cascading issues.
- Unsure: read more code; if still stuck, ask w/ short options.
- Conflicts: call out; pick safer path.
- Write idiomatic, simple, maintainable code. Always ask yourself if this is the most simple intuitive solution to the problem.
- If code is very confusing or hard to understand:
  1. Try to simplify it.
  2. Add an ASCII art diagram in a code comment if it would help.
- No breadcrumbs. If you delete or move code, do not leave a comment in the old place. No "// moved to X", no "relocated". Just remove it. Git history is the source of truth for code movement; comments go stale.
- Clean up unused code ruthlessly. Dead code misleads about what's active and bloats the codebase. If a function no longer needs a parameter or a helper is dead, delete it and update the callers instead of letting the junk linger.

## Git

- Safe by default: `git status/diff/log`. Push only when user asks.
- Branch changes require user consent.
- Don't commit, and push; stop + ask.
- Don’t delete/rename unexpected stuff; stop + ask.
- No amend unless asked.

## Commit Message

@agent-rules/commit-message.md

