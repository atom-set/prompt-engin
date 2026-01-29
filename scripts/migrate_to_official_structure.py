#!/usr/bin/env python3
"""
迁移脚本：将扁平化的 skill 文件结构转换为官方规范结构

官方规范：
- 每个 skill 是一个目录
- 目录内包含 SKILL.md 文件（固定文件名）
- 支持可选目录：scripts/, references/, assets/
"""

import shutil
from pathlib import Path
from typing import List, Tuple


def get_skills_dir() -> Path:
    """获取 skills 目录路径"""
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    return project_root / "skills"


def find_all_skill_files() -> List[Tuple[Path, str]]:
    """
    查找所有需要迁移的 skill 文件
    
    Returns:
        [(文件路径, skill名称), ...] 列表
    """
    skills_dir = get_skills_dir()
    skill_files = []
    
    # 排除的文件
    exclude_names = {'README.md', 'SKILL_TEMPLATE.md'}
    
    # 遍历所有分类目录
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue
        
        # 查找该分类下的所有 .md 文件
        for md_file in category_dir.glob("*.md"):
            if md_file.name in exclude_names:
                continue
            
            # skill 名称 = 分类/文件名（不含扩展名）
            skill_name = f"{category_dir.name}/{md_file.stem}"
            skill_files.append((md_file, skill_name))
    
    return skill_files


def migrate_skill_file(md_file: Path, skill_name: str, dry_run: bool = False) -> bool:
    """
    迁移单个 skill 文件
    
    Args:
        md_file: 源文件路径
        skill_name: skill 名称（如 "core/act-mode"）
        dry_run: 是否为试运行模式
    
    Returns:
        是否成功
    """
    skills_dir = get_skills_dir()
    
    # 目标目录：skills/core/act-mode/
    skill_dir = skills_dir / skill_name
    # 目标文件：skills/core/act-mode/SKILL.md
    target_file = skill_dir / "SKILL.md"
    
    if target_file.exists():
        print(f"⚠️  跳过（已存在）: {skill_name}")
        return False
    
    if dry_run:
        print(f"📋 [试运行] 将迁移: {md_file.name} -> {skill_name}/SKILL.md")
        return True
    
    try:
        # 创建目标目录
        skill_dir.mkdir(parents=True, exist_ok=True)
        
        # 复制文件内容到 SKILL.md
        shutil.copy2(md_file, target_file)
        
        # 删除原文件
        md_file.unlink()
        
        print(f"✅ 已迁移: {skill_name}")
        return True
    except Exception as e:
        print(f"❌ 迁移失败 {skill_name}: {e}")
        return False


def main():
    """主函数"""
    import sys
    
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    if dry_run:
        print("=" * 60)
        print("试运行模式：不会实际修改文件")
        print("=" * 60)
        print()
    
    skills_dir = get_skills_dir()
    if not skills_dir.exists():
        print(f"❌ Skills 目录不存在: {skills_dir}")
        return
    
    # 查找所有需要迁移的文件
    skill_files = find_all_skill_files()
    
    if not skill_files:
        print("✅ 没有找到需要迁移的 skill 文件")
        return
    
    print(f"📊 找到 {len(skill_files)} 个 skill 文件需要迁移")
    print()
    
    # 执行迁移
    success_count = 0
    for md_file, skill_name in skill_files:
        if migrate_skill_file(md_file, skill_name, dry_run):
            success_count += 1
    
    print()
    print("=" * 60)
    if dry_run:
        print(f"📋 试运行完成：将迁移 {success_count} 个 skill 文件")
        print("   使用不带 --dry-run 参数运行以实际执行迁移")
    else:
        print(f"✅ 迁移完成：成功迁移 {success_count}/{len(skill_files)} 个 skill 文件")
    print("=" * 60)


if __name__ == "__main__":
    main()
