"""Read skill command"""

from ..utils import find_skill_file, read_skill_content


def read_skill(skill_path: str):
    """读取并显示 skill 内容"""
    skill_file = find_skill_file(skill_path)
    
    if not skill_file:
        print(f"错误: Skill 不存在: {skill_path}")
        print(f"\n提示: 使用 'skill-engine list' 查看所有可用的 skills")
        return
    
    print("=" * 60)
    print(f"Skill: {skill_path}")
    print("=" * 60)
    print()
    
    content = read_skill_content(skill_file)
    print(content)
