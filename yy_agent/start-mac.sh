#!/bin/bash
set -eu
cd -- "$(dirname -- "$0")/.."
if ! command -v python3 >/dev/null 2>&1; then
  echo "Потрібен Python 3.9 або новіший. Запуск зупинено."
  exit 1
fi
python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else "Потрібен Python 3.9 або новіший")'
if ! command -v git >/dev/null 2>&1; then
  echo "Потрібен Git. Запуск зупинено."
  exit 1
fi
if ! command -v codex >/dev/null 2>&1; then
  echo "Потрібно встановити Codex CLI: https://developers.openai.com/codex/cli/"
  echo "Після встановлення повтори цю команду."
  exit 1
fi
if ! codex login status; then
  echo "Увійди у свій ChatGPT-акаунт у вікні Codex."
  codex login
fi
python3 -m unittest discover -s yy_agent -p 'test_*.py' -v
echo "Запуск черги: до 100 знайдених безкоштовних завдань, до години на кожне."
echo "Черга зупиниться на помилці, блокуванні або подачі, що потребує перевірки."
echo "Результати: $HOME/YY-Agent-runs"
echo "Зупинка: Ctrl+C"
exec python3 yy_agent/agent.py work --max-tasks 100 --timeout 3600
