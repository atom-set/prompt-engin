"""
提示词验证器模块。

提供验证提示词格式和完整性的功能。
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple


class PromptValidator:
    """提示词验证器类。"""

    def __init__(self, base_path: Optional[str] = None):
        """
        初始化验证器。

        Args:
            base_path: 提示词基础路径，默认为当前目录
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def validate_file(self, file_path: str) -> Tuple[bool, List[str]]:
        """
        验证单个提示词文件。

        Args:
            file_path: 文件路径

        Returns:
            (是否有效, 错误列表)
        """
        errors = []
        full_path = self.base_path / file_path

        # 检查文件是否存在
        if not full_path.exists():
            errors.append(f"文件不存在: {file_path}")
            return False, errors

        # 读取文件内容
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            errors.append(f"读取文件失败: {e}")
            return False, errors

        # 验证内容格式
        content_errors = self._validate_content(content, file_path)
        errors.extend(content_errors)

        return len(errors) == 0, errors

    def validate_directory(self, dir_path: str, recursive: bool = True) -> Dict[str, Tuple[bool, List[str]]]:
        """
        验证目录下的所有提示词文件。

        Args:
            dir_path: 目录路径
            recursive: 是否递归验证子目录

        Returns:
            文件路径到验证结果的映射
        """
        full_path = self.base_path / dir_path
        if not full_path.exists():
            return {}

        results = {}
        pattern = "**/*.md" if recursive else "*.md"

        for file_path in full_path.glob(pattern):
            if file_path.is_file() and file_path.name != "README.md":
                relative_path = file_path.relative_to(self.base_path)
                is_valid, errors = self.validate_file(str(relative_path))
                results[str(relative_path)] = (is_valid, errors)

        return results

    def _validate_content(self, content: str, file_path: str) -> List[str]:
        """
        验证内容格式。

        Args:
            content: 文件内容
            file_path: 文件路径（用于错误提示）

        Returns:
            错误列表
        """
        errors = []
        lines = content.split("\n")

        # 检查是否有标题
        has_title = False
        for line in lines:
            if line.startswith("# "):
                has_title = True
                break

        if not has_title:
            errors.append(f"{file_path}: 缺少标题（应以 # 开头）")

        # 检查是否有概述部分
        has_overview = False
        for i, line in enumerate(lines):
            if line.strip() == "## 概述":
                has_overview = True
                # 检查概述是否有内容
                if i + 1 < len(lines) and lines[i + 1].strip():
                    break
                else:
                    errors.append(f"{file_path}: 概述部分为空")
                    break

        if not has_overview:
            errors.append(f"{file_path}: 缺少概述部分（## 概述）")

        # 检查内容是否为空
        if not content.strip():
            errors.append(f"{file_path}: 文件内容为空")

        return errors

