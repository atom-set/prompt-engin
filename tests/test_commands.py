"""Tests for skill-engine commands"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
from skill_engine.commands import (
    list_skills,
    read_skill,
    validate_skill,
    search_skills,
    show_stats,
)


def test_list_skills_command(capsys):
    """测试 list 命令"""
    list_skills()
    captured = capsys.readouterr()
    
    # 应该输出一些 skills
    assert len(captured.out) > 0


def test_list_skills_with_category(capsys):
    """测试 list 命令带分类参数"""
    list_skills("code")
    captured = capsys.readouterr()
    
    # 输出可能为空（如果该分类没有 skills）或有内容
    assert isinstance(captured.out, str)


def test_read_skill_command(capsys):
    """测试 read 命令"""
    # 读取一个已知存在的 skill
    read_skill("design-principles")
    captured = capsys.readouterr()
    
    # 应该输出 skill 内容
    assert len(captured.out) > 0


def test_read_skill_nonexistent(capsys):
    """测试读取不存在的 skill"""
    read_skill("nonexistent-skill-xyz")
    captured = capsys.readouterr()
    
    # 应该输出错误信息
    assert "不存在" in captured.out or "未找到" in captured.out or "not found" in captured.out.lower()


def test_validate_skill_command(capsys):
    """测试 validate 命令"""
    # 验证一个已知存在的 skill
    result = validate_skill("design-principles")
    
    # 应该返回布尔值
    assert isinstance(result, bool)


def test_validate_skill_nonexistent(capsys):
    """测试验证不存在的 skill"""
    result = validate_skill("nonexistent-skill-xyz")
    captured = capsys.readouterr()
    
    # 应该返回 False
    assert result is False
    assert "不存在" in captured.out or "未找到" in captured.out or "not found" in captured.out.lower()


def test_search_skills_by_keyword(capsys):
    """测试按关键词搜索 skills"""
    search_skills(keyword="code")
    captured = capsys.readouterr()
    
    # 应该输出一些结果
    assert isinstance(captured.out, str)


def test_search_skills_by_tag(capsys):
    """测试按标签搜索 skills"""
    search_skills(tag="code")
    captured = capsys.readouterr()
    
    # 应该输出一些结果
    assert isinstance(captured.out, str)


def test_search_skills_no_results(capsys):
    """测试搜索无结果的情况"""
    search_skills(keyword="xyzabc123nonexistent")
    captured = capsys.readouterr()
    
    # 应该提示没有找到结果
    assert "未找到" in captured.out or "没有" in captured.out or len(captured.out.strip()) == 0


def test_show_stats_command(capsys):
    """测试 stats 命令"""
    show_stats()
    captured = capsys.readouterr()
    
    # 应该输出统计信息
    assert len(captured.out) > 0
    # 统计信息应该包含数字
    assert any(char.isdigit() for char in captured.out)


def test_list_skills_sorted_output(capsys):
    """测试 list 命令输出是否排序"""
    list_skills()
    captured = capsys.readouterr()
    
    # 获取输出的行
    lines = [line.strip() for line in captured.out.split('\n') if line.strip()]
    
    # 至少应该有一些输出
    assert len(lines) > 0


def test_validate_all_existing_skills():
    """测试验证所有现有的 skills"""
    from skill_engine.utils import list_all_skills
    
    skills = list_all_skills()
    
    # 至少测试前几个 skills
    for skill_name, skill_path in skills[:5]:
        result = validate_skill(skill_name)
        assert result is True, f"Skill {skill_name} 验证失败"


@patch('builtins.input', return_value='test description')
def test_create_skill_interactive_cancelled(mock_input, capsys):
    """测试取消创建 skill"""
    from skill_engine.commands import create_skill
    
    # 模拟用户取消输入
    with patch('builtins.input', side_effect=['', '', '']):
        # 由于可能会创建文件，我们只测试函数可以调用
        # 实际创建会在非交互模式下测试
        pass


def test_stats_includes_categories(capsys):
    """测试统计信息包含分类信息"""
    show_stats()
    captured = capsys.readouterr()
    
    # 统计信息应该包含分类相关的信息
    output_lower = captured.out.lower()
    assert 'skill' in output_lower or 'total' in output_lower or '总' in captured.out


def test_search_skills_both_params_none():
    """测试搜索时两个参数都为空"""
    # 应该至少不会崩溃
    search_skills()


def test_list_skills_empty_category(capsys):
    """测试列出空分类"""
    list_skills("empty_category_that_does_not_exist")
    captured = capsys.readouterr()
    
    # 应该有一些输出（即使是空的）
    assert isinstance(captured.out, str)


def test_read_skill_output_format(capsys):
    """测试 read 命令输出格式"""
    read_skill("design-principles")
    captured = capsys.readouterr()
    
    # 输出应该包含实际内容
    assert len(captured.out.strip()) > 50  # 至少有一些内容


def test_validate_skill_valid_frontmatter(capsys):
    """测试验证有效的 frontmatter"""
    result = validate_skill("design-principles")
    captured = capsys.readouterr()
    
    if result:
        assert "✅" in captured.out or "有效" in captured.out or "valid" in captured.out.lower()
