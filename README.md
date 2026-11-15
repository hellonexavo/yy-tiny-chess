# YY Tiny Chess — 4 KB Python chess bot

[![make.fun Tiny Chess bounty](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01)
[![YY Tiny Chess rank](https://make.fun/badge/tiny-chess-01/hellonexavo/yy-tiny-chess/rank.svg)](https://make.fun/bounty/tiny-chess-01)
[![YY Tiny Chess reward](https://make.fun/badge/tiny-chess-01/hellonexavo/yy-tiny-chess/reward.svg)](https://make.fun/bounty/tiny-chess-01)

A compact Python chess agent using the make.fun game/move protocol. The bot chooses a move from the legal moves returned by the environment.

## Run

```sh
MAKEFUN_ENV_URL="<competition environment URL>" python3 main.py
```

Offline checks: `python3 -m unittest discover -p 'test_chess.py' -v`.

Competition: https://make.fun/bounty/tiny-chess-01

This repository is **not** proof of an accepted make.fun entry. A signed submission with authentic agent-session transcripts is still required.
