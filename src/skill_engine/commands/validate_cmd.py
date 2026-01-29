"""Validate skill command"""

from ..utils import find_skill_file, read_skill_content, parse_frontmatter, validate_frontmatter


def validate_skill(skill_path: str):
    """验证 skill 格式"""
    skill_file = find_skill_file(skill_path)
    
    if not skill_file:
        print(f"❌ 错误: Skill 不存在: {skill_path}")
        return False
    
    print("=" * 60)
    print(f"验证 Skill: {skill_path}")
    print("=" * 60)
    print()
    
    content = read_skill_content(skill_file)
    
    # 检查 frontmatter
    metadata, _ = parse_frontmatter(content)
    
    if not metadata:
        print("❌ 错误: 缺少 YAML frontmatter")
        print()
        print("Skill 文件必须以 YAML frontmatter 开头:")
        print("---")
        print("name: skill-name")
        print("description: 描述")
        print("tags: [tag1, tag2]")
        print("---")
        return False
    
    # 验证 frontmatter
    is_valid, errors = validate_frontmatter(metadata)
    
    if not is_valid:
        print("❌ Frontmatter 验证失败:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    # 检查必需章节
    required_sections = [
        "## 使用场景",
        "## 触发条件",
        "## 与其他规则的配合"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in content:
            missing_sections.append(section)
    
    if missing_sections:
        print("⚠️  警告: 缺少推荐的章节:")
        for section in missing_sections:
            print(f"  - {section}")
        print()
    
    # 验证通过
    print("✅ Skill 格式验证通过")
    print()
    print("元数据:")
    print(f"  - 名称: {metadata.get('name')}")
    print(f"  - 描述: {metadata.get('description')}")
    if 'priority' in metadata:
        print(f"  - 优先级: {metadata.get('priority')}")
    print(f"  - 标签: {', '.join(metadata.get('tags', []))}")
    
    return True
