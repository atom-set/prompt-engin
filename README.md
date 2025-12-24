# Prompt Engine

> 🚀 一个用于结构化管理和组织提示词的开源工程

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**🔍 GitHub Topics**: 
- **🎯 核心关键字（提示词）**：`prompt` `prompt-engineering` `prompt-template` `prompt-management` `prompt-library` `prompt-optimization` `prompt-versioning` `prompt-validation`
- **AI 相关**：`ai-assistant` `llm` `chatgpt` `claude` `cursor` `ai-tools` `ai-development` `ai-generated`
- **规则相关**：`rules` `rule-engine` `rule-management` `cursor-rules`
- **工具相关**：`developer-tools` `cli-tool` `template-engine` `automation` `markdown` `yaml` `python` `software-engineering`

---

## 📋 简介

**Prompt Engine** 是一个**提示词（Prompt）**结构化工程，帮助开发者更好地组织、管理和复用提示词。

**核心特性**：
- 📝 结构化组织提示词（按阶段和类型分类）
- 🔄 支持版本管理和批量处理
- 🎨 提供可复用的提示词模板
- 🔧 提供 CLI 工具，方便集成到开发流程
- 📚 支持多个 IDE 平台（Cursor、TRAE、Antigravity）

> 📖 **详细说明**：查看 [完整介绍文档](./docs/guides/INTRODUCTION.md)（待创建）  
> 📋 **提示词概述**：查看 [提示词概述文档](./PROMPTS_OVERVIEW.md) 了解所有提示词的描述和应用场景

---

## 🔧 环境安装和测试

### 系统要求

- **Python**：3.8 或更高版本
- **操作系统**：macOS、Linux、Windows
- **依赖**：见 `requirements.txt`

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装到系统（可选，用于全局使用 prompt-engine 命令）
pip install -e .
```

### 环境测试

运行环境测试脚本，检查环境是否正确配置：

```bash
# 测试环境（Shell 脚本）
bash scripts/utils/test_environment.sh

# 或使用 Python 脚本（更详细的测试）
python3 scripts/utils/test_environment.py
```

**测试内容**：
- ✅ Python 版本检查（需要 3.8+）
- ✅ 依赖包检查（检查 requirements.txt 中的包）
- ✅ CLI 工具可用性检查（测试 prompt-engine 命令）
- ✅ 基本功能测试（list、validate 等命令）

> 📖 **详细说明**：查看 [环境安装和测试指南](./docs/guides/INSTALLATION_AND_TESTING.md)  
> ❓ **遇到问题？**：查看 [常见问题 FAQ](./docs/guides/FAQ.md)（待创建）

---

## 📖 使用手册

### 三种使用方式快速选择

Prompt Engine 支持**三种使用方式**，适用于不同的项目需求：

| 使用方式 | 特点 | Token 占用 | 适用场景 | 推荐度 |
|---------|------|-----------|---------|--------|
| **方式1：单文件完整版** | 简单直接，所有规则在一个文件 | 高（8597 行） | 小项目 | ⭐⭐⭐ |
| **方式2：单文件精简版 + 技能** | Token 优化，按需加载 | 低（3427 行 + 按需） | 大项目 | ⭐⭐⭐⭐⭐ |
| **方式3：多文件目录** | 精细控制，路径特定配置 | 中等（按需加载） | 大型/复杂项目 | ⭐⭐⭐⭐ |

> 💡 **快速选择**：
> - **小项目** → [方式1：单文件完整版](#方式1单文件完整版)
> - **大项目** → [方式2：单文件精简版 + 技能](#方式2单文件精简版--技能系统) ⭐ **推荐**
> - **大型/复杂项目** → [方式3：多文件目录](#方式3多文件目录)

### 三个平台支持

| 平台 | 单文件方式 | 多文件目录 | 状态 |
|------|----------|-----------|------|
| **[Cursor IDE](https://cursor.sh/)** | `.cursorrules` | `.cursor/rules/` | ✅ 完全支持 |
| **[TRAE IDE](https://traeide.ai-kit.cn/)** | `.traerules` | `.trae/ai-rules.yml` | ✅ 支持（YAML 格式） |
| **[Antigravity IDE](https://antigravity.dev/)** | `.antigravityrules` | `.agent` (代理配置) | ✅ 单文件支持 |

> 📖 **详细说明**：查看 [完整使用手册](./docs/guides/USAGE_MANUAL.md) 和 [V2 版本改进计划](./docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) ⭐ **推荐**

---

### 方式1：单文件完整版（最简单）

**适用场景**：小项目，不需要 Token 优化

**快速开始**：

```bash
# 1. 生成规则文件（选择你的 IDE）
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules
# 或
python3 scripts/prompt-engine merge --all --ide trae --output .traerules
# 或
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules

# 2. 复制到你的项目根目录
cp .cursorrules /path/to/your-project/
```

**完成！** 现在你的项目已经可以使用规则了。

> 📖 **详细步骤**：查看 [使用手册 - 方式1](./docs/guides/USAGE_MANUAL.md#二方式1单文件完整版)

---

### 方式2：单文件精简版 + 技能系统（推荐）⭐

**适用场景**：大项目，需要 Token 优化

**快速开始**：

```bash
# 1. 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 2. 复制到你的项目
cp .cursorrules /path/to/your-project/

# 3. 安装技能（批量安装，推荐）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 4. 同步技能到 AGENTS.md
cd /path/to/your-project
openskills sync -y
```

**优势**：
- ✅ Token 占用减少约 60%（从 8597 行减少到 3427 行）
- ✅ 按需加载，灵活配置
- ✅ 推荐用于所有项目，特别是大项目

> 📖 **详细步骤**：查看 [使用手册 - 方式2](./docs/guides/USAGE_MANUAL.md#三方式2单文件精简版--技能系统)  
> 📖 **技能系统说明**：查看 [V1 版本技能系统完整指南](./docs/milestones/V1_SKILL/V1_SKILL_SYSTEM_GUIDE.md) ⭐ **推荐**

---

### 方式3：多文件目录（精细控制）

**适用场景**：大型/复杂项目，需要路径特定配置

**支持情况**：
- ✅ **Cursor**：支持 `.cursor/rules/` 目录（Markdown 格式）
- ✅ **TRAE**：支持 `.trae/ai-rules.yml`（YAML 格式）
- ⚠️ **Antigravity**：多文件规则未确认（目前只支持单文件）

**快速开始**：

```bash
# 第一步：生成 multi-files 模式的产物（必须先执行）
cd /path/to/prompt-engin
bash scripts/utils/generate_dist.sh --platform cursor --mode multi-files

# 第二步：同步到项目
bash scripts/utils/sync_to_project.sh --platform cursor --mode multi-files /path/to/your-project

# TRAE：同步到 .trae/ 目录（需要先生成产物）
bash scripts/utils/generate_dist.sh --platform trae --mode multi-files
bash scripts/utils/sync_to_project.sh --platform trae --mode multi-files /path/to/your-project
```

**重要提示**：
- ⚠️ **必须先生成产物**：使用 multi-files 模式前，必须先运行 `generate_dist.sh` 生成产物
- ✅ **预览模式**：可以使用 `--dry-run` 参数预览同步操作，不实际执行
- 📖 **详细说明**：查看 [V2 版本改进计划](./docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) 了解完整使用指南

> 📖 **详细说明**：查看 [使用手册 - 方式3](./docs/guides/USAGE_MANUAL.md#四方式3多文件目录) 和 [V2 版本改进计划](./docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) ⭐ **推荐**

---

### 快速使用提示词（Cursor IDE）

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

---

## 📁 项目结构

```
prompt-engin/
├── src/prompt_engine/    # 核心代码模块
├── prompts/              # 提示词模板目录
│   ├── stages/           # 按阶段组织的提示词
│   └── types/            # 按项目类型组织的提示词
├── scripts/              # 工具脚本
│   ├── core/             # 核心脚本
│   └── utils/            # 工具脚本
├── docs/                 # 文档目录
│   ├── guides/           # 使用指南
│   ├── api/              # API 文档
│   └── examples/         # 示例文档
├── examples/             # 示例项目
└── tests/                # 测试目录
```

> 📖 **详细说明**：查看 [项目结构文档](./docs/PROJECT_STRUCTURE.md)（待创建）

---

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

> 📖 **详细说明**：查看 [开发指南](./docs/guides/DEVELOPMENT.md)（待创建）

---

## 📝 贡献

欢迎贡献！请查看 [CONTRIBUTING.md](./CONTRIBUTING.md) 了解贡献指南。

---

## 📄 许可证

本项目采用 [MIT 许可证](./LICENSE)。

---

## 🤖 AI 生成说明

本工程完全由 AI 全自动生成，包括：
- ✅ 项目结构和目录组织
- ✅ 所有源代码和实现
- ✅ 文档和使用指南
- ✅ 所有提示词模板和示例
- ✅ 测试用例和 CI/CD 配置

这展示了 AI 在软件工程领域的强大能力，从项目初始化到完整实现，全部由 AI 自动完成。

---

## 📚 相关资源

### 核心文档

- [V2 版本改进计划](./docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) - 三个平台 + 三种组织方式的完整指南 ⭐ **推荐**
- [快速参考](./docs/guides/QUICK_REFERENCE.md) - 常用命令速查
- [使用手册](./docs/guides/USAGE_MANUAL.md) - 完整使用指南

### 技能系统文档

- [V1 版本技能系统完整指南](./docs/milestones/V1_SKILL/V1_SKILL_SYSTEM_GUIDE.md) - 技能系统完整指南（整合文档）⭐ **推荐**

### 其他文档

- [快速开始指南](./QUICK_START.md) - 快速开始使用
- [API 文档](./docs/api/README.md)
- [示例项目](./examples/README.md)
- [AI 生成说明](./AI_GENERATED.md) - 了解本项目的 AI 生成过程

---

**最后更新**：2025-12-23
