#!/bin/bash

###############################################################################
# Mermaid to PNG Converter
# 
# 将 Mermaid 流程图代码转换为 PNG 图片文件（自动使用白色背景）
# 
# 使用方法：
#   1. 从文件转换：
#      bash mermaid_to_png.sh input.mmd [output_dir] [output_name]
#   
#   2. 从标准输入转换：
#      echo "graph TD; A-->B" | bash mermaid_to_png.sh [output_dir] [output_name]
# 
# 参数说明：
#   - input.mmd: Mermaid 源文件（可选，如果不提供则从标准输入读取）
#   - output_dir: 输出目录（可选，默认为当前目录）
#   - output_name: 输出文件名（可选，如果不提供则自动生成）
###############################################################################

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查 mmdc 是否安装
if ! command -v mmdc &> /dev/null; then
    echo -e "${RED}错误: mmdc 未安装${NC}"
    echo ""
    echo "请先安装 @mermaid-js/mermaid-cli:"
    echo "  npm install -g @mermaid-js/mermaid-cli"
    echo ""
    exit 1
fi

# 临时文件
TEMP_MMD=$(mktemp /tmp/mermaid_XXXXXX.mmd)
TEMP_PNG=$(mktemp /tmp/mermaid_XXXXXX.png)

# 清理函数
cleanup() {
    rm -f "$TEMP_MMD" "$TEMP_PNG"
}
trap cleanup EXIT

# 解析参数
INPUT_FILE=""
OUTPUT_DIR=""
OUTPUT_NAME=""
READ_FROM_STDIN=false

# 检查是否有标准输入
if [ -t 0 ]; then
    # 没有标准输入，从参数读取
    if [ $# -eq 0 ]; then
        echo -e "${RED}错误: 请提供输入文件或通过标准输入提供 Mermaid 代码${NC}"
        echo ""
        echo "使用方法："
        echo "  1. 从文件转换："
        echo "     bash mermaid_to_png.sh input.mmd [output_dir] [output_name]"
        echo ""
        echo "  2. 从标准输入转换："
        echo "     echo \"graph TD; A-->B\" | bash mermaid_to_png.sh [output_dir] [output_name]"
        echo ""
        exit 1
    fi
    
    # 第一个参数可能是输入文件或输出目录
    if [ -f "$1" ]; then
        INPUT_FILE="$1"
        shift
    fi
    
    # 剩余参数
    if [ $# -ge 1 ]; then
        OUTPUT_DIR="$1"
        shift
    fi
    if [ $# -ge 1 ]; then
        OUTPUT_NAME="$1"
    fi
else
    # 有标准输入
    READ_FROM_STDIN=true
    cat > "$TEMP_MMD"
    
    # 解析参数（从标准输入时，所有参数都是输出相关）
    if [ $# -ge 1 ]; then
        OUTPUT_DIR="$1"
        shift
    fi
    if [ $# -ge 1 ]; then
        OUTPUT_NAME="$1"
    fi
fi

# 确定输入文件
if [ "$READ_FROM_STDIN" = true ]; then
    MMDFILE="$TEMP_MMD"
elif [ -n "$INPUT_FILE" ]; then
    MMDFILE="$INPUT_FILE"
else
    echo -e "${RED}错误: 未指定输入文件${NC}"
    exit 1
fi

# 检查输入文件是否存在
if [ ! -f "$MMDFILE" ]; then
    echo -e "${RED}错误: 输入文件不存在: $MMDFILE${NC}"
    exit 1
fi

# 确定输出目录（默认为当前目录）
if [ -z "$OUTPUT_DIR" ]; then
    OUTPUT_DIR="."
fi

# 创建输出目录（如果不存在）
mkdir -p "$OUTPUT_DIR"

# 确定输出文件名
if [ -z "$OUTPUT_NAME" ]; then
    # 自动生成文件名：使用时间戳
    TIMESTAMP=$(date +%Y%m%d_%H%M%S_%N | cut -b1-20)
    OUTPUT_NAME="mermaid_${TIMESTAMP}.png"
fi

# 确保输出文件名以 .png 结尾
if [[ ! "$OUTPUT_NAME" =~ \.png$ ]]; then
    OUTPUT_NAME="${OUTPUT_NAME}.png"
fi

OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_NAME"

# 转换 Mermaid 为 PNG（使用白色背景）
echo -e "${YELLOW}正在转换 Mermaid 图表...${NC}"
echo "  输入: $MMDFILE"
echo "  输出: $OUTPUT_PATH"

# 使用 mmdc 转换，设置白色背景
mmdc \
    -i "$MMDFILE" \
    -o "$TEMP_PNG" \
    -b white \
    -w 1920 \
    -H 1080 \
    -s 2 \
    -t neutral \
    -f png

# 移动临时文件到目标位置
mv "$TEMP_PNG" "$OUTPUT_PATH"

echo -e "${GREEN}✓ 转换成功: $OUTPUT_PATH${NC}"
