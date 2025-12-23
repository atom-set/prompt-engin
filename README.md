# Prompt Engine

> 🚀 一个用于结构化管理和组织提示词的开源工程

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**🔍 GitHub Topics**: 
- **🎯 核心关键字（提示词）**：`prompt` `prompt-engineering` `prompt-template` `prompt-management` `prompt-library` `prompt-optimization` `prompt-versioning` `prompt-validation`
- **AI 相关**：`ai-assistant` `llm` `chatgpt` `claude` `cursor` `ai-tools` `ai-development` `ai-generated`
- **规则相关**：`rules` `rule-engine` `rule-management` `cursor-rules`
- **工具相关**：`developer-tools` `cli-tool` `template-engine` `automation` `markdown` `yaml` `python` `software-engineering`

## 📋 简介

**Prompt Engine** 是一个**提示词（Prompt）**结构化工程，旨在帮助开发者更好地组织、管理和复用提示词。通过模块化的方式，将提示词按阶段和类型进行分类管理，支持模板化、版本控制和批量处理。

> **🎯 核心定位**：专注于**提示词工程（Prompt Engineering）**，为 AI 辅助开发提供结构化的提示词库和模板系统。

> **💡 特别说明**：本工程完全由 AI 全自动生成，包括项目结构、代码实现、文档和所有提示词模板。这展示了 AI 在软件工程和提示词工程领域的强大能力。

### 核心特性

- 📝 **提示词管理**：结构化组织和管理提示词（Prompts），支持按阶段和类型分类
- 📦 **模块化组织**：按研发阶段和项目类型组织提示词，便于查找和使用
- 🔄 **版本管理**：支持提示词的版本追踪和更新，确保提示词质量
- 🎨 **模板系统**：提供可复用的提示词模板，快速生成高质量提示词
- ✅ **格式验证**：自动验证提示词格式的完整性和规范性
- 🔍 **智能搜索**：支持按关键字、阶段、类型快速搜索提示词
- 🔧 **CLI 工具**：提供命令行接口，方便集成到开发流程
- 📚 **丰富文档**：完整的使用指南和示例，快速上手

> 📋 **提示词概述**：查看 [提示词概述文档](./PROMPTS_OVERVIEW.md) 了解所有提示词的描述和应用场景

## 🚀 快速开始

### 快速使用提示词（推荐）

在 Cursor IDE 中，您可以直接使用以下提示词快速引用规则文件：

- **`@.cursorrules.all`** - 引用全部规则（完整版，包含所有规则）
- **`@.cursorrules.core`** - 引用核心规则（精简版，只包含核心规则，Token 优化）

**使用示例**：

```
@.cursorrules.all 帮我分析这个代码问题
```

```
@.cursorrules.core 帮我实现一个用户登录功能
```

> 💡 **提示**：
> - `.cursorrules.all` 包含所有规则（约 8597 行），适合需要完整规则支持的项目
> - `.cursorrules.core` 只包含核心规则（约 3427 行），Token 占用减少约 60%，适合需要 Token 优化的项目
> - 两个文件都可以直接使用，无需额外配置

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

**方式1：使用包装脚本（推荐，无需安装）**

```bash
# 查看所有可用的提示词模板
python3 scripts/prompt-engine list

# 合并所有提示词文件（通用格式）
python3 scripts/prompt-engine merge --all --output combined.md

# 生成 Cursor IDE 规则文件
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 生成 TRAE IDE 规则文件
python3 scripts/prompt-engine merge --all --ide trae --output .traerules

# 生成 Antigravity IDE 规则文件
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules

# 同时生成 Cursor 和 TRAE IDE 规则文件
python3 scripts/prompt-engine merge --all --ide both --output rules

# 同时生成所有 IDE 规则文件（Cursor、TRAE、Antigravity）
python3 scripts/prompt-engine merge --all --ide all --output rules

# 合并特定阶段的提示词（Cursor IDE）
python3 scripts/prompt-engine merge --stage common --ide cursor --output .cursorrules

# 验证提示词格式
python3 scripts/prompt-engine validate prompts/stages/common/

# 根据模板生成提示词
python3 scripts/prompt-engine generate --template development --type backend
```

**方式2：安装后使用（需要先安装）**

```bash
# 安装项目（推荐使用虚拟环境）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# 然后可以直接使用命令
prompt-engine list
prompt-engine merge --output combined.md
prompt-engine validate prompts/stages/common/
```

## 📁 项目结构

```
prompt-engin/
├── src/
│   └── prompt_engine/      # 核心代码模块
│       ├── __init__.py
│       ├── parser.py        # 提示词解析器
│       ├── merger.py        # 提示词合并器
│       ├── validator.py     # 提示词验证器
│       └── generator.py     # 提示词生成器
├── prompts/                # 提示词模板目录
│   ├── templates/           # 通用提示词模板
│   ├── stages/             # 按阶段组织的提示词
│   │   ├── common/         # 通用阶段提示词
│   │   ├── requirements/   # 需求分析阶段提示词
│   │   ├── design/         # 设计阶段提示词
│   │   ├── development/    # 开发阶段提示词
│   │   ├── testing/        # 测试阶段提示词
│   │   └── documentation/  # 文档阶段提示词
│   └── types/              # 按项目类型组织的提示词
│       ├── frontend/       # 前端项目提示词
│       ├── backend/        # 后端项目提示词
│       ├── fullstack/      # 全栈项目提示词
│       └── mobile/         # 移动端项目提示词
├── scripts/                # 工具脚本
│   ├── core/               # 核心脚本
│   └── utils/              # 工具脚本
├── docs/                   # 文档目录
│   ├── guides/             # 使用指南
│   ├── api/                # API 文档
│   └── examples/           # 示例文档
├── examples/               # 示例项目
├── tests/                  # 测试目录
├── config/                 # 配置文件
└── README.md               # 本文件
```

## 📖 使用指南

### 提示词组织方式

提示词按以下维度组织：

1. **阶段维度**：按研发流程阶段组织
   - `common/` - 通用阶段提示词
   - `requirements/` - 需求分析阶段提示词
   - `design/` - 设计阶段提示词
   - `development/` - 开发阶段提示词
   - `testing/` - 测试阶段提示词
   - `documentation/` - 文档阶段提示词

2. **类型维度**：按项目类型组织
   - `frontend/` - 前端项目提示词
   - `backend/` - 后端项目提示词
   - `fullstack/` - 全栈项目提示词
   - `mobile/` - 移动端项目提示词

### 创建提示词模板

在对应的目录下创建 Markdown 文件：

```markdown
# [阶段名称] 提示词模板

## 概述

[描述本提示词的用途和适用范围]

## 提示词内容

[提示词的具体内容]

## 使用说明

[如何使用这个提示词]

## 注意事项

[需要注意的事项]
```

### 合并提示词

```bash
# 合并所有提示词到一个文件
prompt-engine merge --output combined.md

# 合并特定阶段的提示词
prompt-engine merge --stage development --output dev.md

# 合并特定类型的提示词
prompt-engine merge --type backend --output backend.md
```

### IDE 适配支持

Prompt Engine 支持生成适用于不同 AI 辅助 IDE 的规则文件：

#### Cursor IDE 支持

生成适用于 [Cursor IDE](https://cursor.sh/) 的 `.cursorrules` 文件：

```bash
# 生成完整的 Cursor 规则文件
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 生成特定阶段的 Cursor 规则文件
python3 scripts/prompt-engine merge --stage common --ide cursor --output .cursorrules
```

生成的 `.cursorrules` 文件可以直接放在项目根目录，Cursor IDE 会自动识别并使用。

#### TRAE IDE 支持

生成适用于 [TRAE IDE](https://traeide.ai-kit.cn/) 的 `.traerules` 文件：

```bash
# 生成完整的 TRAE 规则文件
python3 scripts/prompt-engine merge --all --ide trae --output .traerules

# 生成特定阶段的 TRAE 规则文件
python3 scripts/prompt-engine merge --stage common --ide trae --output .traerules
```

生成的 `.traerules` 文件可以直接放在项目根目录，TRAE IDE 会自动识别并使用。

#### Antigravity IDE 支持

生成适用于 [Antigravity IDE](https://antigravity.dev/) 的 `.antigravityrules` 文件：

```bash
# 生成完整的 Antigravity 规则文件
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules

# 生成特定阶段的 Antigravity 规则文件
python3 scripts/prompt-engine merge --stage common --ide antigravity --output .antigravityrules
```

生成的 `.antigravityrules` 文件可以直接放在项目根目录，Antigravity IDE 会自动识别并使用。

#### 同时生成多个 IDE 规则文件

如果需要同时支持多个 IDE，可以使用 `both` 或 `all` 选项：

```bash
# 同时生成 Cursor 和 TRAE IDE 规则文件
python3 scripts/prompt-engine merge --all --ide both --output rules

# 这会生成两个文件：
# - rules.cursorrules
# - rules.traerules

# 同时生成所有 IDE 规则文件（Cursor、TRAE、Antigravity）
python3 scripts/prompt-engine merge --all --ide all --output rules

# 这会生成三个文件：
# - rules.cursorrules
# - rules.traerules
# - rules.antigravityrules
```

#### IDE 格式说明

- **cursor**：生成适用于 Cursor IDE 的规则文件（`.cursorrules`）
- **trae**：生成适用于 TRAE IDE 的规则文件（`.traerules`）
- **antigravity**：生成适用于 Antigravity IDE 的规则文件（`.antigravityrules`）
- **both**：同时生成 Cursor 和 TRAE IDE 的规则文件
- **all**：同时生成所有 IDE（Cursor、TRAE、Antigravity）的规则文件

> 💡 **提示**：如果不指定 `--ide` 选项，将生成通用的 Markdown 格式文件，适用于任何场景。

### 技能系统（Skills）支持

Prompt Engine 支持将部分规则转换为技能（Skills），实现 Token 优化和按需加载。

> **🎯 推荐说明**：Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：
> - **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
> - **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用
> 
> 两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

#### Token 优化

**问题**：完整版规则文件较大（8597 行，约 328KB），占用大量 token。

**解决方案**：将可选规则转换为技能，只保留核心规则在 `.cursorrules` 中。

**效果**：
- 初始上下文 token 减少 **约 60%**（从 8597 行减少到 3427 行）
- 按需加载，只在需要时加载相关技能
- 灵活配置，用户可以选择使用方式

#### 两种使用方式（推荐）

**⭐ 方式2：精简版规则文件 + 技能系统（Token 优化）** ✅ **重点推荐**

> ✅ **已实现**：`--core-only` 选项已可用！

> ✅ **已实现**：`--core-only` 选项已可用！

```bash
# 1. 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 2. 复制到项目
cp .cursorrules /path/to/project/

# 3. 安装技能（按需）

# 方式A：批量安装技能（推荐）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/project
# 脚本会提示：
#   1. 安装所有技能（全选）
#   2. 选择要安装的技能（交互式选择）
#   3. 取消安装

# 然后选择要使用的技能
cd /path/to/project
openskills sync -y

# 方式B：安装单个技能
cd /path/to/project
# ⚠️ 重要：openskills install 只能安装单个技能目录，不能安装整个 .claude/skills/ 目录
# ✅ 正确：安装单个技能
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format
# ❌ 错误：不能安装整个目录
# openskills install /path/to/prompt-engin/.claude/skills  # 这会失败！

# 同步到 AGENTS.md
openskills sync -y
```

**特点**：
- ✅ **Token 占用减少约 60%**（从 8597 行减少到 3427 行）
- ✅ **按需加载**，灵活配置
- ✅ **推荐用于所有项目**，特别是大项目
- ⚠️ 需要 OpenSkills 工具支持

**适用场景**：
- ✅ **所有项目**（推荐优先使用）
- ✅ 大项目，需要 token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

---

**方式1：完整版规则文件（简单直接）** ✅ **适用于小项目**

```bash
# 生成完整版规则文件（包含所有规则）
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 复制到项目
cp .cursorrules /path/to/project/
```

**特点**：
- ✅ 简单直接，复制即用
- ✅ 所有规则始终可用
- ⚠️ Token 占用较大（8597 行，约 308KB）

**适用场景**：
- ✅ 小项目，不需要 token 优化
- ✅ 希望所有规则始终可用
- ✅ 不想安装 OpenSkills 工具

#### 详细文档

- [批量安装指南](./docs/guides/BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法（推荐）
- [技能系统快速参考](./docs/guides/SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [快速使用指南](./docs/guides/QUICK_START_SKILLS.md) - 快速上手
- [使用示例](./docs/guides/USAGE_EXAMPLE.md) - 实际使用示例
- [技能创建指南](./docs/guides/SKILLS_CREATION.md) - 如何创建新技能
- [Token 优化指南](./docs/guides/token-optimization-guide.md) - Token 优化详细说明
- [技能使用指南](./docs/guides/skills-usage-guide.md) - 技能系统使用指南

## 🛠️ 开发

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/unit/test_parser.py

# 生成覆盖率报告
pytest --cov=src/prompt_engine
```

### 代码质量检查

```bash
# 格式化代码
black src/

# 检查代码风格
flake8 src/

# 类型检查
mypy src/
```

## 📝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献指南。

## 📄 许可证

本项目采用 [MIT 许可证](./LICENSE)。

### 🤖 AI 生成说明

本工程完全由 AI 全自动生成，包括：
- ✅ 项目结构和目录组织
- ✅ 所有源代码和实现
- ✅ 文档和使用指南
- ✅ 所有提示词模板和示例
- ✅ 测试用例和 CI/CD 配置

这展示了 AI 在软件工程领域的强大能力，从项目初始化到完整实现，全部由 AI 自动完成。

## 📚 相关资源

- [快速开始指南](./QUICK_START.md) - 快速开始使用
- [API 文档](./docs/api/README.md)
- [示例项目](./examples/README.md)
- [AI 生成说明](./AI_GENERATED.md) - 了解本项目的 AI 生成过程

---

**最后更新**：2025-12-20

