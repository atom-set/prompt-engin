#!/bin/bash

# 批量安装所有技能脚本
# 用途：一次性安装 prompt-engin 项目中的所有技能到当前项目

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
SKILLS_DIR="$PROJECT_ROOT/.claude/skills"

# 检查是否在项目目录中
if [ ! -f "$PROJECT_ROOT/pyproject.toml" ]; then
    echo -e "${RED}错误: 请在 prompt-engin 项目根目录下运行此脚本${NC}"
    exit 1
fi

# 检查技能目录是否存在
if [ ! -d "$SKILLS_DIR" ]; then
    echo -e "${RED}错误: 技能目录不存在: $SKILLS_DIR${NC}"
    exit 1
fi

# 处理命令行参数
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "批量安装 prompt-engin 项目中的技能"
    echo ""
    echo "用法:"
    echo "  bash scripts/utils/install_all_skills.sh [目标项目目录]"
    echo ""
    echo "参数:"
    echo "  目标项目目录  (可选) 要安装技能的目标项目目录路径"
    echo "               如果未提供，使用当前工作目录"
    echo ""
    echo "功能:"
    echo "  - 支持安装所有技能（全选）"
    echo "  - 支持交互式选择要安装的技能"
    echo "  - 显示安装进度和结果统计"
    echo ""
    echo "示例:"
    echo "  # 从 prompt-engin 项目运行，指定目标项目"
    echo "  cd /path/to/prompt-engin"
    echo "  bash scripts/utils/install_all_skills.sh /path/to/your-project"
    echo ""
    echo "  # 从目标项目运行（使用相对路径）"
    echo "  cd /path/to/your-project"
    echo "  bash ../prompt-engin/scripts/utils/install_all_skills.sh"
    echo ""
    echo "  # 使用当前目录作为目标项目"
    echo "  cd /path/to/your-project"
    echo "  bash ../prompt-engin/scripts/utils/install_all_skills.sh ."
    echo ""
    echo "交互式选择:"
    echo "  运行脚本后，会提示选择安装方式："
    echo "    1. 安装所有技能（全选）"
    echo "    2. 选择要安装的技能（输入技能编号，如: 1,3,5）"
    echo "    3. 取消安装"
    echo ""
    exit 0
fi

# 获取目标项目目录（当前工作目录）
TARGET_PROJECT_DIR="${1:-$(pwd)}"

# 如果提供了参数，使用参数作为目标项目目录
if [ -n "$1" ] && [ "$1" != "." ]; then
    TARGET_PROJECT_DIR="$1"
fi

# 检查目标项目目录是否存在
if [ ! -d "$TARGET_PROJECT_DIR" ]; then
    echo -e "${RED}错误: 目标项目目录不存在: $TARGET_PROJECT_DIR${NC}"
    exit 1
fi

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}批量安装 prompt-engin 技能${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${YELLOW}技能源目录:${NC} $SKILLS_DIR"
echo -e "${YELLOW}目标项目目录:${NC} $TARGET_PROJECT_DIR"
echo ""
echo -e "${BLUE}重要提示:${NC}"
echo -e "${YELLOW}  - 本脚本使用 cp/rsync 直接复制技能目录${NC}"
echo -e "${YELLOW}  - 技能将直接复制到目标项目的 .claude/skills/ 目录${NC}"
echo -e "${YELLOW}  - 如果目标目录已存在，将被覆盖${NC}"
echo -e "${YELLOW}  - 如果安装失败，请参考: docs/milestones/V1_SKILL/V1_SKILL_SYSTEM_GUIDE.md${NC}"
echo ""

# 获取所有技能目录
SKILLS=$(ls -1 "$SKILLS_DIR" | grep -v README.md | sort)

if [ -z "$SKILLS" ]; then
    echo -e "${RED}错误: 未找到任何技能${NC}"
    exit 1
fi

# 统计技能数量
SKILL_COUNT=$(echo "$SKILLS" | wc -l | tr -d ' ')
echo -e "${GREEN}找到 $SKILL_COUNT 个技能${NC}"
echo ""

# 显示技能列表
echo -e "${BLUE}可用技能列表:${NC}"
echo "$SKILLS" | nl -w2 -s'. '
echo ""

# 询问安装方式
echo -e "${YELLOW}请选择安装方式:${NC}"
echo -e "  ${GREEN}1${NC}. 安装所有技能（全选）"
echo -e "  ${GREEN}2${NC}. 选择要安装的技能（交互式选择）"
echo -e "  ${GREEN}3${NC}. 取消安装"
echo ""
read -p "$(echo -e ${YELLOW}请输入选项 [1-3]: ${NC})" -n 1 -r INSTALL_MODE
echo ""

# 处理用户选择
SELECTED_SKILLS=""

if [[ $INSTALL_MODE == "1" ]]; then
    # 全选
    SELECTED_SKILLS="$SKILLS"
    echo -e "${GREEN}已选择：安装所有 $SKILL_COUNT 个技能${NC}"
elif [[ $INSTALL_MODE == "2" ]]; then
    # 交互式选择
    echo -e "${BLUE}请选择要安装的技能（输入技能编号，多个用逗号分隔，如: 1,3,5）:${NC}"
    echo -e "${YELLOW}提示: 输入 'all' 选择全部技能${NC}"
    echo ""
    read -p "$(echo -e ${YELLOW}请输入技能编号: ${NC})" SELECTION
    
    if [[ "$SELECTION" == "all" ]] || [[ "$SELECTION" == "ALL" ]]; then
        SELECTED_SKILLS="$SKILLS"
        echo -e "${GREEN}已选择：安装所有 $SKILL_COUNT 个技能${NC}"
    else
        # 解析用户输入的选择
        SELECTED_INDICES=$(echo "$SELECTION" | tr ',' ' ' | tr -s ' ')
        SELECTED_SKILLS=""
        
        for index in $SELECTED_INDICES; do
            # 验证索引是否有效
            if [[ "$index" =~ ^[0-9]+$ ]] && [ "$index" -ge 1 ] && [ "$index" -le "$SKILL_COUNT" ]; then
                skill=$(echo "$SKILLS" | sed -n "${index}p")
                if [ -n "$SELECTED_SKILLS" ]; then
                    SELECTED_SKILLS="$SELECTED_SKILLS"$'\n'"$skill"
                else
                    SELECTED_SKILLS="$skill"
                fi
            else
                echo -e "${YELLOW}警告: 无效的技能编号 $index，已跳过${NC}"
            fi
        done
        
        if [ -z "$SELECTED_SKILLS" ]; then
            echo -e "${RED}错误: 未选择任何技能${NC}"
            exit 1
        fi
        
        SELECTED_COUNT=$(echo "$SELECTED_SKILLS" | wc -l | tr -d ' ')
        echo -e "${GREEN}已选择：安装 $SELECTED_COUNT 个技能${NC}"
    fi
elif [[ $INSTALL_MODE == "3" ]]; then
    echo -e "${YELLOW}已取消安装${NC}"
    exit 0
else
    echo -e "${RED}错误: 无效的选项${NC}"
    exit 1
fi

echo ""

# 显示将要安装的技能
if [ -n "$SELECTED_SKILLS" ]; then
    echo -e "${BLUE}将要安装的技能:${NC}"
    echo "$SELECTED_SKILLS" | nl -w2 -s'. '
    echo ""
    
    # 最终确认
    read -p "$(echo -e ${YELLOW}确认安装到项目: $TARGET_PROJECT_DIR? [y/N]: ${NC})" -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}已取消安装${NC}"
        exit 0
    fi
else
    echo -e "${RED}错误: 未选择任何技能${NC}"
    exit 1
fi

# 进入目标项目目录
cd "$TARGET_PROJECT_DIR"

# 创建目标技能目录（如果不存在）
TARGET_SKILLS_DIR="$TARGET_PROJECT_DIR/.claude/skills"
if [ ! -d "$TARGET_SKILLS_DIR" ]; then
    echo -e "${BLUE}创建目标技能目录:${NC} $TARGET_SKILLS_DIR"
    mkdir -p "$TARGET_SKILLS_DIR"
fi

# 创建 AGENTS.md 模板文件（如果不存在）
TARGET_AGENTS_FILE="$TARGET_PROJECT_DIR/AGENTS.md"
if [ ! -f "$TARGET_AGENTS_FILE" ]; then
    echo -e "${BLUE}创建 AGENTS.md 模板文件:${NC} $TARGET_AGENTS_FILE"
    
    # 优先使用 prompt-engin 项目中的 AGENTS.md 作为模板
    SOURCE_AGENTS_FILE="$PROJECT_ROOT/AGENTS.md"
    if [ -f "$SOURCE_AGENTS_FILE" ]; then
        cp "$SOURCE_AGENTS_FILE" "$TARGET_AGENTS_FILE"
        echo -e "${GREEN}✓${NC} 已从 prompt-engin 项目复制 AGENTS.md 模板"
    else
        # 如果 prompt-engin 项目中没有，创建默认模板
        cat > "$TARGET_AGENTS_FILE" << 'EOF'

<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: Bash("openskills read <skill-name>")
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<!-- 
技能会在安装后通过 openskills sync -y 自动添加到此处
当前文件为模板，实际使用时需要先安装技能，然后运行 openskills sync -y 同步
-->

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
EOF
        echo -e "${GREEN}✓${NC} 已创建默认 AGENTS.md 模板"
    fi
    echo ""
fi

# 安装计数器
INSTALLED=0
FAILED=0
SKIPPED=0

# 逐个安装技能
echo ""
echo -e "${BLUE}开始安装技能...${NC}"
echo ""

while IFS= read -r skill; do
    # 跳过空行
    if [ -z "$skill" ]; then
        continue
    fi
    SKILL_PATH="$SKILLS_DIR/$skill"
    TARGET_SKILL_PATH="$TARGET_SKILLS_DIR/$skill"
    
    # 检查技能目录是否存在
    if [ ! -d "$SKILL_PATH" ]; then
        echo -e "${RED}✗${NC} $skill (目录不存在)"
        ((FAILED++))
        continue
    fi
    
    # 检查 SKILL.md 文件是否存在
    if [ ! -f "$SKILL_PATH/SKILL.md" ]; then
        echo -e "${YELLOW}⚠${NC} $skill (SKILL.md 不存在，跳过)"
        ((SKIPPED++))
        continue
    fi
    
    # 使用 cp 直接复制技能目录
    echo -e "${BLUE}正在安装:${NC} $skill"
    
    # 如果目标目录已存在，先删除（覆盖安装）
    if [ -d "$TARGET_SKILL_PATH" ]; then
        echo -e "${YELLOW}  目标目录已存在，将覆盖: $TARGET_SKILL_PATH${NC}"
        rm -rf "$TARGET_SKILL_PATH"
    fi
    
    # 使用 cp -r 递归复制整个技能目录
    if cp -r "$SKILL_PATH" "$TARGET_SKILL_PATH" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} $skill (安装成功)"
        ((INSTALLED++))
    else
        # 如果 cp 失败，尝试使用 rsync（如果可用）
        if command -v rsync &> /dev/null; then
            # 确保目标目录存在
            mkdir -p "$TARGET_SKILL_PATH"
            if rsync -a "$SKILL_PATH/" "$TARGET_SKILL_PATH/" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $skill (安装成功，使用 rsync)"
                ((INSTALLED++))
            else
                echo -e "${RED}✗${NC} $skill (安装失败)"
                echo -e "${YELLOW}  错误信息: 无法复制技能目录${NC}"
                echo -e "${YELLOW}  提示:${NC}"
                echo -e "${YELLOW}    - 确保有写入权限: $TARGET_SKILLS_DIR${NC}"
                echo -e "${YELLOW}    - 确保源路径正确: $SKILL_PATH${NC}"
                echo -e "${YELLOW}    - 确保技能目录包含 SKILL.md 文件${NC}"
                ((FAILED++))
            fi
        else
            echo -e "${RED}✗${NC} $skill (安装失败)"
            echo -e "${YELLOW}  错误信息: 无法复制技能目录${NC}"
            echo -e "${YELLOW}  提示:${NC}"
            echo -e "${YELLOW}    - 确保有写入权限: $TARGET_SKILLS_DIR${NC}"
            echo -e "${YELLOW}    - 确保源路径正确: $SKILL_PATH${NC}"
            echo -e "${YELLOW}    - 确保技能目录包含 SKILL.md 文件${NC}"
            ((FAILED++))
        fi
    fi
    echo ""
    
done <<< "$SELECTED_SKILLS"

# 显示安装结果
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}安装完成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "${GREEN}成功安装:${NC} $INSTALLED 个技能"
if [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}跳过:${NC} $SKIPPED 个技能"
fi
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}失败:${NC} $FAILED 个技能"
fi

# 计算未安装的技能数量
SELECTED_COUNT=$(echo "$SELECTED_SKILLS" | grep -v '^$' | wc -l | tr -d ' ')
TOTAL_SKILLS=$((INSTALLED + SKIPPED + FAILED))
if [ $TOTAL_SKILLS -lt $SELECTED_COUNT ]; then
    NOT_INSTALLED=$((SELECTED_COUNT - TOTAL_SKILLS))
    echo -e "${YELLOW}未处理:${NC} $NOT_INSTALLED 个技能"
fi
echo ""

# 询问是否立即同步技能到 AGENTS.md
if [ $INSTALLED -gt 0 ]; then
    echo ""
    echo -e "${BLUE}是否立即同步技能到 AGENTS.md？${NC}"
    echo -e "${YELLOW}提示:${NC} AGENTS.md 模板已自动创建"
    echo ""
    echo -e "${YELLOW}请选择:${NC}"
    echo -e "  ${GREEN}y${NC}. 立即同步（使用 openskills sync 交互式界面选择技能）"
    echo -e "  ${GREEN}n${NC}. 稍后手动同步（跳过）"
    echo ""
    read -p "$(echo -e ${YELLOW}请输入选项 [y/N]: ${NC})" -n 1 -r SYNC_CHOICE
    echo ""
    echo ""
    
    # 检查是否安装了 openskills
    if ! command -v openskills &> /dev/null; then
        echo -e "${YELLOW}⚠${NC} 未找到 openskills 命令，跳过同步"
        echo -e "${YELLOW}  提示:${NC} 请先安装 OpenSkills: npm install -g openskills"
        echo ""
    elif [[ $SYNC_CHOICE =~ ^[Yy]$ ]]; then
        # 使用 openskills sync 的原生交互式界面
        echo -e "${BLUE}启动技能同步...${NC}"
        echo -e "${YELLOW}提示:${NC} 使用以下快捷键操作："
        echo -e "${YELLOW}  - ↑↓${NC} 导航技能列表"
        echo -e "${YELLOW}  - 空格${NC} 选择/取消选择技能"
        echo -e "${YELLOW}  - a${NC} 全选/取消全选"
        echo -e "${YELLOW}  - i${NC} 反选"
        echo -e "${YELLOW}  - ⏎${NC} 确认并同步"
        echo ""
        if openskills sync; then
            echo ""
            echo -e "${GREEN}✓${NC} 技能同步完成"
        else
            echo ""
            echo -e "${YELLOW}⚠${NC} 同步已取消或失败"
        fi
    else
        # 跳过同步
        echo -e "${YELLOW}已跳过同步，稍后可手动运行同步命令${NC}"
    fi
    
    # 询问是否同步 .cursorrules.core 到 .cursorrules
    echo ""
    echo -e "${BLUE}是否同步规则文件？${NC}"
    SOURCE_RULES_FILE="$PROJECT_ROOT/.cursorrules.core"
    TARGET_RULES_FILE="$TARGET_PROJECT_DIR/.cursorrules"
    
    if [ -f "$SOURCE_RULES_FILE" ]; then
        echo -e "${YELLOW}提示:${NC} 可以将 prompt-engin 项目的 .cursorrules.core 同步到目标项目的 .cursorrules"
        echo ""
        echo -e "${YELLOW}请选择:${NC}"
        echo -e "  ${GREEN}y${NC}. 同步规则文件（将 .cursorrules.core 复制到 .cursorrules）"
        echo -e "  ${GREEN}n${NC}. 跳过（稍后手动同步）"
        echo ""
        read -p "$(echo -e ${YELLOW}请输入选项 [y/N]: ${NC})" -n 1 -r RULES_SYNC_CHOICE
        echo ""
        echo ""
        
        if [[ $RULES_SYNC_CHOICE =~ ^[Yy]$ ]]; then
            # 如果目标文件已存在，询问是否覆盖
            if [ -f "$TARGET_RULES_FILE" ]; then
                echo -e "${YELLOW}⚠${NC} 目标文件已存在: $TARGET_RULES_FILE"
                echo -e "${YELLOW}提示:${NC} 同步将覆盖现有文件"
                echo ""
                read -p "$(echo -e ${YELLOW}确认覆盖？ [y/N]: ${NC})" -n 1 -r OVERWRITE_CHOICE
                echo ""
                echo ""
                
                if [[ ! $OVERWRITE_CHOICE =~ ^[Yy]$ ]]; then
                    echo -e "${YELLOW}已跳过规则文件同步${NC}"
                else
                    cp "$SOURCE_RULES_FILE" "$TARGET_RULES_FILE"
                    echo -e "${GREEN}✓${NC} 已同步规则文件: $TARGET_RULES_FILE"
                fi
            else
                cp "$SOURCE_RULES_FILE" "$TARGET_RULES_FILE"
                echo -e "${GREEN}✓${NC} 已同步规则文件: $TARGET_RULES_FILE"
            fi
        else
            echo -e "${YELLOW}已跳过规则文件同步${NC}"
        fi
    else
        echo -e "${YELLOW}⚠${NC} 源规则文件不存在: $SOURCE_RULES_FILE"
        echo -e "${YELLOW}  提示:${NC} 无法同步规则文件"
    fi
    
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}其他操作:${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "${YELLOW}查看已安装的技能:${NC}"
    echo -e "   ${GREEN}ls -la $TARGET_SKILLS_DIR${NC}"
    echo ""
    echo -e "${YELLOW}查看特定技能内容:${NC}"
    echo -e "   ${GREEN}cat $TARGET_SKILLS_DIR/<skill-name>/SKILL.md${NC}"
    echo ""
    echo -e "${YELLOW}手动同步技能（如果需要）:${NC}"
    echo -e "   ${GREEN}cd $TARGET_PROJECT_DIR${NC}"
    echo -e "   ${GREEN}openskills sync${NC}        # 交互式选择"
    echo -e "   ${GREEN}openskills sync -y${NC}    # 同步所有技能"
    echo ""
    echo -e "${YELLOW}手动同步规则文件（如果需要）:${NC}"
    echo -e "   ${GREEN}cp $PROJECT_ROOT/.cursorrules.core $TARGET_PROJECT_DIR/.cursorrules${NC}"
    echo ""
fi
