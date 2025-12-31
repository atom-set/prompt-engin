# Prompt Engine 技能目录

> **创建时间**: 2025-12-20（本地时间）  
> **说明**: 本目录包含 Prompt Engine 项目的自定义技能

## 📋 目录说明

本目录包含由 Prompt Engine 项目提供的自定义技能，这些技能是从可选规则转换而来，用于按需加载。

## 🎯 可用技能

### 已创建的技能

**第一批（P0-P1）**：

| 技能名称 | 描述 | 规则文件来源 |
|---------|------|------------|
| `document-format` | 文档格式规范 | `prompts/stages/common/document/document-format.md` |
| `time-format` | 时间格式规范 | `prompts/stages/common/document/time-format.md` |
| `code-organization` | 代码组织规范 | `prompts/stages/common/code/organization/code-organization.md` |
| `problem-location` | 问题定位规范 | `prompts/stages/common/code/problem-location/problem-location.md` |
| `design-principles` | 设计原则规范 | `prompts/stages/common/code/design-principles/design-principles.md` |
| `wiki-output` | WIKI 文档输出规范 | `prompts/stages/documentation/wiki-output.md` |
| `document-generation` | 文档生成规范 | `prompts/stages/documentation/document-generation.md` |

**第二批（P2）**：

| 技能名称 | 描述 | 规则文件来源 |
|---------|------|------------|
| `project-clean-principle` | 项目清洁原则 | `prompts/stages/common/project/project-clean-principle.md` |
| `architecture-diagram-template` | 架构图模板规范 | `prompts/stages/documentation/architecture-diagram-template.md` |
| `open-question-confirmation` | 开放性问题确认规范 | `prompts/stages/common/interaction/open-question-confirmation.md` |
| `modular-output` | 模块化输出策略 | `prompts/stages/common/mode/plan/modular-output.md` |
| `exception-handling` | 例外情况处理 | `prompts/stages/common/mode/plan/exception-handling.md` |
| `compatibility-check` | 兼容性确认机制 | `prompts/stages/common/mode/plan/compatibility-check.md` |
| `file-reading` | 大文件读取策略 | `prompts/stages/common/mode/plan/file-reading.md` |
| `phase-implementation` | 分阶段实施规则 | `prompts/stages/common/mode/act/phase-implementation.md` |
| `time-check` | 时间字段检查机制 | `prompts/stages/common/mode/act/time-check.md` |

**总计**：16 个技能已创建

## 🛠️ 创建新技能

### 方式1：批量生成所有技能（最推荐）⭐

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 一键生成所有 16 个技能
bash scripts/utils/generate_all_skills.sh

# 覆盖所有已存在的技能（强制重新生成）
bash scripts/utils/generate_all_skills.sh --overwrite

# 查看帮助信息
bash scripts/utils/generate_all_skills.sh --help
```

**优势**：
- ✅ 一键生成所有技能，无需逐个创建
- ✅ 自动处理技能映射关系
- ✅ 支持覆盖和跳过模式

### 方式2：使用转换工具（单个技能）

```bash
# 从规则文件创建单个技能
python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/document/document-format.md \
  --skill-name document-format \
  --description "文档格式规范"
```

### 方式3：手动创建

1. 创建技能目录：
   ```bash
   mkdir -p .claude/skills/skill-name
   ```

2. 创建 `SKILL.md` 文件：
   ```markdown
   ---
   name: skill-name
   description: 技能描述
   tags: [rules, prompt-engine]
   ---
   
   # 技能标题
   
   ## 使用场景
   
   当用户需要：
   - **应用此规范**时，自动加载此技能
   
   ## 触发条件
   
   以下情况自动应用此规范：
   - 用户要求应用相关规范时
   - AI 助手识别到需要使用此规范时
   
   ---
   
   [规则文件内容]
   ```

## 📖 使用技能

### 在具体项目中安装技能

```bash
# 进入具体项目目录
cd /path/to/your-project

# 安装 prompt-engin 自定义技能
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format

# 同步到 AGENTS.md
openskills sync -y
```

### 查看已安装的技能

```bash
# 列出已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format
```

## 📚 相关文档

- [技能使用指南](../docs/guides/skills-usage-guide.md) - 完整的使用指南
- [Token 优化指南](../docs/guides/token-optimization-guide.md) - Token 优化说明
- [Skill 能力同步方案](../docs/guides/skill-capability-sync-plan-2025-12-20.md) - 完整的实施方案

---

**最后更新**: 2025-12-31（本地时间）
