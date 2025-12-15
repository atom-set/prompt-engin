# 使用指南

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin

# 安装依赖
pip install -r requirements.txt

# 安装到系统
pip install -e .
```

### 基本使用

#### 1. 列出可用的提示词

```bash
prompt-engine list
```

#### 2. 合并提示词

```bash
# 合并所有提示词
prompt-engine merge --output combined.md

# 按阶段合并
prompt-engine merge --stage common --output common.md

# 按类型合并
prompt-engine merge --type frontend --output frontend.md

# 合并指定文件
prompt-engine merge file1.md file2.md --output merged.md
```

#### 3. 验证提示词

```bash
# 验证单个文件
prompt-engine validate prompts/stages/common/mode/common/mode-common.md

# 验证目录（递归）
prompt-engine validate prompts/stages/common/ --recursive
```

#### 4. 生成提示词

```bash
# 根据模板生成
prompt-engine generate --template prompts/templates/common.md --output output.md

# 使用变量
prompt-engine generate --template prompts/templates/common.md --output output.md --var name=MyPrompt --var version=1.0
```

## 提示词组织

### 目录结构

```
prompts/
├── templates/        # 通用模板
├── stages/          # 按阶段组织
│   ├── common/      # 通用阶段
│   ├── requirements/# 需求分析阶段
│   ├── design/      # 设计阶段
│   ├── development/ # 开发阶段
│   ├── testing/     # 测试阶段
│   └── documentation/# 文档阶段
└── types/           # 按项目类型组织
    ├── frontend/    # 前端项目
    ├── backend/     # 后端项目
    ├── fullstack/   # 全栈项目
    └── mobile/      # 移动端项目
```

### 提示词格式

每个提示词文件应遵循以下格式：

```markdown
# 提示词标题

## 概述

[描述提示词的用途和适用范围]

## 提示词内容

[提示词的具体内容]

## 使用说明

[如何使用这个提示词]

## 注意事项

[需要注意的事项]
```

## 高级用法

### 使用 Python API

```python
from prompt_engine import PromptParser, PromptMerger, PromptValidator

# 解析提示词
parser = PromptParser()
prompt = parser.parse_file("prompts/stages/common/mode/common/mode-common.md")

# 合并提示词
merger = PromptMerger()
output = merger.merge_by_stage("common", "output.md")

# 验证提示词
validator = PromptValidator()
is_valid, errors = validator.validate_file("prompts/stages/common/mode/common/mode-common.md")
```

### 使用 Shell 脚本

```bash
# 合并所有提示词
bash scripts/core/merge_prompts.sh

# 验证所有提示词
bash scripts/utils/validate_prompts.sh
```

## 常见问题

### Q: 如何添加新的提示词？

A: 在对应的目录下创建 Markdown 文件，遵循提示词格式规范。

### Q: 如何自定义合并顺序？

A: 修改 `scripts/core/merge_prompts.sh` 中的阶段和类型顺序。

### Q: 提示词验证失败怎么办？

A: 检查提示词文件是否包含必需的标题和概述部分。

## 更多资源

- [API 文档](../api/README.md)
- [示例项目](../../examples/README.md)
- [贡献指南](../../CONTRIBUTING.md)

