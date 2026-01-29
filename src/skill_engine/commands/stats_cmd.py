"""Stats command"""

from collections import defaultdict
from ..utils import list_all_skills, read_skill_content, extract_metadata


def show_stats():
    """显示 skills 统计信息"""
    all_skills = list_all_skills()
    
    if not all_skills:
        print("未找到任何 skills")
        return
    
    print("=" * 60)
    print("Skills 统计信息")
    print("=" * 60)
    print()
    
    # 统计信息
    total_skills = len(all_skills)
    categories = defaultdict(int)
    tags_count = defaultdict(int)
    total_lines = 0
    
    for skill_name, skill_path in all_skills:
        # 统计分类
        if '/' in skill_name:
            category = skill_name.split('/')[0]
            categories[category] += 1
        
        # 统计标签和行数
        content = read_skill_content(skill_path)
        metadata = extract_metadata(content)
        
        if metadata:
            tags = metadata.get('tags', [])
            for tag in tags:
                tags_count[tag] += 1
        
        # 统计行数
        lines = len(content.split('\n'))
        total_lines += lines
    
    # 显示统计
    print(f"总计: {total_skills} 个 skills")
    print(f"总行数: {total_lines:,} 行")
    print(f"平均行数: {total_lines // total_skills if total_skills > 0 else 0} 行/skill")
    print()
    
    # 按分类统计
    print("按分类统计:")
    for category, count in sorted(categories.items()):
        print(f"  - {category}: {count} 个")
    print()
    
    # 按标签统计
    print("按标签统计:")
    for tag, count in sorted(tags_count.items(), key=lambda x: x[1], reverse=True):
        print(f"  - {tag}: {count} 个")
