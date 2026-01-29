#!/bin/bash
# 合并核心规则到 .core 文件
# 用法: ./scripts/merge-core.sh

set -e

CORE_DIR="prompts/core"
OUTPUT_FILE=".core"

# 检查目录是否存在
if [ ! -d "$CORE_DIR" ]; then
    echo "❌ 错误: 目录不存在: $CORE_DIR"
    echo "请先运行拆分脚本: python scripts/split-core.py"
    exit 1
fi

echo "🔄 开始合并核心规则..."

# 创建输出文件头部
cat > "$OUTPUT_FILE" << 'EOF'
# 合并的提示词文件
# 本文件由多个提示词文件合并生成
# 适用于 Cursor IDE
# 自动生成时间: 
EOF

echo "$(date '+%Y-%m-%d %H:%M:%S')" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# 合并模式相关规则
if [ -d "$CORE_DIR/mode" ]; then
    echo "📁 合并模式相关规则..."
    for file in "$CORE_DIR"/mode/*.md; do
        if [ -f "$file" ]; then
            relative_path="${file#$CORE_DIR/}"
            echo "  ✅ $relative_path"
            echo "" >> "$OUTPUT_FILE"
            echo "# ===========================================================================" >> "$OUTPUT_FILE"
            echo "# 来源: prompts/stages/common/$relative_path" >> "$OUTPUT_FILE"
            echo "# ===========================================================================" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            cat "$file" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    done
fi

# 合并代码规范
if [ -d "$CORE_DIR/code" ]; then
    echo "📁 合并代码规范..."
    
    # 合并 code 目录下的直接文件
    for file in "$CORE_DIR"/code/*.md; do
        if [ -f "$file" ]; then
            relative_path="${file#$CORE_DIR/}"
            echo "  ✅ $relative_path"
            echo "" >> "$OUTPUT_FILE"
            echo "# ===========================================================================" >> "$OUTPUT_FILE"
            echo "# 来源: prompts/stages/common/$relative_path" >> "$OUTPUT_FILE"
            echo "# ===========================================================================" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            cat "$file" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
        fi
    done
    
    # 合并 error-handling 子目录
    if [ -d "$CORE_DIR/code/error-handling" ]; then
        for file in "$CORE_DIR"/code/error-handling/*.md; do
            if [ -f "$file" ]; then
                relative_path="${file#$CORE_DIR/}"
                echo "  ✅ $relative_path"
                echo "" >> "$OUTPUT_FILE"
                echo "# ===========================================================================" >> "$OUTPUT_FILE"
                echo "# 来源: prompts/stages/common/$relative_path" >> "$OUTPUT_FILE"
                echo "# ===========================================================================" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
                cat "$file" >> "$OUTPUT_FILE"
                echo "" >> "$OUTPUT_FILE"
            fi
        done
    fi
fi

echo ""
echo "✅ 合并完成: $OUTPUT_FILE"
echo "📊 文件统计:"
wc -l "$OUTPUT_FILE" | awk '{print "  行数: " $1}'
du -h "$OUTPUT_FILE" | awk '{print "  大小: " $1}'
