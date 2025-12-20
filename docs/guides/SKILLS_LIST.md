# 技能列表

> **创建时间**: 2025-12-20（本地时间）  
> **最后更新**: 2025-12-20（本地时间）

## 📋 技能总览

**总计**：16 个技能已创建

**技能目录**：`.claude/skills/`

---

## 🎯 第一批技能（P0-P1，优先转换）

| 序号 | 技能名称 | 描述 | 规则文件来源 | 状态 |
|------|---------|------|------------|------|
| 1 | `document-format` | 文档格式规范 | `document/document-format.md` | ✅ 已创建 |
| 2 | `time-format` | 时间格式规范 | `document/time-format.md` | ✅ 已创建 |
| 3 | `code-organization` | 代码组织规范 | `code/organization/code-organization.md` | ✅ 已创建 |
| 4 | `problem-location` | 问题定位规范 | `code/problem-location/problem-location.md` | ✅ 已创建 |
| 5 | `design-principles` | 设计原则规范 | `code/design-principles/design-principles.md` | ✅ 已创建 |
| 6 | `wiki-output` | WIKI 文档输出规范 | `documentation/wiki-output.md` | ✅ 已创建 |
| 7 | `document-generation` | 文档生成规范 | `documentation/document-generation.md` | ✅ 已创建 |

---

## 🎯 第二批技能（P2，后续转换）

| 序号 | 技能名称 | 描述 | 规则文件来源 | 状态 |
|------|---------|------|------------|------|
| 8 | `project-clean-principle` | 项目清洁原则 | `project/project-clean-principle.md` | ✅ 已创建 |
| 9 | `architecture-diagram-template` | 架构图模板规范 | `documentation/architecture-diagram-template.md` | ✅ 已创建 |
| 10 | `open-question-confirmation` | 开放性问题确认规范 | `interaction/open-question-confirmation.md` | ✅ 已创建 |
| 11 | `modular-output` | 模块化输出策略 | `mode/plan/modular-output.md` | ✅ 已创建 |
| 12 | `exception-handling` | 例外情况处理 | `mode/plan/exception-handling.md` | ✅ 已创建 |
| 13 | `compatibility-check` | 兼容性确认机制 | `mode/plan/compatibility-check.md` | ✅ 已创建 |
| 14 | `file-reading` | 大文件读取策略 | `mode/plan/file-reading.md` | ✅ 已创建 |
| 15 | `phase-implementation` | 分阶段实施规则 | `mode/act/phase-implementation.md` | ✅ 已创建 |
| 16 | `time-check` | 时间字段检查机制 | `mode/act/time-check.md` | ✅ 已创建 |

---

## 📖 使用方式

### 查看所有技能

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 查看技能目录
ls -la .claude/skills/

# 查看技能列表
ls -1 .claude/skills/ | grep -v README.md
```

### 安装技能

```bash
# 在具体项目中安装技能
cd /path/to/your-project

# 安装单个技能
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 批量安装技能（示例）
for skill in document-format time-format code-organization; do
  openskills install /path/to/prompt-engin/.claude/skills/$skill
done

# 同步到 AGENTS.md
openskills sync -y
```

### 查看技能内容

```bash
# 在 prompt-engin 项目中查看技能
cd /path/to/prompt-engin

# 安装技能（从本地目录）
openskills install .claude/skills/document-format

# 查看技能内容
openskills read document-format
```

---

## 📚 相关文档

- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [技能创建指南](./SKILLS_CREATION.md) - 如何创建新技能
- [技能使用指南](./skills-usage-guide.md) - 完整的使用指南
- [Token 优化指南](./token-optimization-guide.md) - Token 优化详细说明

---

**最后更新**: 2025-12-20（本地时间）
