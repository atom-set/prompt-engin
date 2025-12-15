#!/bin/bash

# 提示词合并脚本
# 功能：将 prompts/ 目录下的提示词文件按阶段和类型合并
# 使用方式：在项目根目录运行此脚本

set -e  # 遇到错误立即退出

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PROMPTS_DIR="$REPO_ROOT/prompts"
OUTPUT_FILE="$REPO_ROOT/merged_prompts.md"

# 检查提示词目录是否存在
if [ ! -d "$PROMPTS_DIR" ]; then
    echo -e "${YELLOW}错误：找不到提示词目录 $PROMPTS_DIR${NC}"
    exit 1
fi

# 阶段顺序（按研发流程顺序）
STAGES=(
    "common"
    "requirements"
    "design"
    "development"
    "testing"
    "documentation"
)

# 项目类型顺序
PROJECT_TYPES=(
    "frontend"
    "backend"
    "fullstack"
    "mobile"
)

echo -e "${BLUE}开始合并提示词文件...${NC}"

# 创建输出文件头部
cat > "$OUTPUT_FILE" << 'EOF'
# 合并的提示词文件
# 本文件由 prompts/ 目录下的提示词文件合并生成
# 提示词按研发阶段和项目类型组织
# 如需修改提示词，请编辑 prompts/ 目录下对应的文件，然后运行此脚本合并

EOF

# 合并提示词文件的函数
merge_prompt_file() {
    local prompt_path="$1"
    local prompt_source="$2"
    
    if [ ! -f "$prompt_path" ]; then
        return 1
    fi
    
    echo -e "${BLUE}合并提示词：$prompt_source${NC}"
    
    # 添加分隔线和提示词来源注释
    echo "" >> "$OUTPUT_FILE"
    echo "# ============================================================================" >> "$OUTPUT_FILE"
    echo "# 提示词来源：prompts/$prompt_source" >> "$OUTPUT_FILE"
    echo "# ============================================================================" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
    
    # 追加提示词文件内容
    cat "$prompt_path" >> "$OUTPUT_FILE"
    
    # 添加空行分隔
    echo "" >> "$OUTPUT_FILE"
    
    return 0
}

# 合并阶段提示词
echo -e "${BLUE}合并阶段提示词...${NC}"
for stage in "${STAGES[@]}"; do
    stage_dir="$PROMPTS_DIR/stages/$stage"
    
    if [ ! -d "$stage_dir" ]; then
        continue
    fi
    
    # 递归获取该阶段目录下的所有 .md 文件，排除 README.md，按字母顺序排序
    all_prompt_files=$(find "$stage_dir" -name "*.md" -type f ! -name "README.md" | sort)
    
    if [ -z "$all_prompt_files" ]; then
        continue
    fi
    
    for prompt_file in $all_prompt_files; do
        relative_path="${prompt_file#$PROMPTS_DIR/}"
        merge_prompt_file "$prompt_file" "$relative_path"
    done
done

# 合并类型提示词
echo -e "${BLUE}合并类型提示词...${NC}"
for project_type in "${PROJECT_TYPES[@]}"; do
    type_dir="$PROMPTS_DIR/types/$project_type"
    
    if [ ! -d "$type_dir" ]; then
        continue
    fi
    
    # 递归获取该类型目录下的所有 .md 文件，排除 README.md，按字母顺序排序
    all_prompt_files=$(find "$type_dir" -name "*.md" -type f ! -name "README.md" | sort)
    
    if [ -z "$all_prompt_files" ]; then
        continue
    fi
    
    for prompt_file in $all_prompt_files; do
        relative_path="${prompt_file#$PROMPTS_DIR/}"
        merge_prompt_file "$prompt_file" "$relative_path"
    done
done

echo -e "${GREEN}✓ 提示词合并完成：$OUTPUT_FILE${NC}"

