#!/bin/bash
# 批量生成所有技能脚本
# 功能：从规则文件批量生成所有技能到 .claude/skills/ 目录

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# 转换工具路径
CONVERT_SCRIPT="$PROJECT_ROOT/scripts/utils/convert_rule_to_skill.py"

# 技能映射表（技能名称:规则文件路径:描述）
declare -a SKILLS=(
    # 第一批（P0-P1）
    "document-format:prompts/stages/common/document/document-format.md:文档格式规范，包括任务清单、测试用例、文章报告等格式要求"
    "time-format:prompts/stages/common/document/time-format.md:时间格式规范，强制要求所有时间字段都必须通过工具动态获取"
    "code-organization:prompts/stages/common/code/organization/code-organization.md:代码组织规范，包括文件大小限制、拆分原则等"
    "problem-location:prompts/stages/common/code/problem-location/problem-location.md:问题定位与调试规范，包括调试流程、调试代码规范等"
    "design-principles:prompts/stages/common/code/design-principles/design-principles.md:设计原则规范，强调简单设计优先，避免过度设计"
    "wiki-output:prompts/stages/documentation/wiki-output.md:WIKI 文档输出规范，包括文档结构、格式要求、Mermaid 图表转换等"
    "document-generation:prompts/stages/documentation/document-generation.md:文档生成规范，整合技术方案、架构图、WIKI 等文档类型的规范"
    # 第二批（P2）
    "project-clean-principle:prompts/stages/common/project/project-clean-principle.md:项目清洁原则，避免将 AI 辅助开发工具和非业务相关的脚本混入项目核心代码"
    "architecture-diagram-template:prompts/stages/documentation/architecture-diagram-template.md:架构图文档模板规范，包括图表模块化、说明可折叠、便于导航等"
    "open-question-confirmation:prompts/stages/common/interaction/open-question-confirmation.md:开放性问题确认规范，针对开放性问题必须通过询问方式与用户的理解达成一致"
    "modular-output:prompts/stages/common/mode/plan/modular-output.md:完整方案模块化输出策略，适用于复杂内容的输出"
    "exception-handling:prompts/stages/common/mode/plan/exception-handling.md:例外情况的处理流程，包括明显的语法错误、已知的简单问题等例外情况"
    "compatibility-check:prompts/stages/common/mode/plan/compatibility-check.md:技术方案调整的兼容性确认机制，涉及技术方案调整时必须明确询问用户是否需要向下兼容"
    "file-reading:prompts/stages/common/mode/plan/file-reading.md:大文件读取策略，对于大文件的读取应采用阶段性读取策略"
    "phase-implementation:prompts/stages/common/mode/act/phase-implementation.md:大型工程分阶段实施规则，大型工程必须分阶段实施，每个阶段完成后确认和测试再继续"
    "time-check:prompts/stages/common/mode/act/time-check.md:时间字段强制检查机制，创建包含时间字段的文档时，必须先通过工具获取当前时间"
)

# 统计变量
TOTAL=0
SUCCESS=0
FAILED=0
SKIPPED=0

# 解析参数
OVERWRITE=false
SKIP_EXISTING=false
QUIET=false

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

批量生成所有技能到 .claude/skills/ 目录。

选项:
    --overwrite          覆盖已存在的技能文件
    --skip-existing      跳过已存在的技能文件（默认行为）
    --quiet              静默模式，只显示错误和最终统计
    -h, --help           显示此帮助信息

示例:
    # 生成所有技能（跳过已存在的）
    bash scripts/utils/generate_all_skills.sh

    # 覆盖所有已存在的技能
    bash scripts/utils/generate_all_skills.sh --overwrite

    # 跳过已存在的技能（显式指定）
    bash scripts/utils/generate_all_skills.sh --skip-existing

说明:
    - 脚本会从规则文件批量生成所有 16 个技能
    - 默认行为：如果技能已存在，会跳过（不覆盖）
    - 使用 --overwrite 可以强制重新生成所有技能
    - 技能将生成到 .claude/skills/ 目录

EOF
}

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --overwrite)
            OVERWRITE=true
            shift
            ;;
        --skip-existing)
            SKIP_EXISTING=true
            shift
            ;;
        --quiet)
            QUIET=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知参数: $1${NC}" >&2
            echo "使用 --help 查看帮助信息"
            exit 1
            ;;
    esac
done

# 检查是否在项目目录中
if [ ! -f "$PROJECT_ROOT/pyproject.toml" ]; then
    echo -e "${RED}错误: 请在 prompt-engin 项目根目录下运行此脚本${NC}" >&2
    exit 1
fi

# 检查转换工具是否存在
if [ ! -f "$CONVERT_SCRIPT" ]; then
    echo -e "${RED}错误: 转换工具不存在: $CONVERT_SCRIPT${NC}" >&2
    exit 1
fi

# 检查 Python 是否可用
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 python3 命令${NC}" >&2
    exit 1
fi

# 显示开始信息
if [ "$QUIET" = false ]; then
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}批量生成 prompt-engin 技能${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}项目根目录:${NC} $PROJECT_ROOT"
    echo -e "${YELLOW}转换工具:${NC} $CONVERT_SCRIPT"
    echo -e "${YELLOW}目标目录:${NC} $PROJECT_ROOT/.claude/skills/"
    echo ""
    
    if [ "$OVERWRITE" = true ]; then
        echo -e "${YELLOW}模式:${NC} ${RED}覆盖模式${NC}（将覆盖所有已存在的技能）"
    else
        echo -e "${YELLOW}模式:${NC} ${GREEN}跳过模式${NC}（跳过已存在的技能）"
    fi
    echo ""
fi

# 创建技能目录（如果不存在）
SKILLS_DIR="$PROJECT_ROOT/.claude/skills"
mkdir -p "$SKILLS_DIR"

# 处理每个技能
TOTAL=${#SKILLS[@]}

if [ "$QUIET" = false ]; then
    echo -e "${BLUE}开始生成技能...${NC}"
    echo ""
fi

for skill_entry in "${SKILLS[@]}"; do
    # 解析技能信息（格式：技能名称:规则文件路径:描述）
    IFS=':' read -r skill_name rule_file description <<< "$skill_entry"
    
    # 检查规则文件是否存在
    rule_path="$PROJECT_ROOT/$rule_file"
    if [ ! -f "$rule_path" ]; then
        if [ "$QUIET" = false ]; then
            echo -e "${RED}✗${NC} $skill_name (规则文件不存在: $rule_file)"
        fi
        ((FAILED++))
        continue
    fi
    
    # 检查技能是否已存在
    skill_dir="$SKILLS_DIR/$skill_name"
    if [ -d "$skill_dir" ] && [ -f "$skill_dir/SKILL.md" ]; then
        if [ "$OVERWRITE" = false ]; then
            if [ "$QUIET" = false ]; then
                echo -e "${YELLOW}⏭${NC} $skill_name (已存在，跳过)"
            fi
            ((SKIPPED++))
            continue
        else
            if [ "$QUIET" = false ]; then
                echo -e "${YELLOW}🔄${NC} $skill_name (已存在，将覆盖)"
            fi
        fi
    fi
    
    # 生成技能
    if [ "$QUIET" = false ]; then
        echo -e "${BLUE}正在生成:${NC} $skill_name"
    fi
    
    # 调用转换工具
    # 如果使用覆盖模式，需要自动确认覆盖
    if [ "$OVERWRITE" = true ] && [ -f "$skill_dir/SKILL.md" ]; then
        # 覆盖模式：自动确认覆盖
        echo "y" | python3 "$CONVERT_SCRIPT" \
            --rule-file "$rule_file" \
            --skill-name "$skill_name" \
            --description "$description" \
            > /dev/null 2>&1
        convert_result=$?
    else
        # 正常模式：直接生成
        python3 "$CONVERT_SCRIPT" \
            --rule-file "$rule_file" \
            --skill-name "$skill_name" \
            --description "$description" \
            > /dev/null 2>&1
        convert_result=$?
    fi
    
    if [ $convert_result -eq 0 ]; then
        if [ "$QUIET" = false ]; then
            echo -e "${GREEN}✓${NC} $skill_name (生成成功)"
        fi
        ((SUCCESS++))
    else
        if [ "$QUIET" = false ]; then
            echo -e "${RED}✗${NC} $skill_name (生成失败)"
        else
            echo -e "${RED}错误:${NC} $skill_name 生成失败" >&2
        fi
        ((FAILED++))
    fi
    
    if [ "$QUIET" = false ]; then
        echo ""
    fi
done

# 显示统计信息
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}生成完成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}成功:${NC} $SUCCESS 个技能"
if [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}跳过:${NC} $SKIPPED 个技能"
fi
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}失败:${NC} $FAILED 个技能"
fi
echo -e "${BLUE}总计:${NC} $TOTAL 个技能"
echo ""

# 如果有失败的技能，返回非零退出码
if [ $FAILED -gt 0 ]; then
    exit 1
fi

exit 0

