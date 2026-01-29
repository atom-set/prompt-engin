# 快速开始指南

> 5 分钟快速上手 CJT Skill Engine v2.0

## 📋 目录

- [什么是 Skills？](#什么是-skills)
- [安装](#安装)
- [基本使用](#基本使用)
- [常见场景](#常见场景)
- [CLI 工具](#cli-工具)
- [下一步](#下一步)

---

## 什么是 Skills？

**Skills** 是模块化的 AI 提示词规则，采用标准化格式组织。

### Skills 的特点

- 📝 **标准化格式** - YAML frontmatter + Markdown 内容
- 🎯 **按需加载** - 只在需要时调用特定的 skill
- 🔄 **领域驱动** - 按功能领域组织（code, documentation, workflow, interaction, project）
- 📦 **模块化** - 可以灵活组合多个 skills
- 🚀 **易于扩展** - 支持自定义 skills

### Skills 组织方式

```
skills/
├── code/           # 代码开发领域 (3 个)
├── documentation/  # 文档领域 (5 个)
├── workflow/       # 工作流程领域 (5 个)
├── interaction/    # 交互领域 (2 个)
└── project/        # 项目管理领域 (1 个)
```

**总计**: 16 个 skills，覆盖 5 大领域

---

## 安装

### 1. 克隆仓库

```bash
git clone https://github.com/your-org/cjt-skill-engine.git
cd cjt-skill-engine
```

### 2. 安装依赖

```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装 skill-engine CLI 工具
pip install -e .
```

### 3. 验证安装

```bash
# 使用 Python 模块方式运行
python3 -m skill_engine.cli list

# 应该看到类似输出：
# ============================================================
# 可用的 Skills
# ============================================================
# 
# 📁 code/
#   - code/debugging
#   - code/design-principles
#   - code/organization
# ...
```

---

## 基本使用

### 方式一：在 Cursor IDE 中使用（推荐）

在 AI 对话中使用 `openskills` 命令：

```bash
# 基本语法
Bash("openskills read <skill-name>")

# 示例：调用设计原则 skill
Bash("openskills read design-principles")

# 示例：调用代码组织规范 skill
Bash("openskills read organization")
```

**说明**：
- `openskills` 是 Cursor IDE 提供的命令
- 会加载指定 skill 的内容到 AI 上下文中
- AI 将根据 skill 的规则进行响应

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
```

---

## 常见场景

### 场景 1：代码开发

#### 需求：遵循设计原则，避免过度设计

```bash
# 调用设计原则 skill
Bash("openskills read design-principles")
```

**效果**：
- AI 会优先考虑简单设计
- 避免为"未来可能的需求"增加复杂度
- 基于明确场景进行设计

#### 需求：代码文件过大，需要拆分

```bash
# 调用代码组织规范 skill
Bash("openskills read organization")
```

**效果**：
- AI 会根据文件大小限制建议拆分
- 提供合理的拆分原则
- 保持代码结构清晰

#### 需求：定位和调试问题

```bash
# 调用问题定位规范 skill
Bash("openskills read debugging")
```

**效果**：
- AI 会遵循系统化的调试流程
- 提供调试代码示例
- 帮助快速定位问题

### 场景 2：文档生成

#### 需求：创建技术文档

```bash
# 调用文档格式规范 skill
Bash("openskills read format")
```

**效果**：
- AI 会按照标准格式生成文档
- 包含任务清单、测试用例等规范格式
- 确保文档结构清晰

#### 需求：创建架构图文档

```bash
# 调用架构图模板规范 skill
Bash("openskills read architecture-diagram")
```

**效果**：
- AI 会使用模块化的架构图模板
- 支持可折叠的说明
- 便于导航和维护

#### 需求：输出 WIKI 格式文档

```bash
# 调用 WIKI 输出规范 skill
Bash("openskills read wiki-output")
```

**效果**：
- AI 会按照 WIKI 格式输出
- 自动转换 Mermaid 图表
- 符合 WIKI 平台要求

### 场景 3：大型项目管理

#### 需求：大型项目分阶段实施

```bash
# 调用分阶段实施规则 skill
Bash("openskills read phase-implementation")
```

**效果**：
- AI 会将大型工程分解为多个阶段
- 每个阶段完成后确认和测试
- 降低项目风险

#### 需求：技术方案调整，需要确认兼容性

```bash
# 调用兼容性检查机制 skill
Bash("openskills read compatibility-check")
```

**效果**：
- AI 会明确询问是否需要向下兼容
- 提供兼容性方案建议
- 避免破坏性变更

### 场景 4：用户交互

#### 需求：需求不明确，有多种实现方案

```bash
# 调用开放性问题确认规范 skill
Bash("openskills read open-question-confirmation")
```

**效果**：
- AI 会主动询问用户意图
- 列出可能的方案供选择
- 确保理解一致

---

## CLI 工具

### 常用命令

```bash
# 列表和查看
python3 -m skill_engine.cli list                    # 列出所有 skills
python3 -m skill_engine.cli read <skill-name>       # 读取 skill 内容
python3 -m skill_engine.cli stats                   # 显示统计信息
python3 -m skill_engine.cli info                    # 显示项目信息

# 搜索
python3 -m skill_engine.cli search <keyword>        # 按关键词搜索
python3 -m skill_engine.cli search --tag <tag>      # 按标签搜索

# 管理
python3 -m skill_engine.cli create <name>           # 创建新 skill
python3 -m skill_engine.cli validate <skill-name>   # 验证 skill 格式
```

### 输出示例

#### 列出所有 skills

```bash
$ python3 -m skill_engine.cli list

============================================================
可用的 Skills
============================================================

📁 code/
  - code/debugging
  - code/design-principles
  - code/organization

📁 documentation/
  - documentation/architecture-diagram
  - documentation/format
  - documentation/generation
  - documentation/time-format
  - documentation/wiki-output

📁 interaction/
  - interaction/open-question-confirmation
  - interaction/time-check

📁 project/
  - project/clean-principle

📁 workflow/
  - workflow/compatibility-check
  - workflow/exception-handling
  - workflow/file-reading
  - workflow/modular-output
  - workflow/phase-implementation
```

#### 显示统计信息

```bash
$ python3 -m skill_engine.cli stats

============================================================
Skills 统计信息
============================================================

总计: 16 个 skills
总行数: 5,152 行
平均行数: 322 行/skill

按分类统计:
  - code: 3 个
  - documentation: 5 个
  - interaction: 2 个
  - project: 1 个
  - workflow: 5 个

按标签统计:
  - code: 3 个
  - documentation: 5 个
  - workflow: 5 个
  - ...
```

#### 读取特定 skill

```bash
$ python3 -m skill_engine.cli read design-principles

============================================================
Skill: design-principles
============================================================

---
name: design-principles
description: 设计原则规范，强调简单设计优先，避免过度设计
tags: [code, design, principles]
---

# 设计原则规范

## 使用场景

当用户需要:
- 设计技术方案时
- 进行架构设计时
- 实现新功能时
...
```

---

## 下一步

### 1. 探索 Skills 库

```bash
# 查看所有可用的 skills
python3 -m skill_engine.cli list

# 查看 skills 详细信息
cat skills/README.md

# 查看特定领域的 skills
cat skills/code/README.md
cat skills/documentation/README.md
```

### 2. 创建自定义 Skills

```bash
# 使用模板创建新 skill
python3 -m skill_engine.cli create my-skill

# 或手动复制模板
cp skills/SKILL_TEMPLATE.md skills/code/my-skill.md

# 编辑 skill 文件
vim skills/code/my-skill.md

# 验证格式
python3 -m skill_engine.cli validate my-skill
```

### 3. 深入学习

- **[README.md](README.md)** - 项目完整文档
- **[skills/README.md](skills/README.md)** - Skills 库详细说明
- **[skills/SKILL_TEMPLATE.md](skills/SKILL_TEMPLATE.md)** - Skill 创建模板
- **[CHANGELOG.md](CHANGELOG.md)** - 版本变更历史

### 4. 参与贡献

- Fork 本仓库
- 创建新的 skill 或改进现有 skill
- 提交 Pull Request

---

## 常见问题

### Q1: 如何知道有哪些 skills 可用？

```bash
# 方法 1：使用 CLI 工具
python3 -m skill_engine.cli list

# 方法 2：查看 skills 目录
ls skills/*/

# 方法 3：查看文档
cat skills/README.md
```

### Q2: 如何搜索特定功能的 skill？

```bash
# 按关键词搜索
python3 -m skill_engine.cli search "代码"
python3 -m skill_engine.cli search "文档"

# 按标签搜索
python3 -m skill_engine.cli search --tag code
python3 -m skill_engine.cli search --tag documentation
```

### Q3: 如何验证 skill 格式是否正确？

```bash
# 验证单个 skill
python3 -m skill_engine.cli validate design-principles

# 运行测试（验证所有 skills）
pytest tests/test_cli.py::test_all_skills_have_valid_frontmatter
```

### Q4: 如何在项目中使用 skills？

在 Cursor IDE 的 AI 对话中：

```bash
# 调用单个 skill
Bash("openskills read design-principles")

# 调用多个 skills（根据需要）
Bash("openskills read design-principles")
Bash("openskills read organization")
```

### Q5: Skills 和 Prompts 有什么区别？

| 特性 | Skills (v2.0) | Prompts (v1.x, 已废弃) |
|------|--------------|----------------------|
| 组织方式 | 模块化，按领域分类 | 单一大文件 |
| 加载方式 | 按需加载 | 全量加载 |
| 更新方式 | 动态更新 | 需要重新生成 |
| 可扩展性 | 易于扩展 | 较难扩展 |
| 格式 | 标准化（YAML + Markdown） | 自由格式 |

---

## 技巧和最佳实践

### 1. 组合使用多个 Skills

根据实际需求，可以组合使用多个 skills：

```bash
# 代码开发场景：设计 + 组织 + 调试
Bash("openskills read design-principles")
Bash("openskills read organization")
Bash("openskills read debugging")

# 文档生成场景：格式 + 架构图 + WIKI
Bash("openskills read format")
Bash("openskills read architecture-diagram")
Bash("openskills read wiki-output")
```

### 2. 使用搜索快速找到 Skill

```bash
# 不确定 skill 名称时，先搜索
python3 -m skill_engine.cli search "设计"
python3 -m skill_engine.cli search "文档"

# 然后调用找到的 skill
Bash("openskills read design-principles")
```

### 3. 定期查看统计信息

```bash
# 了解 skills 库的整体情况
python3 -m skill_engine.cli stats

# 查看项目信息
python3 -m skill_engine.cli info
```

---

## 获取帮助

- **查看文档**: [README.md](README.md)
- **提交问题**: [GitHub Issues](https://github.com/your-org/cjt-skill-engine/issues)
- **参与讨论**: [GitHub Discussions](https://github.com/your-org/cjt-skill-engine/discussions)

---

**祝你使用愉快！** 🎉
