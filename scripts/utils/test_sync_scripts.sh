#!/bin/bash
# 同步脚本测试脚本
# 功能：测试所有同步相关脚本的功能

set -e

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
TEST_DIR="/tmp/test-prompt-engine-$(date +%s)"

# 测试结果统计
PASSED=0
FAILED=0
TOTAL=0

# 清理函数
cleanup() {
    if [ -d "$TEST_DIR" ]; then
        rm -rf "$TEST_DIR"
        echo -e "${YELLOW}清理测试目录: $TEST_DIR${NC}"
    fi
}

# 注册清理函数
trap cleanup EXIT

# 创建测试目录
mkdir -p "$TEST_DIR"
echo -e "${BLUE}创建测试目录: $TEST_DIR${NC}"
echo ""

# 测试函数
test_case() {
    local name="$1"
    local command="$2"
    local expected_exit_code="${3:-0}"
    
    TOTAL=$((TOTAL + 1))
    echo -e "${BLUE}测试 $TOTAL: $name${NC}"
    
    if eval "$command" > /tmp/test_output.log 2>&1; then
        exit_code=$?
    else
        exit_code=$?
    fi
    
    if [ "$exit_code" -eq "$expected_exit_code" ]; then
        echo -e "${GREEN}✓ 通过${NC}"
        PASSED=$((PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ 失败 (退出码: $exit_code, 期望: $expected_exit_code)${NC}"
        echo -e "${YELLOW}输出:${NC}"
        cat /tmp/test_output.log | head -10
        FAILED=$((FAILED + 1))
        return 1
    fi
}

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}开始测试同步脚本${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 测试 1: sync_to_project.sh 帮助信息
test_case "sync_to_project.sh 帮助信息" \
    "bash $PROJECT_ROOT/scripts/utils/sync_to_project.sh --help"

# 测试 2: sync_to_project.sh dry-run 模式 (single-full)
test_case "sync_to_project.sh dry-run (single-full)" \
    "bash $PROJECT_ROOT/scripts/utils/sync_to_project.sh --platform cursor --mode single-full --dry-run $TEST_DIR"

# 测试 3: sync_to_project.sh dry-run 模式 (single-core)
test_case "sync_to_project.sh dry-run (single-core)" \
    "bash $PROJECT_ROOT/scripts/utils/sync_to_project.sh --platform cursor --mode single-core --dry-run $TEST_DIR"

# 测试 4: sync_to_project.sh 实际同步 (single-core)
test_case "sync_to_project.sh 实际同步 (single-core)" \
    "bash $PROJECT_ROOT/scripts/utils/sync_to_project.sh --platform cursor --mode single-core $TEST_DIR"

# 测试 5: 验证同步文件存在
test_case "验证同步文件存在" \
    "[ -f $TEST_DIR/.cursorrules ]"

# 测试 6: 第二次同步以触发备份
test_case "第二次同步以触发备份" \
    "bash $PROJECT_ROOT/scripts/utils/sync_to_project.sh --platform cursor --mode single-core $TEST_DIR > /dev/null 2>&1"

# 测试 7: 验证备份文件存在
test_case "验证备份文件存在" \
    "ls $TEST_DIR/.cursorrules.backup.* > /dev/null 2>&1"

# 测试 8: generate_dist.sh 帮助信息
test_case "generate_dist.sh 帮助信息" \
    "bash $PROJECT_ROOT/scripts/utils/generate_dist.sh --help"

# 测试 9: validate_prompts.sh 运行
test_case "validate_prompts.sh 运行" \
    "bash $PROJECT_ROOT/scripts/utils/validate_prompts.sh > /dev/null 2>&1" \
    "0"

# 测试 10: merge_prompts.sh 运行
test_case "merge_prompts.sh 运行" \
    "bash $PROJECT_ROOT/scripts/core/merge_prompts.sh > /dev/null 2>&1"

# 测试 11: 验证合并文件存在
test_case "验证合并文件存在" \
    "[ -f $PROJECT_ROOT/merged_prompts.md ]"

# 测试 12: SyncSkill 模块导入
test_case "SyncSkill 模块导入" \
    "cd $PROJECT_ROOT && python3 -c 'from scripts.skills_sync.sync_skill import SyncSkill; print(\"OK\")' > /dev/null 2>&1"

# 测试 13: SyncSkill dry-run 模式
test_case "SyncSkill dry-run 模式" \
    "cd $PROJECT_ROOT && python3 -c 'from scripts.skills_sync.sync_skill import SyncSkill; s = SyncSkill(\"$TEST_DIR\", [], dry_run=True); s.run(); print(\"OK\")' > /dev/null 2>&1"

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}测试完成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}通过: $PASSED${NC}"
echo -e "${RED}失败: $FAILED${NC}"
echo -e "${BLUE}总计: $TOTAL${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✓ 所有测试通过${NC}"
    exit 0
else
    echo -e "${RED}✗ 有 $FAILED 个测试失败${NC}"
    exit 1
fi

