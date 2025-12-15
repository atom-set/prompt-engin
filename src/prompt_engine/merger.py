"""
提示词合并器模块。

提供合并多个提示词文件的功能。
"""

from pathlib import Path
from typing import List, Optional


class PromptMerger:
    """提示词合并器类。"""

    def __init__(self, base_path: Optional[str] = None):
        """
        初始化合并器。

        Args:
            base_path: 提示词基础路径，默认为当前目录
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    def merge(
        self,
        prompt_files: List[str],
        output_path: str,
        add_separators: bool = True,
        add_source_comments: bool = True,
    ) -> str:
        """
        合并多个提示词文件。

        Args:
            prompt_files: 提示词文件路径列表
            output_path: 输出文件路径
            add_separators: 是否添加分隔线
            add_source_comments: 是否添加来源注释

        Returns:
            输出文件路径
        """
        output_file = self.base_path / output_path
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, "w", encoding="utf-8") as f:
            # 写入文件头
            f.write("# 合并的提示词文件\n")
            f.write("# 本文件由多个提示词文件合并生成\n\n")

            # 合并每个文件
            for prompt_file in prompt_files:
                full_path = self.base_path / prompt_file
                if not full_path.exists():
                    print(f"警告: 文件不存在，跳过: {prompt_file}")
                    continue

                # 添加分隔线和来源注释
                if add_separators:
                    f.write("\n")
                    f.write("# " + "=" * 75 + "\n")
                if add_source_comments:
                    f.write(f"# 来源: {prompt_file}\n")
                if add_separators:
                    f.write("# " + "=" * 75 + "\n")
                    f.write("\n")

                # 写入文件内容
                with open(full_path, "r", encoding="utf-8") as src:
                    f.write(src.read())

                # 添加空行分隔
                if add_separators:
                    f.write("\n")

        return str(output_file)

    def merge_by_stage(
        self,
        stage: str,
        output_path: str,
        recursive: bool = True,
    ) -> str:
        """
        按阶段合并提示词。

        Args:
            stage: 阶段名称（如 common, development）
            output_path: 输出文件路径
            recursive: 是否递归查找子目录

        Returns:
            输出文件路径
        """
        stage_dir = self.base_path / "prompts" / "stages" / stage
        if not stage_dir.exists():
            raise FileNotFoundError(f"阶段目录不存在: {stage_dir}")

        prompt_files = []
        pattern = "**/*.md" if recursive else "*.md"

        for file_path in stage_dir.glob(pattern):
            if file_path.is_file() and file_path.name != "README.md":
                relative_path = file_path.relative_to(self.base_path)
                prompt_files.append(str(relative_path))

        return self.merge(prompt_files, output_path)

    def merge_by_type(
        self,
        project_type: str,
        output_path: str,
        recursive: bool = True,
    ) -> str:
        """
        按项目类型合并提示词。

        Args:
            project_type: 项目类型（如 frontend, backend）
            output_path: 输出文件路径
            recursive: 是否递归查找子目录

        Returns:
            输出文件路径
        """
        type_dir = self.base_path / "prompts" / "types" / project_type
        if not type_dir.exists():
            raise FileNotFoundError(f"类型目录不存在: {type_dir}")

        prompt_files = []
        pattern = "**/*.md" if recursive else "*.md"

        for file_path in type_dir.glob(pattern):
            if file_path.is_file() and file_path.name != "README.md":
                relative_path = file_path.relative_to(self.base_path)
                prompt_files.append(str(relative_path))

        return self.merge(prompt_files, output_path)

