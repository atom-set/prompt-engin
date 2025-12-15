"""
测试提示词验证器
"""

import pytest
from pathlib import Path
from prompt_engine.validator import PromptValidator


@pytest.fixture
def validator():
    """创建验证器实例"""
    project_root = Path(__file__).parent.parent.parent
    return PromptValidator(base_path=str(project_root))


def test_validate_file(validator):
    """测试验证单个文件"""
    is_valid, errors = validator.validate_file("prompts/stages/common/mode/common/mode-common.md")
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)
    # 如果文件存在且格式正确，应该通过验证
    if is_valid:
        assert len(errors) == 0
    else:
        assert len(errors) > 0


def test_validate_file_not_found(validator):
    """测试验证不存在的文件"""
    is_valid, errors = validator.validate_file("non-existent-file.md")
    assert is_valid is False
    assert len(errors) > 0


def test_validate_directory(validator):
    """测试验证目录"""
    results = validator.validate_directory("prompts/stages/common/")
    assert isinstance(results, dict)
    # 至少应该有一个文件的验证结果
    assert len(results) > 0


def test_validate_content(validator):
    """测试验证内容格式"""
    # 有效内容
    valid_content = """# 标题

## 概述

这是概述内容。

## 其他内容

其他内容。
"""
    errors = validator._validate_content(valid_content, "test.md")
    assert len(errors) == 0

    # 无效内容（缺少标题）
    invalid_content = """## 概述

这是概述内容。
"""
    errors = validator._validate_content(invalid_content, "test.md")
    assert len(errors) > 0

