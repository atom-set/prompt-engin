# API 文档

## 核心模块

### PromptParser

提示词解析器，用于解析提示词文件。

```python
from prompt_engine import PromptParser

parser = PromptParser(base_path=".")
prompt = parser.parse_file("prompts/stages/common/mode/common/mode-common.md")
prompts = parser.parse_directory("prompts/stages/common/")
```

#### 方法

- `parse_file(file_path: str) -> Dict[str, any]` - 解析单个文件
- `parse_directory(dir_path: str, recursive: bool = True) -> List[Dict[str, any]]` - 解析目录

### PromptMerger

提示词合并器，用于合并多个提示词文件。

```python
from prompt_engine import PromptMerger

merger = PromptMerger(base_path=".")
output = merger.merge(["file1.md", "file2.md"], "output.md")
output = merger.merge_by_stage("common", "output.md")
output = merger.merge_by_type("frontend", "output.md")
```

#### 方法

- `merge(prompt_files: List[str], output_path: str, ...) -> str` - 合并文件列表
- `merge_by_stage(stage: str, output_path: str, ...) -> str` - 按阶段合并
- `merge_by_type(project_type: str, output_path: str, ...) -> str` - 按类型合并

### PromptValidator

提示词验证器，用于验证提示词格式。

```python
from prompt_engine import PromptValidator

validator = PromptValidator(base_path=".")
is_valid, errors = validator.validate_file("prompts/stages/common/mode/common/mode-common.md")
results = validator.validate_directory("prompts/stages/common/")
```

#### 方法

- `validate_file(file_path: str) -> Tuple[bool, List[str]]` - 验证单个文件
- `validate_directory(dir_path: str, recursive: bool = True) -> Dict[str, Tuple[bool, List[str]]]` - 验证目录

### PromptGenerator

提示词生成器，用于根据模板生成提示词。

```python
from prompt_engine import PromptGenerator

generator = PromptGenerator(base_path=".")
output = generator.generate_from_template("template.md", "output.md", {"name": "MyPrompt"})
templates = generator.list_templates()
```

#### 方法

- `generate_from_template(template_path: str, output_path: str, variables: Optional[Dict[str, str]] = None) -> str` - 根据模板生成
- `list_templates(template_dir: str = "prompts/templates") -> List[str]` - 列出模板

## CLI 命令

### merge

合并提示词文件。

```bash
prompt-engine merge [OPTIONS] [FILES]...
```

选项：
- `--output, -o` - 输出文件路径
- `--stage` - 按阶段合并
- `--type` - 按类型合并

### validate

验证提示词文件格式。

```bash
prompt-engine validate [OPTIONS] PATH
```

选项：
- `--recursive, -r` - 递归验证子目录

### generate

根据模板生成提示词。

```bash
prompt-engine generate [OPTIONS]
```

选项：
- `--template, -t` - 模板文件路径
- `--output, -o` - 输出文件路径
- `--var` - 模板变量（格式: key=value）

### list

列出可用的提示词模板。

```bash
prompt-engine list
```

---

**最后更新**：2025-12-20

