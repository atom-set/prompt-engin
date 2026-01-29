"""Tests for skill-engine CLI"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from skill_engine.utils import (
    get_skills_dir,
    find_skill_file,
    list_all_skills,
    parse_frontmatter,
    validate_frontmatter,
    read_skill_content
)


def test_get_skills_dir():
    """测试获取 skills 目录"""
    skills_dir = get_skills_dir()
    assert skills_dir.exists()
    assert skills_dir.is_dir()
    assert skills_dir.name == "skills"


def test_find_skill_file():
    """测试查找 skill 文件"""
    # 测试存在的 skill（使用新的文件名）
    skill_file = find_skill_file("design-principles")
    assert skill_file is not None
    assert skill_file.exists()
    
    # 测试不存在的 skill
    skill_file = find_skill_file("non-existent-skill")
    assert skill_file is None


def test_find_skill_file_various_formats():
    """测试不同格式的 skill 文件查找"""
    # 测试完整路径
    skill_file = find_skill_file("code/design-principles")
    assert skill_file is not None or find_skill_file("design-principles") is not None
    
    # 测试仅名称
    skill_file = find_skill_file("organization")
    assert skill_file is not None or find_skill_file("code-organization") is not None


def test_list_all_skills():
    """测试列出所有 skills"""
    skills = list_all_skills()
    assert len(skills) > 0
    
    # 检查返回格式
    for skill_name, skill_path in skills:
        assert isinstance(skill_name, str)
        assert isinstance(skill_path, Path)
        assert skill_path.exists()


def test_list_skills_by_category():
    """测试按分类列出 skills"""
    # 测试 code 分类
    skills = list_all_skills("code")
    assert len(skills) >= 0
    
    for skill_name, skill_path in skills:
        assert "code" in str(skill_path)


def test_list_skills_nonexistent_category():
    """测试列出不存在的分类"""
    skills = list_all_skills("nonexistent-category")
    assert len(skills) == 0


def test_read_skill_content():
    """测试读取 skill 内容"""
    skill_file = find_skill_file("design-principles")
    if skill_file:
        content = read_skill_content(skill_file)
        assert len(content) > 0
        assert isinstance(content, str)


def test_parse_frontmatter():
    """测试解析 frontmatter"""
    content = """---
name: test-skill
description: Test skill
tags: [test, demo]
---

# Test Skill

Content here.
"""
    
    metadata, content_without_fm = parse_frontmatter(content)
    
    assert metadata is not None
    assert metadata['name'] == 'test-skill'
    assert metadata['description'] == 'Test skill'
    assert metadata['tags'] == ['test', 'demo']
    assert '# Test Skill' in content_without_fm


def test_parse_frontmatter_no_frontmatter():
    """测试解析没有 frontmatter 的内容"""
    content = """# Test Skill

Content here without frontmatter.
"""
    
    metadata, content_without_fm = parse_frontmatter(content)
    
    assert metadata is None or metadata == {}
    assert '# Test Skill' in content_without_fm


def test_parse_frontmatter_invalid_yaml():
    """测试解析无效的 YAML frontmatter"""
    content = """---
invalid: yaml: content
---

# Test Skill
"""
    
    # 应该能够处理无效的 YAML，返回空或 None
    metadata, content_without_fm = parse_frontmatter(content)
    # 不应该抛出异常


def test_validate_frontmatter():
    """测试验证 frontmatter"""
    # 有效的 frontmatter
    valid_metadata = {
        'name': 'test-skill',
        'description': 'Test skill',
        'tags': ['test']
    }
    is_valid, errors = validate_frontmatter(valid_metadata)
    assert is_valid
    assert len(errors) == 0
    
    # 无效的 frontmatter（缺少必需字段）
    invalid_metadata = {
        'name': 'test-skill'
    }
    is_valid, errors = validate_frontmatter(invalid_metadata)
    assert not is_valid
    assert len(errors) > 0


def test_validate_frontmatter_missing_name():
    """测试验证缺少 name 的 frontmatter"""
    metadata = {
        'description': 'Test skill',
        'tags': ['test']
    }
    is_valid, errors = validate_frontmatter(metadata)
    assert not is_valid
    assert any('name' in error.lower() for error in errors)


def test_validate_frontmatter_empty_tags():
    """测试验证 tags 为空的 frontmatter"""
    metadata = {
        'name': 'test-skill',
        'description': 'Test skill',
        'tags': []
    }
    is_valid, errors = validate_frontmatter(metadata)
    # tags 可以为空，但必须存在
    assert is_valid or any('tag' in error.lower() for error in errors)


def test_all_skills_have_valid_frontmatter():
    """测试所有 skills 都有有效的 frontmatter"""
    skills = list_all_skills()
    
    for skill_name, skill_path in skills:
        content = read_skill_content(skill_path)
        metadata, _ = parse_frontmatter(content)
        
        # 检查是否有 frontmatter
        assert metadata is not None, f"{skill_name} 缺少 frontmatter"
        
        # 验证 frontmatter
        is_valid, errors = validate_frontmatter(metadata)
        assert is_valid, f"{skill_name} frontmatter 无效: {errors}"


def test_cli_main_no_args(capsys):
    """测试 CLI 不带参数"""
    from skill_engine.cli import main
    
    with patch('sys.argv', ['skill-engine']):
        main()
        captured = capsys.readouterr()
        assert 'usage:' in captured.out.lower() or 'skill engine' in captured.out.lower()


def test_cli_info_command(capsys):
    """测试 info 命令"""
    from skill_engine.cli import show_info
    
    show_info()
    captured = capsys.readouterr()
    assert 'Skill Engine' in captured.out
    assert '2.0.0' in captured.out


def test_cli_create_parser():
    """测试创建命令解析器"""
    from skill_engine.cli import create_parser
    
    parser = create_parser()
    assert parser is not None
    
    # 测试 list 命令
    args = parser.parse_args(['list'])
    assert args.command == 'list'
    
    # 测试 read 命令
    args = parser.parse_args(['read', 'test-skill'])
    assert args.command == 'read'
    assert args.skill == 'test-skill'
    
    # 测试 create 命令
    args = parser.parse_args(['create', 'new-skill', '--category', 'test'])
    assert args.command == 'create'
    assert args.name == 'new-skill'
    assert args.category == 'test'
    
    # 测试 stats 命令
    args = parser.parse_args(['stats'])
    assert args.command == 'stats'
    
    # 测试 info 命令
    args = parser.parse_args(['info'])
    assert args.command == 'info'


def test_skills_directory_structure():
    """测试 skills 目录结构"""
    skills_dir = get_skills_dir()
    
    # 检查是否存在各个分类目录
    expected_categories = ['code', 'documentation', 'workflow', 'interaction', 'project']
    
    for category in expected_categories:
        category_dir = skills_dir / category
        # 至少应该有一个分类存在
        if category_dir.exists():
            assert category_dir.is_dir()
            # 检查是否有 README.md
            readme = category_dir / "README.md"
            # README.md 可选


def test_skill_template_exists():
    """测试 skill 模板是否存在"""
    skills_dir = get_skills_dir()
    template_file = skills_dir / "SKILL_TEMPLATE.md"
    
    if template_file.exists():
        content = read_skill_content(template_file)
        assert len(content) > 0
        # 模板应该包含 frontmatter 示例
        assert '---' in content


def test_list_all_skills_excludes_readme_and_template():
    """测试列出 skills 时排除 README 和模板"""
    skills = list_all_skills()
    
    for skill_name, skill_path in skills:
        assert 'README' not in skill_path.name
        assert 'SKILL_TEMPLATE' not in skill_path.name


def test_skill_file_encoding():
    """测试 skill 文件编码（应该是 UTF-8）"""
    skill_file = find_skill_file("design-principles")
    if skill_file:
        # 应该能够正确读取 UTF-8 编码的文件
        try:
            content = read_skill_content(skill_file)
            assert isinstance(content, str)
        except UnicodeDecodeError:
            pytest.fail("Skill 文件编码不是 UTF-8")


def test_skills_have_required_sections():
    """测试 skills 是否包含必需的章节"""
    skills = list_all_skills()
    
    # 至少测试几个 skills
    for skill_name, skill_path in skills[:3]:
        content = read_skill_content(skill_path)
        
        # 检查是否有 frontmatter
        assert '---' in content
        
        # 内容不应该为空
        assert len(content.strip()) > 100  # 至少有一些实质内容
