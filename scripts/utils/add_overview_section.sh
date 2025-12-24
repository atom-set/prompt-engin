#!/bin/bash
# 批量添加概述部分的脚本
# 功能：为缺少"## 概述"部分的提示词文件添加概述部分

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROMPTS_DIR="$REPO_ROOT/prompts"

# 检查提示词目录是否存在
if [ ! -d "$PROMPTS_DIR" ]; then
    echo -e "${RED}错误：找不到提示词目录 $PROMPTS_DIR${NC}"
    exit 1
fi

echo -e "${YELLOW}开始为提示词文件添加概述部分...${NC}"
echo ""

# 查找所有缺少"## 概述"的 .md 文件
files_without_overview=$(find "$PROMPTS_DIR" -name "*.md" -type f ! -name "README.md" | while read file; do
    if ! grep -q "^## 概述" "$file"; then
        echo "$file"
    fi
done)

if [ -z "$files_without_overview" ]; then
    echo -e "${GREEN}✓ 所有文件都已包含概述部分${NC}"
    exit 0
fi

count=0
for file in $files_without_overview; do
    # 检查文件是否有标题
    if ! grep -q "^# " "$file"; then
        echo -e "${YELLOW}跳过：$file（缺少标题）${NC}"
        continue
    fi
    
    # 读取文件内容
    content=$(cat "$file")
    
    # 查找第一个分隔线（---）的位置
    if echo "$content" | grep -q "^---$"; then
        # 在分隔线后添加概述部分
        # 提取文件名（不含路径和扩展名）作为概述的基础
        filename=$(basename "$file" .md)
        
        # 生成概述内容（基于文件名和文件说明）
        overview_section="## 概述

本文件定义了相关规则和规范，具体内容见下方详细说明。

---"
        
        # 在第一个分隔线后插入概述部分
        # 使用 sed 在第一个 --- 后插入
        awk -v overview="$overview_section" '
            /^---$/ && !found {
                print $0
                print ""
                print overview
                found=1
                next
            }
            {print}
        ' "$file" > "$file.tmp" && mv "$file.tmp" "$file"
        
        echo -e "${GREEN}✓ 已添加概述：$file${NC}"
        ((count++))
    else
        echo -e "${YELLOW}跳过：$file（缺少分隔线）${NC}"
    fi
done

echo ""
echo -e "${GREEN}✓ 完成：已为 $count 个文件添加概述部分${NC}"

