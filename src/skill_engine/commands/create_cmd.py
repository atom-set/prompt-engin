"""Create skill command"""

from pathlib import Path
from ..utils import get_skills_dir


SKILL_TEMPLATE = """---
name: {name}
description: {description}
tags: [{tags}]
---

# {title}

## 使用场景

当用户需要：
- 场景描述 1
- 场景描述 2

## 触发条件

以下情况自动应用此规范：
- 触发条件 1
- 触发条件 2

## 与其他规则的配合

- 与核心规则配合使用

---

## {title}

### 强制要求
- **核心原则**：...
- **适用范围**：...

### 详细说明

内容...

### 适用场景

**以下场景必须遵循此规范：**

- ✅ 场景 1

### 重要原则

1. **原则 1**：说明

### 注意事项

1. **注意事项 1**
"""


def create_skill(name: str, category: str = "common", interactive: bool = True):
    """
    创建新的 skill（官方规范：每个 skill 是一个目录，包含 SKILL.md）
    
    Args:
        name: skill 名称
        category: 分类（如 "core", "code"）
        interactive: 是否交互式输入
    """
    skills_dir = get_skills_dir()
    
    # 确定分类目录
    category_dir = skills_dir / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # 官方规范：每个 skill 是一个目录，目录内包含 SKILL.md
    skill_dir = category_dir / name
    skill_file = skill_dir / "SKILL.md"
    
    if skill_file.exists():
        print(f"错误: Skill 已存在: {skill_file}")
        return
    
    if skill_dir.exists():
        print(f"警告: Skill 目录已存在: {skill_dir}")
        print(f"      但 SKILL.md 文件不存在，将创建")
    
    # 交互式输入（如果启用）
    if interactive:
        print("=" * 60)
        print("创建新 Skill")
        print("=" * 60)
        print()
        
        description = input("描述（一句话说明）: ").strip()
        if not description:
            description = f"{name} 规范"
        
        tags_input = input("标签（逗号分隔，如: code, format）: ").strip()
        if not tags_input:
            tags = category
        else:
            tags = tags_input
        
        title = input(f"标题（默认: {name.replace('-', ' ').title()}）: ").strip()
        if not title:
            title = name.replace('-', ' ').title()
    else:
        description = f"{name} 规范"
        tags = category
        title = name.replace('-', ' ').title()
    
    # 生成内容
    content = SKILL_TEMPLATE.format(
        name=name,
        description=description,
        tags=tags,
        title=title
    )
    
    # 创建 skill 目录
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 写入 SKILL.md 文件
    with open(skill_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print()
    print(f"✅ Skill 创建成功: {skill_dir}/SKILL.md")
    print()
    print("下一步:")
    print(f"  1. 编辑文件: {skill_file}")
    print(f"  2. 可选：创建 scripts/, references/, assets/ 目录")
    print(f"  3. 验证格式: skill-engine validate {category}/{name}")
    print(f"  4. 查看内容: skill-engine read {category}/{name}")
