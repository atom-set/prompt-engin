# 技能系统快速使用指南

> **创建时间**: 2025-12-20（本地时间）  
> **适用对象**: 所有使用 Prompt Engine 的开发者

## 🎯 推荐说明

Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：

- **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
- **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用

> **重要**：两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

**选择建议**：
- **⭐ 所有项目（推荐）** → 使用方式2（精简版规则文件 + 技能系统）
- **小项目或不需要 token 优化** → 使用方式1（完整版规则文件）

## 📋 当前状态

### ✅ 已实现功能
- ✅ 技能同步脚本（`scripts/skills_sync/sync_skill.py`）
- ✅ AGENTS.md 模板文件
- ✅ 规则转技能工具（`scripts/utils/convert_rule_to_skill.py`）
- ✅ **16 个技能已创建**（第一批 7 个 + 第二批 9 个）
- ✅ 完整的使用文档

## 🚀 快速开始

### ⭐ 方式2：精简版规则文件 + 技能系统 ✅ **重点推荐**

**✅ 已实现**：`--core-only` 选项已可用！

**使用方式**：

```bash
# 1. 生成精简版规则文件（只包含核心规则）
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 2. 复制到你的项目
cp .cursorrules /path/to/your-project/

# 3. 安装 prompt-engin 自定义技能（按需）
cd /path/to/your-project

# 安装技能（从 prompt-engin 项目的技能目录）
# ⚠️ 注意：使用绝对路径或相对路径指向 prompt-engin 项目的 .claude/skills/ 目录
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format

# 或者使用相对路径（如果在同一工作区）
# openskills install ../prompt-engin/.claude/skills/document-format

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

### 方式1：完整版规则文件 ✅ **适用于小项目**

**最简单的方式，直接使用完整版规则文件**：

```bash
# 1. 生成完整版规则文件
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 2. 复制到你的项目
cp .cursorrules /path/to/your-project/

# 完成！直接使用即可
```

**特点**：
- ✅ 简单直接，复制即用
- ✅ 所有规则始终可用
- ⚠️ Token 占用较大（8597 行，约 328KB）

**适用场景**：
- ✅ 小项目，不需要 token 优化
- ✅ 希望所有规则始终可用
- ✅ 不想安装 OpenSkills 工具

## 📍 技能目录位置

**prompt-engin 项目中的技能目录**：`.claude/skills/`

**查看技能目录**：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 查看技能目录
ls -la .claude/skills/

# 应该看到：
# document-format/
# time-format/
# README.md
```

**注意**：
- 技能目录在 prompt-engin 项目根目录下的 `.claude/skills/` 目录
- 使用绝对路径或相对路径安装技能时，需要指向这个目录

## 📋 已创建的技能

**总计**：16 个技能已创建

**第一批（P0-P1）**：7 个
- `document-format`、`time-format`、`code-organization`、`problem-location`、`design-principles`、`wiki-output`、`document-generation`

**第二批（P2）**：9 个
- `project-clean-principle`、`architecture-diagram-template`、`open-question-confirmation`、`modular-output`、`exception-handling`、`compatibility-check`、`file-reading`、`phase-implementation`、`time-check`

**查看完整列表**：[技能列表](./SKILLS_LIST.md)

## 📖 详细文档

- [技能列表](./SKILLS_LIST.md) - 所有已创建技能的完整列表
- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [技能创建指南](./SKILLS_CREATION.md) - 如何创建新技能
- [Token 优化指南](./token-optimization-guide.md) - Token 优化详细说明
- [技能使用指南](./skills-usage-guide.md) - 技能系统完整使用指南
- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法

## 🔧 环境准备（仅方式2需要）

如果未来要使用方式2（精简版 + 技能系统），需要先安装 OpenSkills：

```bash
# 安装 OpenSkills（需要 Node.js 20.6+）
npm install -g openskills

# 验证安装
openskills --version
# 应该显示：1.2.1 或更高版本
```

## ❓ 常见问题

### Q1：现在可以使用技能系统吗？

**A1**：可以！`--core-only` 选项已实现，可以使用方式2（精简版规则文件 + 技能系统）。如果不需要 Token 优化，也可以继续使用方式1（完整版规则文件）。

### Q2：两种方式有什么区别？

**A2**：
- **方式1**：简单直接，所有规则始终可用，Token 占用较大（8597 行）
- **方式2**：Token 优化，按需加载，需要 OpenSkills 工具支持（3427 行，减少约 60%）

### Q3：如何查看实现进度？

**A3**：查看 [技能使用指南](./skills-usage-guide.md) 和 [Token 优化指南](./token-optimization-guide.md) 了解详细的使用方法和优化效果。

---

**最后更新**: 2025-12-20（本地时间）
