"""List skills command"""

from pathlib import Path
from ..utils import get_skills_dir


def list_skills_in_dir(directory: Path, prefix: str = ""):
    """
    递归列出目录中的所有 skills（官方规范：每个 skill 是一个目录，包含 SKILL.md）
    """
    for item in sorted(directory.iterdir()):
        if item.is_dir() and not item.name.startswith('.'):
            # 检查是否是 skill 目录（包含 SKILL.md）
            skill_file = item / "SKILL.md"
            if skill_file.exists():
                # 这是一个 skill 目录
                print(f"  - {prefix}{item.name}")
            else:
                # 可能是分类目录，继续递归
                print(f"  📂 {prefix}{item.name}/")
                list_skills_in_dir(item, prefix=f"{prefix}{item.name}/")
        elif item.is_file() and item.suffix == '.md' and item.name not in ['README.md', 'SKILL_TEMPLATE.md', 'SKILL.md']:
            # 向后兼容：旧的扁平化结构
            skill_name = item.stem
            print(f"  - {prefix}{skill_name} (旧格式)")


def list_skills(category: str = None):
    """列出所有可用的 skills"""
    skills_dir = get_skills_dir()
    
    if not skills_dir.exists():
        print(f"错误: skills 目录不存在: {skills_dir}")
        return
    
    print("=" * 60)
    print("可用的 Skills")
    print("=" * 60)
    
    if category:
        # 列出特定类别的 skills
        category_dir = skills_dir / category
        if not category_dir.exists():
            print(f"错误: 类别不存在: {category}")
            return
        list_skills_in_dir(category_dir, prefix=f"{category}/")
    else:
        # 列出所有类别
        for category_path in sorted(skills_dir.iterdir()):
            if category_path.is_dir() and not category_path.name.startswith('.'):
                print(f"\n📁 {category_path.name}/")
                list_skills_in_dir(category_path, prefix=f"{category_path.name}/")
