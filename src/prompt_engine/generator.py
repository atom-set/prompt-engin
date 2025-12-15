"""
提示词生成器模块。

提供根据模板生成提示词的功能。
"""

from pathlib import Path
from typing import Dict, List, Optional


class PromptGenerator:
    """提示词生成器类。"""

    def __init__(self, base_path: Optional[str] = None):
        """
        初始化生成器。

        Args:
            base_path: 提示词基础路径，默认为当前目录
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def generate_from_template(
        self,
        template_path: str,
        output_path: str,
        variables: Optional[Dict[str, str]] = None,
    ) -> str:
        """
        根据模板生成提示词。

        Args:
            template_path: 模板文件路径
            output_path: 输出文件路径
            variables: 模板变量字典

        Returns:
            输出文件路径
        """
        template_file = self.base_path / template_path
        if not template_file.exists():
            raise FileNotFoundError(f"模板文件不存在: {template_file}")

        # 读取模板内容
        with open(template_file, "r", encoding="utf-8") as f:
            content = f.read()

        # 替换变量
        if variables:
            for key, value in variables.items():
                content = content.replace(f"{{{{{key}}}}}", value)

        # 写入输出文件
        output_file = self.base_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(content)

        return str(output_file)

    def list_templates(self, template_dir: str = "prompts/templates") -> List[str]:
        """
        列出可用的模板。

        Args:
            template_dir: 模板目录路径

        Returns:
            模板文件路径列表
        """
        template_path = self.base_path / template_dir
        if not template_path.exists():
            return []

        templates = []
        for file_path in template_path.glob("*.md"):
            if file_path.is_file() and file_path.name != "README.md":
                relative_path = file_path.relative_to(self.base_path)
                templates.append(str(relative_path))

        return templates

