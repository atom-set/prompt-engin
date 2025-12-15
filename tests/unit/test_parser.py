"""
测试提示词解析器
"""

import pytest
from pathlib import Path
from prompt_engine.parser import PromptParser


@pytest.fixture
def parser():
    """创建解析器实例"""
    project_root = Path(__file__).parent.parent.parent
    return PromptParser(base_path=str(project_root))


def test_parse_file(parser):
    """测试解析单个文件"""
    prompt = parser.parse_file("prompts/stages/common/mode/common/mode-common.md")
    assert "path" in prompt
    assert "content" in prompt
    assert "metadata" in prompt
    assert prompt["path"] == "prompts/stages/common/mode/common/mode-common.md"


def test_parse_file_not_found(parser):
    """测试解析不存在的文件"""
    with pytest.raises(FileNotFoundError):
        parser.parse_file("non-existent-file.md")


def test_parse_directory(parser):
    """测试解析目录"""
    prompts = parser.parse_directory("prompts/stages/common/")
    assert isinstance(prompts, list)
    # 至少应该有一个文件
    assert len(prompts) > 0


def test_extract_metadata(parser):
    """测试提取元数据"""
    content = """# 测试标题

## 概述

这是一个测试概述。

## 其他内容

其他内容。
"""
    metadata = parser._extract_metadata(content)
    assert "title" in metadata
    assert metadata["title"] == "测试标题"
    assert "overview" in metadata
    assert "测试概述" in metadata["overview"]

