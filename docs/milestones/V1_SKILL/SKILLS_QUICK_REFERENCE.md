# 技能系统快速参考

> **创建时间**: 2025-12-20（本地时间）  
> **适用对象**: 所有使用 Prompt Engine 的开发者

## 📍 技能目录位置

### prompt-engin 项目中的技能目录

**位置**：`.claude/skills/`

**完整路径**：`/Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/`

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

### 具体项目中的技能目录

**位置**：`.claude/skills/` 或 `.agent/skills/`

**完整路径**：`/path/to/your-project/.claude/skills/`

**注意**：技能目录会在安装技能时自动创建，不需要手动创建。

---

## 🚀 快速使用

### 方式1：批量安装所有技能（推荐）

**一次性安装所有技能，然后选择使用哪些**：

```bash
# 1. 进入你的项目目录
cd /path/to/your-project

# 2. 运行批量安装脚本（从 prompt-engin 项目运行）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 或者：在目标项目目录中运行（使用相对路径）
cd /path/to/your-project
bash ../prompt-engin/scripts/utils/install_all_skills.sh

# 3. 同步到 AGENTS.md（选择要使用的技能）
cd /path/to/your-project
openskills sync -y
```

**优势**：
- ✅ 一次性安装所有技能，无需逐个安装
- ✅ 安装后可以通过 `openskills sync -y` 选择使用哪些技能
- ✅ 简单快捷，适合首次使用

### 方式2：安装单个技能

**只安装需要的技能**：

```bash
# 1. 进入你的项目目录
cd /path/to/your-project

# 2. 安装单个技能（使用绝对路径）
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/time-format

# 3. 同步到 AGENTS.md
openskills sync -y
```

### 方式3：使用相对路径（如果在同一工作区）

```bash
# 如果 prompt-engin 和你的项目在同一工作区
cd /path/to/your-project

# 使用相对路径
openskills install ../prompt-engin/.claude/skills/document-format
openskills install ../prompt-engin/.claude/skills/time-format

# 同步到 AGENTS.md
openskills sync -y
```

---

## 📋 已创建的技能

**第一批（P0-P1）**：

| 技能名称 | 规则文件来源 | 使用场景 |
|---------|------------|---------|
| `document-format` | `document/document-format.md` | 创建文档时自动应用 |
| `time-format` | `document/time-format.md` | 处理时间字段时自动应用 |
| `code-organization` | `code/organization/code-organization.md` | 代码组织时自动应用 |
| `problem-location` | `code/problem-location/problem-location.md` | 问题定位时自动应用 |
| `design-principles` | `code/design-principles/design-principles.md` | 设计原则时自动应用 |
| `wiki-output` | `documentation/wiki-output.md` | WIKI 文档时自动应用 |
| `document-generation` | `documentation/document-generation.md` | 文档生成时自动应用 |

**第二批（P2）**：

| 技能名称 | 规则文件来源 | 使用场景 |
|---------|------------|---------|
| `project-clean-principle` | `project/project-clean-principle.md` | 项目清理时自动应用 |
| `architecture-diagram-template` | `documentation/architecture-diagram-template.md` | 架构图时自动应用 |
| `open-question-confirmation` | `interaction/open-question-confirmation.md` | 开放性问题确认时自动应用 |
| `modular-output` | `mode/plan/modular-output.md` | 模块化输出时自动应用 |
| `exception-handling` | `mode/plan/exception-handling.md` | 例外情况处理时自动应用 |
| `compatibility-check` | `mode/plan/compatibility-check.md` | 兼容性确认时自动应用 |
| `file-reading` | `mode/plan/file-reading.md` | 大文件读取时自动应用 |
| `phase-implementation` | `mode/act/phase-implementation.md` | 分阶段实施时自动应用 |
| `time-check` | `mode/act/time-check.md` | 时间字段检查时自动应用 |

**总计**：16 个技能已创建

---

## 🔧 创建新技能

### 使用转换工具

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 从规则文件创建技能
python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/code/organization/code-organization.md \
  --skill-name code-organization \
  --description "代码组织规范"
```

### 验证技能创建

```bash
# 检查技能目录
ls -la .claude/skills/code-organization/

# 查看技能内容
cat .claude/skills/code-organization/SKILL.md | head -30
```

---

## ❓ 常见问题

### Q1：`.claude/skills` 目录在哪里？

**A1**：
- **prompt-engin 项目**：`.claude/skills/` 在项目根目录下
- **具体项目**：`.claude/skills/` 在项目根目录下（安装技能后自动创建）

### Q2：如何找到 prompt-engin 的技能目录？

**A2**：使用绝对路径或相对路径：

```bash
# 绝对路径（推荐）
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format

# 相对路径（如果在同一工作区）
openskills install ../prompt-engin/.claude/skills/document-format
```

### Q3：技能目录不存在怎么办？

**A3**：
- **prompt-engin 项目**：技能目录应该已经存在（`.claude/skills/`）
- **具体项目**：安装技能时会自动创建，不需要手动创建

### Q4：如何查看 prompt-engin 项目中有哪些技能？

**A4**：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 查看技能目录
ls -la .claude/skills/

# 或查看 README
cat .claude/skills/README.md
```

### Q5：为什么不能直接安装整个技能目录？

**A5**：

`openskills install` **只能安装单个技能目录**，不能安装整个 `.claude/skills/` 目录。

**错误示例**：
```bash
# ❌ 错误：不能安装整个技能目录
openskills install /path/to/prompt-engin/.claude/skills
```

**正确做法**：

**方式1：使用批量安装脚本（推荐）**
```bash
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

**方式2：安装单个技能**
```bash
# ✅ 正确：安装单个技能目录
openskills install /path/to/prompt-engin/.claude/skills/document-format
```

**详细说明**：
- `openskills install` 只能接受单个技能目录路径，不能接受整个技能目录
- 如果提供整个目录路径，`openskills` 会误认为是 GitHub 仓库路径，导致失败
- 请参考 [故障排查指南](./TROUBLESHOOTING.md) 了解更多详情

---

## 📖 相关文档

- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法
- [故障排查指南](./TROUBLESHOOTING.md) - 常见问题和解决方法
- [技能创建指南](./SKILLS_CREATION.md) - 详细的创建指南
- [技能使用指南](./skills-usage-guide.md) - 完整的使用指南
- [快速使用指南](./QUICK_START_SKILLS.md) - 快速上手

---

**最后更新**: 2025-12-20（本地时间）
