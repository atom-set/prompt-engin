#!/bin/bash

# 统计 Prompt Engine 数据指标
# 用于分享大纲中的数据统计

echo "=== Prompt Engine 数据统计 ==="
echo ""

# 检查文件是否存在
if [ ! -f ".cursorrules.all" ] || [ ! -f ".cursorrules.core" ]; then
    echo "⚠️  警告: 找不到统计文件"
    echo ""
    echo "请先生成规则文件:"
    echo "  python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.all"
    echo "  python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core"
    echo ""
    exit 1
fi

# 统计行数
full_lines=$(wc -l < .cursorrules.all)
core_lines=$(wc -l < .cursorrules.core)
reduction=$(( (full_lines - core_lines) * 10000 / full_lines ))
reduction_percent=$(echo "scale=1; $reduction / 100" | bc)

# 统计文件大小
full_size=$(du -h .cursorrules.all | cut -f1)
core_size=$(du -h .cursorrules.core | cut -f1)

echo "📊 文件行数统计:"
echo "  完整版 (.cursorrules.all): ${full_lines} 行"
echo "  精简版 (.cursorrules.core): ${core_lines} 行"
echo "  减少: $((full_lines - core_lines)) 行"
echo "  减少比例: ${reduction_percent}%"
echo ""

echo "📦 文件大小统计:"
echo "  完整版: ${full_size}"
echo "  精简版: ${core_size}"
echo ""

echo "✅ 统计完成"
echo ""
echo "💡 提示: 可以将这些数据更新到分享大纲中"

