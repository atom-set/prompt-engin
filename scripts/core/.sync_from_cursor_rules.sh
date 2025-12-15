#!/bin/bash

# 从 cursor-rules 同步提示词到当前工程
# 这是一个隐藏工具，仅用于内部使用

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 运行 Python 脚本
python3 "$SCRIPT_DIR/.sync_from_cursor_rules.py" "$@"

