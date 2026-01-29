"""Search skills command"""

from ..utils import list_all_skills, read_skill_content, extract_metadata


def search_skills(keyword: str = None, tag: str = None):
    """搜索 skills"""
    all_skills = list_all_skills()
    
    if not all_skills:
        print("未找到任何 skills")
        return
    
    print("=" * 60)
    if keyword:
        print(f"搜索关键词: {keyword}")
    elif tag:
        print(f"搜索标签: {tag}")
    print("=" * 60)
    print()
    
    results = []
    
    for skill_name, skill_path in all_skills:
        content = read_skill_content(skill_path)
        metadata = extract_metadata(content)
        
        if not metadata:
            continue
        
        # 按关键词搜索
        if keyword:
            keyword_lower = keyword.lower()
            if (keyword_lower in skill_name.lower() or
                keyword_lower in metadata.get('description', '').lower() or
                keyword_lower in content.lower()):
                results.append((skill_name, metadata))
        
        # 按标签搜索
        elif tag:
            tags = metadata.get('tags', [])
            if tag in tags:
                results.append((skill_name, metadata))
    
    if not results:
        print("未找到匹配的 skills")
        return
    
    print(f"找到 {len(results)} 个匹配的 skills:")
    print()
    
    for skill_name, metadata in results:
        print(f"📄 {skill_name}")
        print(f"   描述: {metadata.get('description', 'N/A')}")
        print(f"   标签: {', '.join(metadata.get('tags', []))}")
        print()
