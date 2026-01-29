#!/bin/bash

###############################################################################
# Skill Engine Sync Script
# 
# 将 skills 同步到指定项目
# 
# 使用方法：
#   cd ~/skill-engine
#   ./scripts/sync.sh /path/to/your-project
###############################################################################

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 检查参数
if [ $# -eq 0 ]; then
    echo -e "${RED}错误: 请指定目标项目路径${NC}"
    echo ""
    echo "使用方法："
    echo "  ./scripts/sync.sh /path/to/your-project"
    echo ""
    exit 1
fi

# 获取 skill-engine 目录（脚本所在目录的父目录）
SKILL_ENGINE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_DIR="$1"

# 检查目标目录是否存在
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}错误: 目标目录不存在: $TARGET_DIR${NC}"
    exit 1
fi

# 转换为绝对路径
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo -e "${GREEN}=== Skill Engine Sync ===${NC}"
echo "Source: $SKILL_ENGINE_DIR"
echo "Target: $TARGET_DIR"
echo ""

# 检查目标目录是否是 git 仓库
if [ ! -d "$TARGET_DIR/.git" ]; then
    echo -e "${RED}错误: 目标目录不是 Git 仓库${NC}"
    echo "请指定一个 Git 项目根目录"
    exit 1
fi

# 1. 创建 .claude 目录（如果不存在）
if [ ! -d "$TARGET_DIR/.claude" ]; then
    mkdir -p "$TARGET_DIR/.claude"
    echo -e "  ${GREEN}✓${NC} 创建 .claude 目录"
fi

# 2. 同步 skills 目录到 .claude/skills
echo -e "${YELLOW}[1/3]${NC} 同步 .claude/skills/ 目录..."
if [ -d "$TARGET_DIR/.claude/skills" ]; then
    echo "  ⚠️  .claude/skills/ 目录已存在，是否覆盖? (y/n)"
    read -r response
    response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    if [[ "$response_lower" != "y" ]]; then
        echo "  跳过 .claude/skills/"
    else
        rm -rf "$TARGET_DIR/.claude/skills"
        cp -r "$SKILL_ENGINE_DIR/skills" "$TARGET_DIR/.claude/"
        echo -e "  ${GREEN}✓${NC} .claude/skills/ 已更新"
    fi
else
    cp -r "$SKILL_ENGINE_DIR/skills" "$TARGET_DIR/.claude/"
    echo -e "  ${GREEN}✓${NC} .claude/skills/ 已复制"
fi

# 3. 复制 AGENTS.md 到项目根目录
echo -e "${YELLOW}[2/3]${NC} 复制 AGENTS.md..."
if [ -f "$TARGET_DIR/AGENTS.md" ]; then
    echo "  ⚠️  AGENTS.md 已存在，是否覆盖? (y/n)"
    read -r response
    response_lower=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    if [[ "$response_lower" != "y" ]]; then
        echo "  跳过 AGENTS.md"
    else
        cp "$SKILL_ENGINE_DIR/AGENTS.md" "$TARGET_DIR/"
        echo -e "  ${GREEN}✓${NC} AGENTS.md 已更新"
    fi
else
    cp "$SKILL_ENGINE_DIR/AGENTS.md" "$TARGET_DIR/"
    echo -e "  ${GREEN}✓${NC} AGENTS.md 已复制"
fi

# 4. 显示状态
echo -e "${YELLOW}[3/3]${NC} 检查 Git 状态..."
echo ""
(cd "$TARGET_DIR" && git status --short .claude/skills/ AGENTS.md 2>/dev/null || true)
echo ""

# 统计信息
SKILL_COUNT=$(find "$TARGET_DIR/.claude/skills" -name "*.md" ! -name "README.md" ! -name "SKILL_TEMPLATE.md" 2>/dev/null | wc -l | tr -d ' ')
echo -e "${BLUE}已同步:${NC}"
echo "  • $SKILL_COUNT 个 skills (位于 .claude/skills/)"
echo "  • AGENTS.md 配置文件"
echo ""

echo -e "${GREEN}同步完成！${NC}"
echo ""
echo "下一步（在目标项目中执行）："
echo "  cd $TARGET_DIR"
echo "  git add .claude/skills/ AGENTS.md"
echo "  git commit -m 'feat: 添加 AI skills'"
echo "  git push"
echo ""
echo -e "${GREEN}=== 完成 ===${NC}"
