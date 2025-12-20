# 提示词模板目录

本目录包含所有提示词模板，按阶段和类型组织。

## 🤖 AI 生成说明

**重要**：本目录下的所有提示词模板均由 AI 全自动生成，包括：
- 提示词内容和结构
- 目录组织和分类
- 示例和说明文档

这些提示词展示了 AI 在提示词工程领域的应用，可以作为实际使用的参考模板。

## 目录结构

### 按阶段组织 (`stages/`)

- `common/` - 通用阶段提示词
  - `mode/` - 模式规则（Plan、Act、Debug）
  - `code/` - 代码规范（命名、函数、格式、错误处理等）
  - `document/` - 文档规范（格式、时间格式）
  - `interaction/` - 交互规范（确认机制等）
  - `project/` - 项目规范（项目清洁原则）
- `requirements/` - 需求分析阶段
- `design/` - 设计阶段
- `development/` - 开发阶段
- `testing/` - 测试阶段
- `documentation/` - 文档阶段
  - `document-generation.md` - 文档生成规范（整合版，推荐使用）
  - `architecture-diagram-template.md` - 架构图文档模板规范
  - `wiki-output.md` - WIKI 输出规范

### 按类型组织 (`types/`)

- `frontend/` - 前端项目提示词
- `backend/` - 后端项目提示词
- `fullstack/` - 全栈项目提示词
- `mobile/` - 移动端项目提示词

### 通用模板 (`templates/`)

- `project-template.md` - 项目模板
- `rule-modularization-guide.md` - 规则模块化指南
- `stage-template.md` - 阶段模板
- `technical-solution-template.md` - 技术方案模板（包含完整模板和 AI 使用提示词）

## 使用方式

1. **直接使用**：可以直接使用这些 AI 生成的提示词模板
2. **定制修改**：根据实际需求修改和定制提示词
3. **参考学习**：作为提示词工程的参考和学习材料

## 文档生成规范

### 文档阶段规范

文档阶段（`stages/documentation/`）包含以下规范文件：

| 文件 | 说明 | 推荐度 |
|------|------|--------|
| `document-generation.md` | 文档生成规范（整合版） | ⭐⭐⭐ 推荐优先使用 |
| `architecture-diagram-template.md` | 架构图文档模板规范 | ⭐⭐ 特定文档类型 |
| `wiki-output.md` | WIKI 输出规范 | ⭐⭐ 特定文档类型 |

**`document-generation.md`（推荐使用）**：
- ✅ 整合了所有文档类型的规范（技术方案、架构图、WIKI）
- ✅ 包含通用规范（时间格式、内容格式、代码格式等）
- ✅ 提供统一的使用指南和最佳实践
- ✅ 技术方案文档引用 `templates/technical-solution-template.md` 模板

### 技术方案文档

**模板文件**：`templates/technical-solution-template.md`

**使用方式**：
1. 使用模板中的 AI 使用提示词
2. 替换项目信息占位符
3. 根据项目实际情况调整章节

**详细说明**：参见 `templates/README.md` 和 `stages/documentation/document-generation.md`

## 提示词格式

每个提示词文件遵循以下格式：

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

## 相关文档

- [项目 README](../README.md)
- [AI 生成说明](../AI_GENERATED.md)
- [快速开始指南](../../QUICK_START.md) - 快速开始使用

