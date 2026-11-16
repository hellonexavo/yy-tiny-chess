# YY Agent — make.fun worker

A general task runner, independent of the Tiny Chess entry on main.
Requires Python 3.9+, git, and an installed, authenticated Codex CLI.
No Python packages or separate paid model API keys are required.
Codex uses your existing account limits; a subscription is not unlimited usage.
Check current Codex OS requirements before installing on an older Mac.

## Start on your Mac

Install Codex from https://developers.openai.com/codex/cli/ and authenticate
with your existing ChatGPT account using `codex login`.

```sh
git clone --branch universal-agent --single-branch https://github.com/hellonexavo/yy-tiny-chess.git YY-Agent
cd YY-Agent
python3 yy_agent/agent.py scan
python3 yy_agent/agent.py work --max-tasks 1 --timeout 3600
```

Inspect or choose a specific task:

```sh
python3 yy_agent/agent.py inspect tiny-chess-01
python3 yy_agent/agent.py run tiny-chess-01 --timeout 3600
python3 yy_agent/agent.py status
```

## What runs

Discovery reads the public homepage and fetches current official requirements.
Paid or unknown entry fees and closed/expired tasks are rejected before execution.
The worker creates a private workspace per task under ~/YY-Agent-runs, runs Codex
with workspace-write sandboxing and network access, and limits wall time.
Task requirements and the exact worker prompt are saved. Codex writes its native
sessions in its own configured session directory; do not delete these. The local
events.jsonl is additional diagnostic output, not a replacement transcript.

The coding agent is asked to verify prerequisites, fetch and review the official
kit, build, test, grade, bundle native sessions and submit only free entries using
existing owner authentication. Missing login, access, recorded sessions or other
requirements must produce a blocked report. It is a general coding worker:
success on every brief is not guaranteed.

The queue skips previously attempted slugs and stops on failures, missing reports,
blocked reports and reported submissions. It is bounded, not a background service.
Rerun a selected slug explicitly if you need another development attempt.
A stale .running lock after a system crash must be removed only after checking
that no previous worker is still executing.

## Status truth

A completed Codex process is marked needs_review, not accepted or paid.
result.json is the coding agent's report. submission_verified stays false:
this version does not independently authenticate and check a submission status.
Official submission, quota, transcript eligibility, ranking and payout checks
remain make.fun's decision. Wallet registration/linking, reward claims and
financial signatures are deliberately owner actions. API integration for
independent submission-status verification is not implemented.

## Privacy and costs

Do not put wallets or private keys in this repository or workspace.
No entry fees, paid APIs, bets or purchases are authorized in the worker prompt.
This is a behavioral constraint, not a billing firewall: do not provide payment
tools or paid API credentials to the executor. Existing Codex/MCP configuration
may expose tools; review it before running on your personal computer.
Preserve native logs and use the official bundle redaction to remove personal
details. Never fabricate usage or a session transcript.

## Tests

```sh
python3 -m unittest discover -s yy_agent -p 'test_*.py' -v
```

CI runs offline tests on Python 3.9 and 3.13. It does not sign in, use Codex
credits, create platform accounts or submit competition entries.
