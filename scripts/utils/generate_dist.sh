#!/bin/bash
# 产物生成脚本
# 功能：生成所有平台的三种方式产物，自动组织到 dist/ 目录

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"

# 平台列表
PLATFORMS=("cursor" "trae" "antigravity")

# 方式列表
MODES=("single-full" "single-core" "multi-files")

# 获取平台文件扩展名（兼容旧版 bash）
get_platform_ext() {
    case "$1" in
        cursor)
            echo ".cursorrules"
            ;;
        trae)
            echo ".traerules"
            ;;
        antigravity)
            echo ".antigravityrules"
            ;;
        *)
            echo ""
            ;;
    esac
}

# 显示帮助信息
show_help() {
    cat << EOF
用法: $0 [选项]

生成所有平台的三种方式产物，自动组织到 dist/ 目录。

选项:
    --all              生成所有平台的三种方式产物
    --platform PLATFORM 生成特定平台的产物 (cursor/trae/antigravity)
    --mode MODE         生成特定方式的产物 (single-full/single-core/multi-files)
    --clean             生成前清理旧产物
    --verify            生成后验证产物
    --help              显示此帮助信息

示例:
    $0 --all                    # 生成所有平台的三种方式产物（包括技能产物）
    $0 --platform cursor        # 生成 Cursor 平台的所有方式产物
    $0 --mode single-core       # 生成所有平台的精简版产物（包括技能产物）
    $0 --platform cursor --mode single-core  # 生成 Cursor 平台的精简版产物
    $0 --skills                 # 单独生成技能产物
    $0 --all --clean            # 清理后生成所有产物
    $0 --all --verify           # 生成并验证所有产物

EOF
}

# 清理旧产物
clean_dist() {
    echo -e "${YELLOW}清理旧产物...${NC}"
    if [ -d "$DIST_DIR" ]; then
        find "$DIST_DIR" -type f -name ".*" -delete
        find "$DIST_DIR" -type f -name "*.md" -not -name "README.md" -delete
        find "$DIST_DIR" -type f -name "*.yml" -delete
        find "$DIST_DIR" -type f -name "*.mdc" -delete
        # 清理技能目录（但保留目录结构）
        if [ -d "$DIST_DIR/skills" ]; then
            find "$DIST_DIR/skills" -mindepth 1 -maxdepth 1 -type d -exec rm -rf {} +
            find "$DIST_DIR/skills" -type f -not -name "README.md" -delete
        fi
        echo -e "${GREEN}✓ 清理完成${NC}"
    fi
}

# 生成单文件完整版
generate_single_full() {
    local platform=$1
    local ext=$(get_platform_ext "$platform")
    
    # 对于 TRAE 和 Antigravity，CLI 工具会自动添加扩展名
    # 所以输出文件名应该是 .all.traerules 或 .all.antigravityrules
    if [ "$platform" = "trae" ]; then
        local output_file="$DIST_DIR/$platform/single-full/.all.traerules"
        local expected_file="$DIST_DIR/$platform/single-full/${ext}.all"
    elif [ "$platform" = "antigravity" ]; then
        local output_file="$DIST_DIR/$platform/single-full/.all.antigravityrules"
        local expected_file="$DIST_DIR/$platform/single-full/${ext}.all"
    else
        local output_file="$DIST_DIR/$platform/single-full/${ext}.all"
        local expected_file="$output_file"
    fi
    
    echo -e "${YELLOW}生成 $platform 单文件完整版...${NC}"
    mkdir -p "$(dirname "$output_file")"
    
    python3 "$PROJECT_ROOT/scripts/prompt-engine" merge \
        --all \
        --ide "$platform" \
        --output "$output_file"
    
    # 如果生成的文件名与预期不同，重命名
    if [ -f "$output_file" ] && [ "$output_file" != "$expected_file" ]; then
        mv "$output_file" "$expected_file"
        echo -e "${GREEN}✓ 已生成: $expected_file${NC}"
    elif [ -f "$expected_file" ]; then
        echo -e "${GREEN}✓ 已生成: $expected_file${NC}"
    else
        echo -e "${RED}✗ 生成失败: $expected_file${NC}"
        return 1
    fi
}

# 生成单文件精简版
generate_single_core() {
    local platform=$1
    local ext=$(get_platform_ext "$platform")
    
    # 对于 TRAE 和 Antigravity，CLI 工具会自动添加扩展名
    # 所以输出文件名应该是 .core.traerules 或 .core.antigravityrules
    if [ "$platform" = "trae" ]; then
        local output_file="$DIST_DIR/$platform/single-core/.core.traerules"
        local expected_file="$DIST_DIR/$platform/single-core/${ext}.core"
    elif [ "$platform" = "antigravity" ]; then
        local output_file="$DIST_DIR/$platform/single-core/.core.antigravityrules"
        local expected_file="$DIST_DIR/$platform/single-core/${ext}.core"
    else
        local output_file="$DIST_DIR/$platform/single-core/${ext}.core"
        local expected_file="$output_file"
    fi
    
    echo -e "${YELLOW}生成 $platform 单文件精简版...${NC}"
    mkdir -p "$(dirname "$output_file")"
    
    python3 "$PROJECT_ROOT/scripts/prompt-engine" merge \
        --core-only \
        --ide "$platform" \
        --output "$output_file"
    
    # 如果生成的文件名与预期不同，重命名
    if [ -f "$output_file" ] && [ "$output_file" != "$expected_file" ]; then
        mv "$output_file" "$expected_file"
        echo -e "${GREEN}✓ 已生成: $expected_file${NC}"
    elif [ -f "$expected_file" ]; then
        echo -e "${GREEN}✓ 已生成: $expected_file${NC}"
    else
        echo -e "${RED}✗ 生成失败: $expected_file${NC}"
        return 1
    fi
}

# 生成多文件目录
generate_multi_files() {
    local platform=$1
    echo -e "${YELLOW}生成 $platform 多文件目录...${NC}"
    
    case "$platform" in
        cursor)
            generate_cursor_multi_files
            ;;
        trae)
            generate_trae_multi_files
            ;;
        antigravity)
            generate_antigravity_multi_files
            ;;
        *)
            echo -e "${RED}错误: 未知的平台: $platform${NC}"
            return 1
            ;;
    esac
}

# 生成 Cursor 多文件目录
generate_cursor_multi_files() {
    local output_dir="$DIST_DIR/cursor/multi-files/rules"
    mkdir -p "$output_dir"
    
    echo -e "${YELLOW}组织 Cursor 多文件规则...${NC}"
    
    # 定义模块组织和文件编号
    local file_num=1
    local modules=(
        "common:prompts/stages/common"
        "requirements:prompts/stages/requirements"
        "design:prompts/stages/design"
        "development:prompts/stages/development"
        "testing:prompts/stages/testing"
        "documentation:prompts/stages/documentation"
    )
    
    for module_info in "${modules[@]}"; do
        IFS=':' read -r module_name module_path <<< "$module_info"
        local module_dir="$PROJECT_ROOT/$module_path"
        
        if [ ! -d "$module_dir" ]; then
            continue
        fi
        
        # 查找该模块下的所有 .md 文件（排除 README.md 和 index.md）
        local found_files=false
        while IFS= read -r -d '' md_file; do
            local filename=$(basename "$md_file")
            if [[ "$filename" == "README.md" ]] || [[ "$filename" == "index.md" ]]; then
                continue
            fi
            
            # 生成更清晰的文件名：基于相对路径
            local relative_path="${md_file#$PROJECT_ROOT/$module_path/}"
            local clean_name="${relative_path//\//-}"  # 将路径分隔符替换为连字符
            clean_name="${clean_name%.md}"  # 移除 .md 扩展名
            
            # 如果文件名过长，使用简化版本
            if [ ${#clean_name} -gt 50 ]; then
                clean_name="${clean_name:0:50}"
            fi
            
            # 生成编号文件名
            local num_str=$(printf "%03d" $file_num)
            local output_file="$output_dir/${num_str}-${clean_name}.mdc"
            
            # 复制文件内容，并根据平台替换引用
            {
                echo "# 来源: ${md_file#$PROJECT_ROOT/}"
                echo ""
                cat "$md_file"
            } > "$output_file"
            
            found_files=true
            ((file_num++))
        done < <(find "$module_dir" -type f -name "*.md" -not -name "README.md" -not -name "index.md" -print0 | sort -z)
        
        if [ "$found_files" = false ]; then
            # 如果模块下没有文件，创建一个占位文件
            local num_str=$(printf "%03d" $file_num)
            local output_file="$output_dir/${num_str}-${module_name}.mdc"
            echo "# ${module_name} 模块规则" > "$output_file"
            echo "" >> "$output_file"
            echo "> **说明**：本模块暂无规则文件" >> "$output_file"
            ((file_num++))
        fi
    done
    
    echo -e "${GREEN}✓ 已生成 Cursor 多文件目录: $output_dir${NC}"
    echo -e "${BLUE}  文件数量: $((file_num - 1))${NC}"
}

# 生成 TRAE 多文件目录（YAML 格式）
generate_trae_multi_files() {
    local output_dir="$DIST_DIR/trae/multi-files/.trae"
    mkdir -p "$output_dir"
    
    echo -e "${YELLOW}生成 TRAE YAML 规则文件...${NC}"
    
    # 生成 ai-rules.yml
    local yaml_file="$output_dir/ai-rules.yml"
    
    {
        echo "# TRAE AI 规则文件"
        echo "# 本文件由多个提示词文件合并生成"
        echo "# 适用于 TRAE IDE"
        echo ""
        echo "rules:"
        echo "  - name: \"通用规则\""
        echo "    description: \"适用于所有文件的通用规则\""
        echo "    content: |"
        
        # 收集所有提示词文件内容
        local stages=("common" "requirements" "design" "development" "testing" "documentation")
        for stage in "${stages[@]}"; do
            local stage_dir="$PROJECT_ROOT/prompts/stages/$stage"
            if [ ! -d "$stage_dir" ]; then
                continue
            fi
            
            while IFS= read -r -d '' md_file; do
                local filename=$(basename "$md_file")
                if [[ "$filename" == "README.md" ]] || [[ "$filename" == "index.md" ]]; then
                    continue
                fi
                
                # 将 Markdown 内容转换为 YAML 字符串（添加缩进）
                echo "      # 来源: ${md_file#$PROJECT_ROOT/}"
                sed 's/^/      /' "$md_file"
                echo ""
            done < <(find "$stage_dir" -type f -name "*.md" -not -name "README.md" -not -name "index.md" -print0 | sort -z)
        done
    } > "$yaml_file"
    
    echo -e "${GREEN}✓ 已生成 TRAE YAML 规则文件: $yaml_file${NC}"
}

# 生成 Antigravity 多文件目录（Agent 配置文件）
generate_antigravity_multi_files() {
    local output_dir="$DIST_DIR/antigravity/multi-files"
    mkdir -p "$output_dir"
    
    echo -e "${YELLOW}生成 Antigravity Agent 配置文件...${NC}"
    
    # 生成一个基本的 Agent 配置文件
    local agent_file="$output_dir/prompt-engine-agent.agent"
    
    {
        echo "name: \"Prompt Engine Rules Agent\""
        echo "description: \"AI 代理配置，用于加载和管理提示词规则\""
        echo "model: \"default\""
        echo ""
        echo "tasks:"
        echo "  - description: \"应用代码规范规则\""
        echo "    input: \"代码文件\""
        echo "    output: \"符合规范的代码\""
        echo ""
        echo "  - description: \"应用文档规范规则\""
        echo "    input: \"文档内容\""
        echo "    output: \"符合规范的文档\""
        echo ""
        echo "# 注意：Antigravity 的 .agent 文件用于配置 AI 代理，不是规则文件"
        echo "# 规则文件应使用 .antigravityrules 单文件方式"
    } > "$agent_file"
    
    echo -e "${GREEN}✓ 已生成 Antigravity Agent 配置文件: $agent_file${NC}"
    echo -e "${YELLOW}⚠️  注意：Antigravity 的 .agent 文件用于配置 AI 代理，不是规则文件${NC}"
    echo -e "${YELLOW}   规则文件应使用 .antigravityrules 单文件方式${NC}"
}

# 生成技能产物
generate_skills() {
    local output_dir="$DIST_DIR/skills"
    local source_dir="$PROJECT_ROOT/.claude/skills"
    
    echo -e "${YELLOW}生成技能产物...${NC}"
    mkdir -p "$output_dir"
    
    if [ ! -d "$source_dir" ]; then
        echo -e "${YELLOW}⚠️  技能目录不存在: $source_dir${NC}"
        return 0
    fi
    
    local skill_count=0
    local skipped_count=0
    
    # 复制所有技能目录（排除 README.md）
    while IFS= read -r -d '' skill_dir; do
        local skill_name=$(basename "$skill_dir")
        if [ "$skill_name" = "README.md" ]; then
            continue
        fi
        
        # 检查 SKILL.md 文件是否存在
        if [ ! -f "$skill_dir/SKILL.md" ]; then
            echo -e "${YELLOW}⚠️  跳过 $skill_name (SKILL.md 不存在)${NC}"
            ((skipped_count++))
            continue
        fi
        
        # 复制技能目录
        local target_dir="$output_dir/$skill_name"
        if [ -d "$target_dir" ]; then
            rm -rf "$target_dir"
        fi
        
        if cp -r "$skill_dir" "$target_dir" 2>/dev/null; then
            echo -e "${GREEN}✓ 已复制技能: $skill_name${NC}"
            ((skill_count++))
        else
            echo -e "${RED}✗ 复制失败: $skill_name${NC}"
            ((skipped_count++))
        fi
    done < <(find "$source_dir" -mindepth 1 -maxdepth 1 -type d -print0 | sort -z)
    
    # 复制 README.md（如果存在）
    if [ -f "$source_dir/README.md" ]; then
        cp "$source_dir/README.md" "$output_dir/" 2>/dev/null
        echo -e "${GREEN}✓ 已复制 README.md${NC}"
    fi
    
    echo -e "${GREEN}✓ 已生成技能产物目录: $output_dir${NC}"
    echo -e "${BLUE}  技能数量: $skill_count${NC}"
    if [ $skipped_count -gt 0 ]; then
        echo -e "${YELLOW}  跳过数量: $skipped_count${NC}"
    fi
}

# 验证产物
verify_dist() {
    echo -e "${YELLOW}验证产物...${NC}"
    local errors=0
    
    for platform in "${PLATFORMS[@]}"; do
        local ext=$(get_platform_ext "$platform")
        
        # 检查单文件完整版
        local full_file="$DIST_DIR/$platform/single-full/${ext}.all"
        if [ ! -f "$full_file" ]; then
            echo -e "${RED}✗ 缺失: $full_file${NC}"
            ((errors++))
        fi
        
        # 检查单文件精简版
        local core_file="$DIST_DIR/$platform/single-core/${ext}.core"
        if [ ! -f "$core_file" ]; then
            echo -e "${RED}✗ 缺失: $core_file${NC}"
            ((errors++))
        fi
    done
    
    # 检查技能目录（可选，不强制）
    if [ -d "$DIST_DIR/skills" ]; then
        local skill_dirs=$(find "$DIST_DIR/skills" -mindepth 1 -maxdepth 1 -type d | wc -l)
        if [ "$skill_dirs" -gt 0 ]; then
            echo -e "${GREEN}✓ 技能产物: $skill_dirs 个技能${NC}"
        fi
    fi
    
    if [ $errors -eq 0 ]; then
        echo -e "${GREEN}✓ 所有产物验证通过${NC}"
        return 0
    else
        echo -e "${RED}✗ 发现 $errors 个错误${NC}"
        return 1
    fi
}

# 生成特定平台的产物
generate_platform() {
    local platform=$1
    local mode=$2
    
    if [ -z "$mode" ]; then
        # 生成所有方式
        generate_single_full "$platform"
        generate_single_core "$platform"
        generate_multi_files "$platform"
    else
        # 生成特定方式
        case "$mode" in
            single-full)
                generate_single_full "$platform"
                ;;
            single-core)
                generate_single_core "$platform"
                ;;
            multi-files)
                generate_multi_files "$platform"
                ;;
            *)
                echo -e "${RED}错误: 未知的方式: $mode${NC}"
                echo "可用方式: single-full, single-core, multi-files"
                exit 1
                ;;
        esac
    fi
}

# 主函数
main() {
    local generate_all=false
    local platform=""
    local mode=""
    local clean=false
    local verify=false
    local skills_only=false
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --all)
                generate_all=true
                shift
                ;;
            --platform)
                platform="$2"
                shift 2
                ;;
            --mode)
                mode="$2"
                shift 2
                ;;
            --skills)
                skills_only=true
                shift
                ;;
            --clean)
                clean=true
                shift
                ;;
            --verify)
                verify=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            *)
                echo -e "${RED}错误: 未知参数: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 如果没有指定任何参数，显示帮助
    if [ "$generate_all" = false ] && [ -z "$platform" ] && [ -z "$mode" ] && [ "$clean" = false ] && [ "$verify" = false ] && [ "$skills_only" = false ]; then
        show_help
        exit 0
    fi
    
    # 清理旧产物
    if [ "$clean" = true ]; then
        clean_dist
    fi
    
    # 如果只生成技能产物
    if [ "$skills_only" = true ]; then
        generate_skills
        if [ "$verify" = true ]; then
            verify_dist
        fi
        echo -e "${GREEN}✓ 完成${NC}"
        return 0
    fi
    
    # 生成产物
    if [ "$generate_all" = true ]; then
        # 生成所有平台的三种方式产物
        echo -e "${GREEN}开始生成所有平台的三种方式产物...${NC}"
        for p in "${PLATFORMS[@]}"; do
            generate_platform "$p" ""
        done
        # 生成技能产物
        generate_skills
    elif [ -n "$platform" ]; then
        # 生成特定平台的产物
        if [[ ! " ${PLATFORMS[@]} " =~ " ${platform} " ]]; then
            echo -e "${RED}错误: 未知的平台: $platform${NC}"
            echo "可用平台: ${PLATFORMS[*]}"
            exit 1
        fi
        generate_platform "$platform" "$mode"
        # 如果生成所有方式，也生成技能产物
        if [ -z "$mode" ]; then
            generate_skills
        fi
    elif [ -n "$mode" ]; then
        # 生成所有平台的特定方式产物
        for p in "${PLATFORMS[@]}"; do
            generate_platform "$p" "$mode"
        done
        # 如果生成精简版，也生成技能产物（方式2需要技能）
        if [ "$mode" = "single-core" ]; then
            generate_skills
        fi
    fi
    
    # 验证产物
    if [ "$verify" = true ]; then
        verify_dist
    fi
    
    echo -e "${GREEN}✓ 完成${NC}"
}

# 运行主函数
main "$@"

