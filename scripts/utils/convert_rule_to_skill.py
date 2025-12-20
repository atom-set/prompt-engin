#!/usr/bin/env python3
"""
规则转技能工具

将规则文件转换为 OpenSkills 格式的技能文件。

用法：
    python3 scripts/utils/convert_rule_to_skill.py \
        --rule-file prompts/stages/common/document/document-format.md \
        --skill-name document-format \
        --description "文档格式规范"
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Optional


def extract_title(content: str) -> str:
    """从规则文件内容中提取标题（第一个二级标题）"""
    lines = content.split('\n')
    for line in lines:
        if line.startswith('## '):
            title = line[3:].strip()
            # 移除可能的 # 后缀
            title = title.rstrip('#').strip()
            return title
    return ""


def extract_description(content: str, skill_name: str) -> str:
    """从规则文件内容中提取描述（第一个段落）"""
    lines = content.split('\n')
    description_lines = []
    in_description = False
    
    for line in lines:
        # 跳过文件头注释
        if line.startswith('>') or line.startswith('#'):
            continue
        # 跳过空行
        if not line.strip():
            if in_description:
                break
            continue
        # 收集描述段落
        if not in_description:
            in_description = True
        description_lines.append(line.strip())
        # 如果已经有足够的描述（至少10个字符），可以停止
        if len(' '.join(description_lines)) >= 50:
            break
    
    description = ' '.join(description_lines)
    if len(description) < 10:
        description = f"规则技能：{skill_name}"
    
    # 截断过长的描述
    if len(description) > 200:
        description = description[:197] + "..."
    
    return description


def create_skill_from_rule(
    rule_file: Path,
    skill_name: str,
    skill_dir: Path,
    description: Optional[str] = None,
) -> bool:
    """
    从规则文件创建技能
    
    Args:
        rule_file: 规则文件路径
        skill_name: 技能名称
        skill_dir: 技能目录路径
        description: 技能描述（可选）
    
    Returns:
        是否成功
    """
    if not rule_file.exists():
        print(f"错误：规则文件不存在: {rule_file}", file=sys.stderr)
        return False
    
    # 读取规则文件内容
    with open(rule_file, 'r', encoding='utf-8') as f:
        rule_content = f.read()
    
    # 提取标题和描述
    title = extract_title(rule_content)
    if not title:
        title = skill_name.replace('-', ' ').title()
    
    if not description:
        description = extract_description(rule_content, skill_name)
    
    # 创建技能目录
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建 SKILL.md 文件
    skill_md = skill_dir / "SKILL.md"
    
    # 生成技能内容
    skill_content = f"""---
name: {skill_name}
description: {description}
tags: [rules, prompt-engine]
---

# {title}

## 使用场景

当用户需要：
- **应用此规范**时，自动加载此技能

## 触发条件

以下情况自动应用此规范：
- 用户要求应用相关规范时
- AI 助手识别到需要使用此规范时

## 与其他规则的配合

- 与其他规则技能配合使用
- 与核心规则配合使用

---

{rule_content}
"""
    
    # 写入技能文件
    with open(skill_md, 'w', encoding='utf-8') as f:
        f.write(skill_content)
    
    print(f"✓ 已创建技能: {skill_dir}")
    print(f"  技能文件: {skill_md}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="将规则文件转换为 OpenSkills 格式的技能文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从规则文件创建技能
  python3 scripts/utils/convert_rule_to_skill.py \\
    --rule-file prompts/stages/common/document/document-format.md \\
    --skill-name document-format \\
    --description "文档格式规范"
        """
    )
    
    parser.add_argument(
        "--rule-file",
        type=str,
        required=True,
        help="规则文件路径（相对于项目根目录）"
    )
    
    parser.add_argument(
        "--skill-name",
        type=str,
        required=True,
        help="技能名称（小写字母、数字、连字符）"
    )
    
    parser.add_argument(
        "--description",
        type=str,
        default=None,
        help="技能描述（可选，如果不提供会自动提取）"
    )
    
    parser.add_argument(
        "--base-path",
        type=str,
        default=None,
        help="项目根目录路径（默认：脚本所在目录的父目录）"
    )
    
    args = parser.parse_args()
    
    # 确定项目根目录
    if args.base_path:
        project_root = Path(args.base_path)
    else:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent.parent
    
    # 验证技能名称格式
    if not re.match(r'^[a-z0-9-]+$', args.skill_name):
        print(f"错误：技能名称只能包含小写字母、数字和连字符: {args.skill_name}", file=sys.stderr)
        sys.exit(1)
    
    # 解析规则文件路径
    rule_file = project_root / args.rule_file
    if not rule_file.exists():
        print(f"错误：规则文件不存在: {rule_file}", file=sys.stderr)
        sys.exit(1)
    
    # 技能目录
    skill_dir = project_root / ".claude" / "skills" / args.skill_name
    
    # 检查技能是否已存在
    if skill_dir.exists() and (skill_dir / "SKILL.md").exists():
        response = input(f"技能 '{args.skill_name}' 已存在，是否覆盖？(y/N): ")
        if response.lower() not in ('y', 'yes'):
            print("已取消操作")
            sys.exit(0)
    
    # 创建技能
    success = create_skill_from_rule(
        rule_file,
        args.skill_name,
        skill_dir,
        args.description,
    )
    
    if success:
        print(f"\n✓ 技能创建成功: {skill_dir}")
        print(f"  查看技能: openskills read {args.skill_name}")
        print(f"  安装技能: openskills install {skill_dir}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
