"""File utility functions"""

from pathlib import Path
from typing import List, Optional, Tuple


def get_skills_dir() -> Path:
    """获取 skills 目录路径"""
    current_dir = Path(__file__).parent.parent.parent.parent
    skills_dir = current_dir / "skills"
    return skills_dir


def find_skill_file(skill_name: str) -> Optional[Path]:
    """
    查找 skill 文件（官方规范：每个 skill 是一个目录，包含 SKILL.md）
    
    Args:
        skill_name: skill 名称（可以是完整路径如 "core/act-mode" 或简单名称如 "act-mode"）
    
    Returns:
        SKILL.md 文件路径，如果未找到返回 None
    """
    skills_dir = get_skills_dir()
    
    # 官方规范：每个 skill 是一个目录，目录内包含 SKILL.md
    # 优先尝试：skills/core/act-mode/SKILL.md
    if '/' in skill_name:
        # 完整路径：core/act-mode
        skill_dir = skills_dir / skill_name
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists() and skill_file.is_file():
            return skill_file
    else:
        # 简单名称：act-mode，需要搜索所有分类目录
        for category_dir in skills_dir.iterdir():
            if not category_dir.is_dir():
                continue
            skill_dir = category_dir / skill_name
            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists() and skill_file.is_file():
                return skill_file
    
    # 向后兼容：支持旧的扁平化结构（如果存在）
    possible_paths = [
        skills_dir / f"{skill_name}.md",
        skills_dir / skill_name,
    ]
    
    for path in possible_paths:
        if path.exists() and path.is_file():
            return path
    
    # 递归搜索 SKILL.md 文件
    for skill_file in skills_dir.rglob("SKILL.md"):
        # 检查目录名是否匹配
        skill_dir_name = skill_file.parent.name
        if skill_dir_name == skill_name or skill_file.parent.relative_to(skills_dir) == Path(skill_name):
            return skill_file
    
    return None


def list_all_skills(category: Optional[str] = None) -> List[Tuple[str, Path]]:
    """
    列出所有 skills（官方规范：每个 skill 是一个目录，包含 SKILL.md）
    
    Args:
        category: 可选的分类过滤（如 "core", "code"）
    
    Returns:
        (skill_name, skill_path) 的列表，skill_name 格式为 "category/skill-name"
    """
    skills_dir = get_skills_dir()
    
    if not skills_dir.exists():
        return []
    
    skills = []
    
    # 官方规范：查找所有包含 SKILL.md 的目录
    if category:
        category_dir = skills_dir / category
        if category_dir.exists():
            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists() and skill_file.is_file():
                    skill_name = f"{category}/{skill_dir.name}"
                    skills.append((skill_name, skill_file))
    else:
        # 遍历所有分类目录
        for category_dir in skills_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue
            
            # 查找该分类下的所有 skill 目录
            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir():
                    continue
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists() and skill_file.is_file():
                    skill_name = f"{category_dir.name}/{skill_dir.name}"
                    skills.append((skill_name, skill_file))
    
    # 向后兼容：如果还有旧的扁平化结构，也包含进来
    exclude_names = {'README.md', 'SKILL_TEMPLATE.md', 'SKILL.md'}
    if category:
        category_dir = skills_dir / category
        if category_dir.exists():
            for skill_file in category_dir.glob("*.md"):
                if skill_file.name not in exclude_names:
                    skill_name = f"{category}/{skill_file.stem}"
                    # 避免重复（如果已经有目录结构版本）
                    if not any(s[0] == skill_name for s in skills):
                        skills.append((skill_name, skill_file))
    else:
        for skill_file in skills_dir.rglob("*.md"):
            if skill_file.name not in exclude_names:
                rel_path = skill_file.relative_to(skills_dir)
                skill_name = str(rel_path.with_suffix('')).replace('\\', '/')
                # 避免重复（如果已经有目录结构版本）
                if not any(s[0] == skill_name for s in skills):
                    skills.append((skill_name, skill_file))
    
    return sorted(skills, key=lambda x: x[0])


def read_skill_content(skill_path: Path) -> str:
    """
    读取 skill 文件内容
    
    Args:
        skill_path: skill 文件路径
    
    Returns:
        文件内容
    """
    with open(skill_path, 'r', encoding='utf-8') as f:
        return f.read()
