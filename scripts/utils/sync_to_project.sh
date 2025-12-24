#!/bin/bash
# 同步到项目脚本
# 功能：从 dist/ 目录同步产物到具体项目

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
DIST_DIR="$PROJECT_ROOT/dist"

# 平台列表
PLATFORMS=("cursor" "trae" "antigravity")

# 方式列表
MODES=("single-full" "single-core" "multi-files")

# 获取平台文件扩展名
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
用法: $0 [选项] <项目路径>

从 dist/ 目录同步产物到具体项目。

选项:
    --platform PLATFORM  指定平台 (cursor/trae/antigravity)
    --mode MODE          指定方式 (single-full/single-core/multi-files)
    --dry-run            预览模式，不实际同步
    --help               显示此帮助信息

如果未指定平台和方式，将进入交互式选择模式。

示例:
    $0 /path/to/your-project                    # 交互式选择
    $0 --platform cursor --mode single-core /path/to/your-project
    $0 --platform cursor --mode single-core --dry-run /path/to/your-project

EOF
}

# 交互式选择平台
interactive_select_platform() {
    echo -e "${BLUE}请选择平台:${NC}"
    for i in "${!PLATFORMS[@]}"; do
        echo "  $((i+1)). ${PLATFORMS[$i]}"
    done
    read -p "请输入选项 (1-${#PLATFORMS[@]}): " choice
    
    if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#PLATFORMS[@]}" ]; then
        echo "${PLATFORMS[$((choice-1))]}"
    else
        echo -e "${RED}错误: 无效的选项${NC}"
        exit 1
    fi
}

# 交互式选择方式
interactive_select_mode() {
    echo -e "${BLUE}请选择方式:${NC}"
    echo "  1. single-full (单文件完整版)"
    echo "  2. single-core (单文件精简版)"
    echo "  3. multi-files (多文件目录)"
    read -p "请输入选项 (1-3): " choice
    
    case "$choice" in
        1)
            echo "single-full"
            ;;
        2)
            echo "single-core"
            ;;
        3)
            echo "multi-files"
            ;;
        *)
            echo -e "${RED}错误: 无效的选项${NC}"
            exit 1
            ;;
    esac
}

# 备份现有文件
backup_file() {
    local file=$1
    if [ -f "$file" ] || [ -d "$file" ]; then
        local backup="${file}.backup.$(date +%Y%m%d_%H%M%S)"
        echo -e "${YELLOW}备份现有文件: $file -> $backup${NC}"
        cp -r "$file" "$backup"
        echo -e "${GREEN}✓ 备份完成${NC}"
    fi
}

# 同步单文件完整版
sync_single_full() {
    local platform=$1
    local target_dir=$2
    local dry_run=$3
    
    local ext=$(get_platform_ext "$platform")
    local source_file="$DIST_DIR/$platform/single-full/${ext}.all"
    local target_file="$target_dir/${ext}"
    
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}错误: 源文件不存在: $source_file${NC}"
        echo "请先运行: bash scripts/utils/generate_dist.sh --platform $platform --mode single-full"
        return 1
    fi
    
    if [ "$dry_run" = true ]; then
        echo -e "${BLUE}[预览] 将同步:${NC}"
        echo "  源文件: $source_file"
        echo "  目标文件: $target_file"
        return 0
    fi
    
    echo -e "${YELLOW}同步单文件完整版...${NC}"
    backup_file "$target_file"
    cp "$source_file" "$target_file"
    echo -e "${GREEN}✓ 已同步到: $target_file${NC}"
}

# 同步单文件精简版
sync_single_core() {
    local platform=$1
    local target_dir=$2
    local dry_run=$3
    
    local ext=$(get_platform_ext "$platform")
    local source_file="$DIST_DIR/$platform/single-core/${ext}.core"
    local target_file="$target_dir/${ext}"
    
    if [ ! -f "$source_file" ]; then
        echo -e "${RED}错误: 源文件不存在: $source_file${NC}"
        echo "请先运行: bash scripts/utils/generate_dist.sh --platform $platform --mode single-core"
        return 1
    fi
    
    if [ "$dry_run" = true ]; then
        echo -e "${BLUE}[预览] 将同步:${NC}"
        echo "  源文件: $source_file"
        echo "  目标文件: $target_file"
        return 0
    fi
    
    echo -e "${YELLOW}同步单文件精简版...${NC}"
    backup_file "$target_file"
    cp "$source_file" "$target_file"
    echo -e "${GREEN}✓ 已同步到: $target_file${NC}"
}

# 同步多文件目录
sync_multi_files() {
    local platform=$1
    local target_dir=$2
    local dry_run=$3
    
    local source_dir=""
    local target_path=""
    
    case "$platform" in
        cursor)
            source_dir="$DIST_DIR/cursor/multi-files/rules"
            target_path="$target_dir/.cursor/rules"
            ;;
        trae)
            source_dir="$DIST_DIR/trae/multi-files/.trae"
            target_path="$target_dir/.trae"
            ;;
        antigravity)
            source_dir="$DIST_DIR/antigravity/multi-files"
            target_path="$target_dir"
            ;;
        *)
            echo -e "${RED}错误: 未知的平台: $platform${NC}"
            return 1
            ;;
    esac
    
    if [ ! -d "$source_dir" ] || [ -z "$(ls -A "$source_dir" 2>/dev/null)" ]; then
        echo -e "${RED}错误: 源目录不存在或为空: $source_dir${NC}"
        echo "请先运行: bash scripts/utils/generate_dist.sh --platform $platform --mode multi-files"
        return 1
    fi
    
    if [ "$dry_run" = true ]; then
        echo -e "${BLUE}[预览] 将同步:${NC}"
        echo "  源目录: $source_dir"
        echo "  目标目录: $target_path"
        return 0
    fi
    
    echo -e "${YELLOW}同步多文件目录...${NC}"
    backup_file "$target_path"
    mkdir -p "$(dirname "$target_path")"
    cp -r "$source_dir" "$target_path"
    echo -e "${GREEN}✓ 已同步到: $target_path${NC}"
}

# 主函数
main() {
    local platform=""
    local mode=""
    local dry_run=false
    local target_dir=""
    
    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --platform)
                platform="$2"
                shift 2
                ;;
            --mode)
                mode="$2"
                shift 2
                ;;
            --dry-run)
                dry_run=true
                shift
                ;;
            --help)
                show_help
                exit 0
                ;;
            -*)
                echo -e "${RED}错误: 未知参数: $1${NC}"
                show_help
                exit 1
                ;;
            *)
                target_dir="$1"
                shift
                ;;
        esac
    done
    
    # 检查目标目录
    if [ -z "$target_dir" ]; then
        echo -e "${RED}错误: 请指定项目路径${NC}"
        show_help
        exit 1
    fi
    
    if [ ! -d "$target_dir" ]; then
        echo -e "${RED}错误: 目标目录不存在: $target_dir${NC}"
        exit 1
    fi
    
    # 交互式选择（如果未指定）
    if [ -z "$platform" ]; then
        platform=$(interactive_select_platform)
    else
        if [[ ! " ${PLATFORMS[@]} " =~ " ${platform} " ]]; then
            echo -e "${RED}错误: 未知的平台: $platform${NC}"
            echo "可用平台: ${PLATFORMS[*]}"
            exit 1
        fi
    fi
    
    if [ -z "$mode" ]; then
        mode=$(interactive_select_mode)
    else
        if [[ ! " ${MODES[@]} " =~ " ${mode} " ]]; then
            echo -e "${RED}错误: 未知的方式: $mode${NC}"
            echo "可用方式: ${MODES[*]}"
            exit 1
        fi
    fi
    
    # 执行同步
    echo -e "${GREEN}同步配置:${NC}"
    echo "  平台: $platform"
    echo "  方式: $mode"
    echo "  目标: $target_dir"
    echo ""
    
    case "$mode" in
        single-full)
            sync_single_full "$platform" "$target_dir" "$dry_run"
            ;;
        single-core)
            sync_single_core "$platform" "$target_dir" "$dry_run"
            ;;
        multi-files)
            sync_multi_files "$platform" "$target_dir" "$dry_run"
            ;;
    esac
    
    if [ "$dry_run" = false ]; then
        echo -e "${GREEN}✓ 同步完成${NC}"
    fi
}

# 运行主函数
main "$@"

