# Validation and submission blockers

Checks performed against the changes based on commit
`9a347536969f0dee728107d318160c08bb3e4ecc`:

- Python 3.13.5: five unittest cases pass; syntax compilation passes.
- Docker Engine 29.9.2: the same five tests pass in `python:3.13-slim`
  with networking disabled and the repository mounted read-only.
- `main.py` is 4089 bytes, within the repository's 4096-byte check.
- An offline HTTP stub verified `/game`, legal `/move`, and completion.
  This is a protocol smoke check, not official practice grading.
- The promotion regression fails on the base revision: it selects a queen
  promotion that immediately loses the queen. The corrected evaluation
  accounts for the promoted piece's value. Castling evaluation also moves
  the rook on the simulated board.

The environment proxy rejects `https://make.fun/skill.md` with HTTP 403
(`CONNECT tunnel failed`). Current `tiny-chess-01` requirements and the
official kit could therefore not be retrieved. Official `bundle --dry-run`,
any applicable `--codex-cloud` mode, and practice grading were not run.

No authentic session transcript was found in the inspected accessible
workspace and temporary directories; `/workspace/.codex` was empty.
Official bundle discovery remains untested. No transcript, timestamps, or
usage records were synthesized. These validation notes are not a session
transcript and must not be supplied as one.

No make.fun submission or prize eligibility has been confirmed.
