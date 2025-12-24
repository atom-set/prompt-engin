#!/bin/bash
# 环境测试脚本
# 功能：检查环境是否正确配置，包括 Python 版本、依赖包、CLI 工具等

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 测试结果统计
PASSED=0
FAILED=0
WARNINGS=0
TOTAL=0

# 测试函数
test_check() {
    local name="$1"
    local command="$2"
    local expected_exit_code="${3:-0}"
    
    TOTAL=$((TOTAL + 1))
    echo -n "  [$TOTAL] $name ... "
    
    if eval "$command" > /tmp/test_env_output.log 2>&1; then
        exit_code=$?
    else
        exit_code=$?
    fi
    
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ 失败${NC}"
        if [ -s /tmp/test_env_output.log ]; then
            echo -e "    ${YELLOW}错误信息:${NC}"
            cat /tmp/test_env_output.log | sed 's/^/    /' | head -5
        fi
        FAILED=$((FAILED + 1))
        return 1
    fi
}

# 警告检查函数
test_warning() {
    local name="$1"
    local command="$2"
    
    TOTAL=$((TOTAL + 1))
    echo -n "  [$TOTAL] $name ... "
    
    if eval "$command" > /tmp/test_env_output.log 2>&1; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${YELLOW}⚠ 警告${NC}"
        if [ -s /tmp/test_env_output.log ]; then
            echo -e "    ${YELLOW}警告信息:${NC}"
            cat /tmp/test_env_output.log | sed 's/^/    /' | head -3
        fi
        WARNINGS=$((WARNINGS + 1))
        return 0
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}环境测试脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${BLUE}项目路径: $PROJECT_ROOT${NC}"
echo ""

# 1. Python 版本检查
echo -e "${BLUE}1. Python 环境检查${NC}"
echo ""

test_check "Python 3 已安装" \
    "command -v python3 > /dev/null"

if command -v python3 > /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
    PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    
    test_check "Python 版本 >= 3.8" \
        "[ $PYTHON_MAJOR -gt 3 ] || ([ $PYTHON_MAJOR -eq 3 ] && [ $PYTHON_MINOR -ge 8 ])"
    
    echo -e "    ${BLUE}当前版本: Python $PYTHON_VERSION${NC}"
fi

echo ""

# 2. 依赖包检查
echo -e "${BLUE}2. 依赖包检查${NC}"
echo ""

if [ -f "$PROJECT_ROOT/requirements.txt" ]; then
    while IFS= read -r package || [ -n "$package" ]; do
        # 跳过空行和注释
        if [[ -z "$package" ]] || [[ "$package" =~ ^# ]]; then
            continue
        fi
        
        # 提取包名（去除版本号）
        package_name=$(echo "$package" | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1 | cut -d'[' -f1 | tr -d ' ')
        
        if [ -n "$package_name" ]; then
            test_warning "依赖包: $package_name" \
                "python3 -c 'import ${package_name//-/_}' 2>/dev/null"
        fi
    done < "$PROJECT_ROOT/requirements.txt"
else
    echo -e "  ${YELLOW}⚠ requirements.txt 不存在，跳过依赖包检查${NC}"
    WARNINGS=$((WARNINGS + 1))
fi

echo ""

# 3. CLI 工具检查
echo -e "${BLUE}3. CLI 工具检查${NC}"
echo ""

test_check "prompt-engine CLI 工具可用" \
    "python3 $PROJECT_ROOT/scripts/prompt-engine --help > /dev/null 2>&1"

test_warning "openskills 工具可用（可选）" \
    "command -v openskills > /dev/null"

echo ""

# 4. 基本功能测试
echo -e "${BLUE}4. 基本功能测试${NC}"
echo ""

test_check "list 命令可用" \
    "python3 $PROJECT_ROOT/scripts/prompt-engine list > /dev/null 2>&1"

test_check "validate 命令可用" \
    "python3 $PROJECT_ROOT/scripts/prompt-engine validate $PROJECT_ROOT/prompts > /dev/null 2>&1"

echo ""

# 5. 项目文件检查
echo -e "${BLUE}5. 项目文件检查${NC}"
echo ""

test_check "prompts 目录存在" \
    "[ -d $PROJECT_ROOT/prompts ]"

test_check "scripts 目录存在" \
    "[ -d $PROJECT_ROOT/scripts ]"

test_check "dist 目录存在" \
    "[ -d $PROJECT_ROOT/dist ]"

test_warning "产物文件存在（single-full）" \
    "[ -f $PROJECT_ROOT/dist/cursor/single-full/.cursorrules.all ]"

test_warning "产物文件存在（single-core）" \
    "[ -f $PROJECT_ROOT/dist/cursor/single-core/.cursorrules.core ]"

echo ""

# 6. 脚本权限检查
echo -e "${BLUE}6. 脚本权限检查${NC}"
echo ""

test_check "generate_dist.sh 有执行权限" \
    "[ -x $PROJECT_ROOT/scripts/utils/generate_dist.sh ]"

test_check "sync_to_project.sh 有执行权限" \
    "[ -x $PROJECT_ROOT/scripts/utils/sync_to_project.sh ]"

test_check "validate_prompts.sh 有执行权限" \
    "[ -x $PROJECT_ROOT/scripts/utils/validate_prompts.sh ]"

test_check "test_sync_scripts.sh 有执行权限" \
    "[ -x $PROJECT_ROOT/scripts/utils/test_sync_scripts.sh ]"

echo ""

# 输出测试报告
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}测试报告${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}通过: $PASSED${NC}"
echo -e "${RED}失败: $FAILED${NC}"
echo -e "${YELLOW}警告: $WARNINGS${NC}"
echo -e "${BLUE}总计: $TOTAL${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}✓ 所有测试通过，环境配置正确！${NC}"
        exit 0
    else
        echo -e "${GREEN}✓ 所有必需测试通过，但有 $WARNINGS 个警告（可选功能）${NC}"
        exit 0
    fi
else
    echo -e "${RED}✗ 有 $FAILED 个测试失败，请检查环境配置${NC}"
    exit 1
fi

