"""
提示词解析器模块。

提供解析提示词文件的功能。
"""

import os
from pathlib import Path
from typing import Dict, List, Optional


class PromptParser:
    """提示词解析器类。"""

    def __init__(self, base_path: Optional[str] = None):
        """
        初始化解析器。

        Args:
            base_path: 提示词基础路径，默认为当前目录
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def parse_file(self, file_path: str) -> Dict[str, any]:
        """
        解析单个提示词文件。

        Args:
            file_path: 文件路径

        Returns:
            包含提示词信息的字典
        """
        full_path = self.base_path / file_path
        if not full_path.exists():
            raise FileNotFoundError(f"文件不存在: {full_path}")

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {
            "path": str(file_path),
            "content": content,
            "metadata": self._extract_metadata(content),
        }

    def parse_directory(self, dir_path: str, recursive: bool = True) -> List[Dict[str, any]]:
        """
        解析目录下的所有提示词文件。

        Args:
            dir_path: 目录路径
            recursive: 是否递归解析子目录

        Returns:
            提示词信息列表
        """
        full_path = self.base_path / dir_path
        if not full_path.exists():
            raise FileNotFoundError(f"目录不存在: {full_path}")

        prompts = []
        pattern = "**/*.md" if recursive else "*.md"

        for file_path in full_path.glob(pattern):
            if file_path.is_file() and file_path.name != "README.md":
                relative_path = file_path.relative_to(self.base_path)
                try:
                    prompt = self.parse_file(str(relative_path))
                    prompts.append(prompt)
                except Exception as e:
                    print(f"警告: 解析文件失败 {relative_path}: {e}")

        return prompts

    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """
        从内容中提取元数据。

        Args:
            content: 文件内容

        Returns:
            元数据字典
        """
        metadata = {}
        lines = content.split("\n")

        # 提取标题（第一个 # 开头的行）
        for line in lines:
            if line.startswith("# "):
                metadata["title"] = line[2:].strip()
                break

        # 提取概述（## 概述 之后的内容）
        in_overview = False
        overview_lines = []
        for line in lines:
            if line.strip() == "## 概述":
                in_overview = True
                continue
            elif in_overview and line.startswith("##"):
                break
            elif in_overview:
                overview_lines.append(line.strip())

        if overview_lines:
            metadata["overview"] = "\n".join(overview_lines).strip()

        return metadata

