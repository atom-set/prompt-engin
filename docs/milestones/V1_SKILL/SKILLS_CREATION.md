# 技能创建指南

> **创建时间**: 2025-12-20（本地时间）  
> **适用对象**: 所有使用 Prompt Engine 的开发者

## 📋 目录导航

- [一、技能目录位置](#一技能目录位置)
- [二、创建技能的方法](#二创建技能的方法)
- [三、从规则文件创建技能](#三从规则文件创建技能)
- [四、验证技能](#四验证技能)
- [五、在项目中使用技能](#五在项目中使用技能)

---

## 一、技能目录位置

### 1.1 prompt-engin 项目中的技能目录

**技能目录位置**：`.claude/skills/`

**完整路径**：`/path/to/prompt-engin/.claude/skills/`

**目录结构**：

```
.claude/skills/
├── README.md                    # 技能目录说明
├── document-format/            # 文档格式技能
│   └── SKILL.md
├── time-format/                # 时间格式技能
│   └── SKILL.md
└── [其他技能]/
    └── SKILL.md
```

### 1.2 具体项目中的技能目录

**技能目录位置**：`.claude/skills/` 或 `.agent/skills/`

**完整路径**：`/path/to/your-project/.claude/skills/`

**注意**：
- 技能目录会在安装技能时自动创建
- 不需要手动创建 `.claude/skills/` 目录

---

## 二、创建技能的方法

### 方法1：批量生成所有技能（最推荐）⭐

**工具位置**：`scripts/utils/generate_all_skills.sh`

**功能**：一键批量生成所有 16 个技能，自动从规则文件转换。

**使用示例**：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成所有技能（跳过已存在的，默认行为）
bash scripts/utils/generate_all_skills.sh

# 覆盖所有已存在的技能（强制重新生成）
bash scripts/utils/generate_all_skills.sh --overwrite

# 静默模式（只显示错误和统计）
bash scripts/utils/generate_all_skills.sh --quiet

# 查看帮助信息
bash scripts/utils/generate_all_skills.sh --help
```

**优势**：
- ✅ 一键生成所有 16 个技能，无需逐个创建
- ✅ 自动处理技能映射关系，无需手动指定
- ✅ 支持覆盖模式和跳过模式，灵活配置
- ✅ 提供详细的进度显示和统计信息
- ✅ 包含错误处理和验证机制

**适用场景**：
- 首次创建所有技能
- 规则文件更新后重新生成技能
- 技能文件丢失后恢复

### 方法2：使用规则转技能工具（单个技能）

**工具位置**：`scripts/utils/convert_rule_to_skill.py`

**使用示例**：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 从规则文件创建单个技能
python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/document/document-format.md \
  --skill-name document-format \
  --description "文档格式规范，包括任务清单、测试用例、文章报告等格式要求"
```

**参数说明**：
- `--rule-file`：规则文件路径（相对于项目根目录）
- `--skill-name`：技能名称（小写字母、数字、连字符）
- `--description`：技能描述（可选，如果不提供会自动提取）

**适用场景**：
- 创建新技能（不在批量列表中的）
- 测试单个技能的生成
- 修改单个技能后重新生成

### 方法3：使用 Shell 脚本（参考项目）

**工具位置**：`scripts/utils/create_skill.sh`（如果存在）

**使用示例**：

```bash
# 从规则文件创建技能
bash scripts/utils/create_skill.sh \
  --skill-name document-format \
  --rule-file prompts/stages/common/document/document-format.md \
  --description "文档格式规范"
```

### 方法3：手动创建技能

**步骤1：创建技能目录**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 创建技能目录
mkdir -p .claude/skills/document-format
```

**步骤2：创建 SKILL.md 文件**

```bash
# 创建 SKILL.md 文件
cat > .claude/skills/document-format/SKILL.md << 'EOF'
---
name: document-format
description: 文档格式规范，包括任务清单、测试用例、文章报告等格式要求
tags: [rules, prompt-engine, documentation, format]
---

# 文档格式规范

## 使用场景

当用户需要：
- **创建任务清单**时，自动应用此规范
- **编写测试用例**时，自动应用此规范
- **生成报告文档**时，自动应用此规范

## 触发条件

以下情况自动应用此规范：
- 用户要求创建任务清单、测试用例、报告文档
- 用户要求生成文档或输出文档内容

---

[规则文件内容]
EOF
```

---

## 三、从规则文件创建技能

### 3.1 可转换的规则文件

根据方案文档，以下规则文件可以转换为技能：

**第一批（P0-P1，优先转换）**：
1. `document/document-format.md` → `document-format`
2. `document/time-format.md` → `time-format`
3. `code/organization/code-organization.md` → `code-organization`
4. `code/problem-location/problem-location.md` → `problem-location`
5. `code/design-principles/design-principles.md` → `design-principles`
6. `documentation/wiki-output.md` → `wiki-output`
7. `documentation/document-generation.md` → `document-generation`

**第二批（P2，后续转换）**：
- `project/project-clean-principle.md` → `project-clean-principle`
- `documentation/architecture-diagram-template.md` → `architecture-diagram-template`
- `interaction/open-question-confirmation.md` → `open-question-confirmation`
- `mode/plan/modular-output.md` → `modular-output`
- `mode/plan/exception-handling.md` → `exception-handling`
- `mode/plan/compatibility-check.md` → `compatibility-check`
- `mode/plan/file-reading.md` → `file-reading`
- `mode/act/phase-implementation.md` → `phase-implementation`
- `mode/act/time-check.md` → `time-check`

### 3.2 批量创建技能

**推荐方式：使用批量生成脚本** ⭐

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 一键生成所有 16 个技能
bash scripts/utils/generate_all_skills.sh
```

**传统方式：逐个创建**（不推荐，仅作参考）

如果需要逐个创建技能，可以使用以下命令：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 创建第一批技能
python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/document/document-format.md \
  --skill-name document-format

python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/document/time-format.md \
  --skill-name time-format

# ... 其他技能类似
```

**注意**：推荐使用批量生成脚本，更高效、更不容易出错。

---

## 四、验证技能

### 4.1 检查技能目录

```bash
# 检查技能目录是否存在
ls -la .claude/skills/

# 检查特定技能
ls -la .claude/skills/document-format/
cat .claude/skills/document-format/SKILL.md | head -20
```

### 4.2 使用 OpenSkills 验证

```bash
# 在 prompt-engin 项目中验证技能
cd /path/to/prompt-engin

# 安装技能（从本地目录）
openskills install .claude/skills/document-format

# 查看技能内容
openskills read document-format

# 同步到 AGENTS.md
openskills sync -y
```

---

## 五、在项目中使用技能

### 5.1 从 prompt-engin 项目安装技能

**在具体项目中使用**：

```bash
# 进入具体项目目录
cd /path/to/your-project

# 安装 prompt-engin 自定义技能（从本地目录）
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format

# 同步到 AGENTS.md
openskills sync -y
```

### 5.2 验证安装

```bash
# 检查技能目录
ls -la .claude/skills/

# 列出已安装的技能
openskills list

# 查看特定技能
openskills read document-format
```

---

## 相关文档

- [技能使用指南](./skills-usage-guide.md) - 技能系统使用指南
- [Token 优化指南](./token-optimization-guide.md) - Token 优化详细说明
- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法

---

**最后更新**: 2025-12-31（本地时间）
