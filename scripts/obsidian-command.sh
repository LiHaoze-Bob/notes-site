#!/bin/sh
# 从插件入口运行，固定使用本项目的 Python 环境。
set -eu
SITE_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd -- "$SITE_ROOT"
mkdir -p "$SITE_ROOT/.runtime"
exec "$SITE_ROOT/.venv/bin/python" -u "$SITE_ROOT/scripts/site.py" "$1" --from-obsidian
