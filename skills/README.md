# Skills 库

> CJT Skill Engine v2.0 - 领域驱动的 Skills 系统

## 📖 简介

本目录包含项目的所有 Skills 定义。Skills 是 CJT Skill Engine v2.0 的核心，采用领域驱动的组织方式。

## 🎯 Skills 系统说明

### 什么是 Skills？

Skills 是模块化的 AI 提示词规则，每个 skill 包含：

- **YAML Frontmatter** - 元数据（name, description, priority, tags）
- **使用场景** - 说明何时使用这个 skill
- **触发条件** - 说明何时自动应用这个 skill
- **与其他规则的配合** - 说明如何与其他 skills 协同工作
- **规则内容** - 完整的规则说明、示例和最佳实践

### 优先级机制

每个 skill 都有一个 **priority** 字段（1-4），用于标识其应用优先级，让 AI 能够快速识别和按优先级应用：

- **Priority 1** - 核心规则（最高优先级）：必须首先应用的基础规则
  - `tool-permission-system` - 工具调用前必须检查
  - `mode-common` - 响应生成时自动应用
  - `security-permissions` - 工具调用前安全检查

- **Priority 2** - 模式规则：根据当前模式条件应用
  - `plan-mode` - Plan 模式下应用
  - `act-mode` - Act 模式下应用
  - `solution-output` - 代码修改前应用
  - `file-write` - 文件写入前应用

- **Priority 3** - 代码标准：编写代码时自动应用
  - `code-format`, `naming`, `function-design`, `comments`
  - `error-handling-*`, `return-values`

- **Priority 4** - 领域技能：按需加载的领域特定技能
  - 代码开发：`design-principles`, `code-organization`, `problem-location`
  - 文档生成：`document-format`, `document-generation`, `wiki-output`, `architecture-diagram`, `time-format`
  - 工作流程：`phase-implementation`, `compatibility-check`, `exception-handling`, `file-reading`, `modular-output`
  - 交互：`open-question-confirmation`, `time-check`
  - 项目管理：`project-clean-principle`

**优先级识别方式**：
- AI 解析 skill 的 YAML frontmatter 时，可以直接读取 `priority` 字段
- 如果没有 `priority` 字段，系统会根据分类和标签自动推断优先级
- 优先级信息也会在分析报告中显示，便于验证和优化

### Skill 目录结构（官方规范）

**符合 Agent Skills 开放标准**：
- ✅ 每个 skill 是一个目录
- ✅ 目录内必须包含 `SKILL.md` 文件（固定文件名）
- ✅ 支持可选目录：`scripts/`, `references/`, `assets/`
- ✅ 兼容 Cursor IDE、Claude Desktop 等平台

**结构示例**：
```
skills/
├── core/
│   ├── act-mode/              # skill 目录
│   │   └── SKILL.md           # 固定文件名（必需）
│   │   ├── scripts/           # 可选：脚本文件
│   │   ├── references/        # 可选：参考文档
│   │   └── assets/            # 可选：资源文件
│   └── code-format/
│       └── SKILL.md
└── code/
    └── design-principles/
        └── SKILL.md
```

### Skill 标准格式

每个 `SKILL.md` 文件遵循以下标准格式：

```markdown
---
name: skill-name
description: Skill 的简短描述
priority: 4
tags: [category, subcategory]
---

# Skill 标题

## 使用场景

当用户需要：
- 场景描述...

## 触发条件

以下情况自动应用此规范：
- 触发条件...

## 与其他规则的配合

- 与其他 skills 的配合说明...

---

## 规则正文内容
...
```

参考 [SKILL_TEMPLATE.md](SKILL_TEMPLATE.md) 了解完整的模板格式。

## 📚 可用的 Skills

### 领域驱动的组织方式

本项目采用**领域驱动**的 skills 组织方式，共 **31 个 skills**，分为 **6 个功能领域**：

```
skills/
├── core/           # 核心规则领域 (15 个) ⭐ 顶层规则
├── code/           # 代码开发领域 (3 个)
├── documentation/  # 文档领域 (5 个)
├── workflow/       # 工作流程领域 (5 个)
├── interaction/    # 交互领域 (2 个)
└── project/        # 项目管理领域 (1 个)
```

> **注意**：`core/` 目录包含最核心的规则，这些规则应该优先应用。

### 0. 核心规则领域 (`core/`) - 15 个 skills ⭐

> **重要**：这些是顶层核心规则，应该优先应用。位于 `skills/core/` 目录。

| Skill | 描述 | 标签 |
|-------|------|------|
| **tool-permission-system** | 工具权限系统，定义工具分类体系和统一检查流程 | `core`, `mode`, `permission`, `security` |
| **mode-common** | 模式通用规则，包括模式切换、响应格式等 | `core`, `mode`, `common` |
| **security-permissions** | 安全规则和权限规则，系统化整理权限矩阵 | `core`, `mode`, `security`, `permission` |
| **plan-mode** | Plan 模式行为规范，定义 Plan 模式下的允许和禁止操作 | `core`, `mode`, `plan` |
| **act-mode** | Act 模式行为规范，定义 Act 模式下的执行规范 | `core`, `mode`, `act` |
| **solution-output** | 方案输出机制，定义方案输出的内容和格式 | `core`, `mode`, `plan`, `solution` |
| **file-write** | 文件写入规则，包括文件大小检查和写入策略 | `core`, `mode`, `act`, `file` |
| **code-format** | 代码格式规范，包括缩进、行长度、空行等 | `core`, `code`, `format` |
| **naming** | 命名规范，包括变量、函数、类、常量等命名规则 | `core`, `code`, `naming` |
| **function-design** | 函数设计规范，包括函数命名、参数处理、代码嵌套等 | `core`, `code`, `function`, `design` |
| **comments** | 注释规范，包括单行注释、多行注释、文档注释等 | `core`, `code`, `comments` |
| **error-handling-strategy** | 错误处理策略，包括异常捕获、错误处理模式等 | `core`, `code`, `error-handling`, `strategy` |
| **error-logging** | 错误日志记录，包括日志级别、日志内容、结构化日志等 | `core`, `code`, `error-handling`, `logging` |
| **error-message-format** | 错误信息格式，包括用户可见错误、错误码规范等 | `core`, `code`, `error-handling`, `message` |
| **return-values** | 返回值规范，包括返回值模式、错误处理等 | `core`, `code`, `error-handling`, `return` |

**详见**：[core/README.md](core/README.md)

### 1. 代码开发领域 (`code/`) - 3 个 skills

| Skill | 描述 | 标签 |
|-------|------|------|
| **organization** | 代码组织规范，包括文件大小限制、拆分原则等 | `code`, `organization`, `refactoring` |
| **design-principles** | 设计原则规范，强调简单设计优先，避免过度设计 | `code`, `design`, `principles` |
| **debugging** | 问题定位与调试规范，包括调试流程、调试代码规范等 | `code`, `debug`, `troubleshooting` |

**详见**：[code/README.md](code/README.md)

### 2. 文档领域 (`documentation/`) - 5 个 skills

| Skill | 描述 | 标签 |
|-------|------|------|
| **format** | 文档格式规范，包括任务清单、测试用例、文章报告等格式要求 | `documentation`, `format`, `standards` |
| **generation** | 文档生成规范，整合技术方案、架构图、WIKI 等文档类型的规范 | `documentation`, `generation`, `automation` |
| **architecture-diagram** | 架构图文档模板规范，包括图表模块化、说明可折叠、便于导航等 | `architecture`, `diagram`, `template` |
| **wiki-output** | WIKI 文档输出规范，包括文档结构、格式要求、Mermaid 图表转换等 | `wiki`, `output`, `mermaid` |
| **time-format** | 时间格式规范，强制要求所有时间字段都必须通过工具动态获取 | `time`, `format`, `standards` |

**详见**：[documentation/README.md](documentation/README.md)

### 3. 工作流程领域 (`workflow/`) - 5 个 skills

| Skill | 描述 | 标签 |
|-------|------|------|
| **phase-implementation** | 大型工程分阶段实施规则，每个阶段完成后确认和测试再继续 | `workflow`, `phase`, `implementation` |
| **compatibility-check** | 兼容性确认机制，涉及技术方案调整时必须明确询问用户 | `compatibility`, `migration`, `breaking-changes` |
| **exception-handling** | 例外情况处理流程，包括明显的语法错误、已知的简单问题等 | `exception`, `error-handling`, `edge-cases` |
| **file-reading** | 大文件读取策略，对于大文件的读取应采用阶段性读取策略 | `file`, `reading`, `performance`, `strategy` |
| **modular-output** | 完整方案模块化输出策略，适用于复杂内容的输出 | `modular`, `output`, `organization` |

**详见**：[workflow/README.md](workflow/README.md)

### 4. 交互领域 (`interaction/`) - 2 个 skills

| Skill | 描述 | 标签 |
|-------|------|------|
| **open-question-confirmation** | 开放性问题确认规范，针对开放性问题必须通过询问方式与用户达成一致 | `interaction`, `confirmation`, `open-question` |
| **time-check** | 时间字段强制检查机制，创建包含时间字段的文档时必须先通过工具获取当前时间 | `time`, `validation`, `automation` |

**详见**：[interaction/README.md](interaction/README.md)

### 5. 项目管理领域 (`project/`) - 1 个 skill

| Skill | 描述 | 标签 |
|-------|------|------|
| **clean-principle** | 项目清洁原则，避免将 AI 辅助开发工具和非业务相关的脚本混入项目核心代码 | `project`, `clean`, `principles` |

**详见**：[project/README.md](project/README.md)

## 🔧 如何使用 Skills

### 方式一：在 Cursor IDE 中使用（推荐）

在 AI 对话中使用 `openskills` 命令：

```bash
# 调用单个 skill
Bash("openskills read <skill-name>")

# 示例：调用设计原则 skill
Bash("openskills read design-principles")

# 示例：调用代码组织规范 skill
Bash("openskills read organization")
```

### 方式二：使用 skill-engine CLI

```bash
# 列出所有 skills（按领域分类）
python3 -m skill_engine.cli list

# 读取特定 skill
python3 -m skill_engine.cli read design-principles

# 搜索 skills
python3 -m skill_engine.cli search "代码"
python3 -m skill_engine.cli search --tag code

# 显示统计信息
python3 -m skill_engine.cli stats

# 验证 skill 格式
python3 -m skill_engine.cli validate design-principles
```

## 📝 创建自定义 Skills

### 1. 使用 CLI 工具创建（推荐）

```bash
# 创建新 skill（交互式）
python3 -m skill_engine.cli create my-skill

# CLI 会引导你：
# - 选择领域（code, documentation, workflow, interaction, project）
# - 输入描述
# - 选择标签
# - 自动创建目录结构（符合官方规范）
# - 自动生成 SKILL.md 文件（固定文件名）
```

### 2. 手动创建

```bash
# 创建 skill 目录（官方规范：每个 skill 是一个目录）
mkdir -p skills/code/my-skill

# 复制模板到 SKILL.md（固定文件名）
cp skills/SKILL_TEMPLATE.md skills/code/my-skill/SKILL.md

# 可选：创建支持目录
mkdir -p skills/code/my-skill/{scripts,references,assets}

# 编辑文件
vim skills/code/my-skill/SKILL.md

# 验证格式
python3 -m skill_engine.cli validate code/my-skill
```

### 3. Skill 目录结构要求（官方规范）

- **目录名**：使用小写字母和连字符（如 `my-skill`）
- **位置**：放在对应的领域目录下（如 `skills/code/my-skill/`）
- **必需文件**：目录内必须包含 `SKILL.md` 文件（固定文件名）
- **可选目录**：`scripts/`、`references/`、`assets/`
- **格式**：`SKILL.md` 必须包含 YAML frontmatter 和标准章节
- **内容**：清晰的使用场景、触发条件和规则说明

## 📊 统计数据

```bash
$ python3 -m skill_engine.cli stats

总计: 31 个 skills
总行数: 约 10,000+ 行
平均行数: 约 320 行/skill

按领域统计:
  - core: 15 个 ⭐ (顶层核心规则)
  - code: 3 个
  - documentation: 5 个
  - workflow: 5 个
  - interaction: 2 个
  - project: 1 个
```

## 🎯 Skills 使用场景

### 代码开发场景

```bash
# 设计技术方案
Bash("openskills read design-principles")

# 代码文件过大需要拆分
Bash("openskills read organization")

# 定位和调试问题
Bash("openskills read debugging")
```

### 文档生成场景

```bash
# 创建技术文档
Bash("openskills read format")

# 创建架构图文档
Bash("openskills read architecture-diagram")

# 输出 WIKI 格式文档
Bash("openskills read wiki-output")
```

### 项目管理场景

```bash
# 大型项目分阶段实施
Bash("openskills read phase-implementation")

# 技术方案调整，确认兼容性
Bash("openskills read compatibility-check")
```

### 用户交互场景

```bash
# 需求不明确，需要确认
Bash("openskills read open-question-confirmation")
```

## 🔗 相关资源

- **[SKILL_TEMPLATE.md](SKILL_TEMPLATE.md)** - Skill 创建模板
- **[../README.md](../README.md)** - 项目主文档
- **[../QUICK_START.md](../QUICK_START.md)** - 快速开始指南
- **[../AGENTS.md](../AGENTS.md)** - Cursor IDE Skills 配置

## 📖 各领域详细文档

- **[core/README.md](core/README.md)** - 核心规则领域 Skills ⭐ (顶层规则)
- **[code/README.md](code/README.md)** - 代码开发领域 Skills
- **[documentation/README.md](documentation/README.md)** - 文档领域 Skills
- **[workflow/README.md](workflow/README.md)** - 工作流程领域 Skills
- **[interaction/README.md](interaction/README.md)** - 交互领域 Skills
- **[project/README.md](project/README.md)** - 项目管理领域 Skills

---

**如有问题，请参考项目文档或提交 Issue。**
