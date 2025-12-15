#!/bin/bash

# 提示词验证脚本
# 功能：验证 prompts/ 目录下的提示词文件格式
# 使用方式：在项目根目录运行此脚本

set -e  # 遇到错误立即退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROMPTS_DIR="$REPO_ROOT/prompts"

# 检查提示词目录是否存在
if [ ! -d "$PROMPTS_DIR" ]; then
    echo -e "${YELLOW}错误：找不到提示词目录 $PROMPTS_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}开始验证提示词文件...${NC}"
echo ""

# 验证计数器
valid_count=0
invalid_count=0
total_count=0

# 验证单个文件的函数
validate_file() {
    local file_path="$1"
    local errors=()
    
    # 检查文件是否存在
    if [ ! -f "$file_path" ]; then
        errors+=("文件不存在")
        return 1
    fi
    
    # 读取文件内容
    local content
    content=$(cat "$file_path")
    
    # 检查是否有标题（以 # 开头）
    if ! echo "$content" | grep -q "^# "; then
        errors+=("缺少标题（应以 # 开头）")
    fi
    
    # 检查是否有概述部分
    if ! echo "$content" | grep -q "^## 概述"; then
        errors+=("缺少概述部分（## 概述）")
    fi
    
    # 检查内容是否为空
    if [ -z "$(echo "$content" | tr -d '[:space:]')" ]; then
        errors+=("文件内容为空")
    fi
    
    # 输出验证结果
    if [ ${#errors[@]} -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $file_path"
        return 0
    else
        echo -e "${RED}✗${NC} $file_path"
        for error in "${errors[@]}"; do
            echo -e "  ${RED}-${NC} $error"
        done
        return 1
    fi
}

# 验证所有提示词文件
find "$PROMPTS_DIR" -name "*.md" -type f ! -name "README.md" | while read -r file_path; do
    ((total_count++))
    if validate_file "$file_path"; then
        ((valid_count++))
    else
        ((invalid_count++))
    fi
done

# 显示统计信息
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}验证完成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}有效：${NC}$valid_count"
echo -e "${RED}无效：${NC}$invalid_count"
echo -e "${BLUE}总计：${NC}$total_count"
echo ""

# 如果有无效文件，退出码为 1
if [ $invalid_count -gt 0 ]; then
    exit 1
fi

