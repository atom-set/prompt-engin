# V1 版本技能系统完整指南

> **文件说明**：V1 版本技能系统完整指南，整合所有技能系统相关文档
> **版本核心**：精简版规则文件 + 技能系统（Token 优化，按需加载）
> **创建时间**：2025-12-24（本地时间）
> **更新时间**：2025-12-24（本地时间）

---

## 📋 目录

- [一、V1 版本概述](#一v1-版本概述)
- [二、快速开始](#二快速开始)
- [三、技能系统使用指南](#三技能系统使用指南)
- [四、Token 优化指南](#四token-优化指南)
- [五、技能列表](#五技能列表)
- [六、批量安装指南](#六批量安装指南)
- [七、技能创建指南](#七技能创建指南)
- [八、故障排查指南](#八故障排查指南)
- [九、使用示例](#九使用示例)
- [十、快速参考](#十快速参考)

---

## 一、V1 版本概述

### 版本定位

**V1 版本**是 Prompt Engine 的技能系统版本，核心特性是支持**精简版规则文件 + 技能系统**，实现 Token 优化和按需加载。

### 核心改进

1. **Token 优化**：
   - ✅ 初始上下文 Token 减少约 60%（从 8597 行减少到 3427 行）
   - ✅ 按需加载，只在需要时加载相关技能
   - ✅ 灵活配置，用户可以选择使用哪些技能

2. **两种使用方式**：
   - ✅ 方式1：完整版规则文件（简单直接，复制即用）
   - ✅ 方式2：精简版规则文件 + 技能系统（Token 优化，推荐）⭐

3. **技能系统**：
   - ✅ 16 个技能已创建（第一批 7 个 + 第二批 9 个）
   - ✅ 批量安装脚本支持
   - ✅ 规则转技能工具

### 推荐说明

Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：

- **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
- **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用

> **重要**：两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

**选择建议**：
- **⭐ 所有项目（推荐）** → 使用方式2（精简版规则文件 + 技能系统）
- **小项目或不需要 token 优化** → 使用方式1（完整版规则文件）

---

## 二、快速开始

### 2.1 前提条件

**必需环境**：
- Node.js 20.6+（OpenSkills 依赖）
- OpenSkills 已全局安装：`npm i -g openskills`

**验证安装**：

```bash
# 检查 OpenSkills 版本
openskills --version
# 应该显示：1.2.1 或更高版本
```

### 2.2 ⭐ 方式2：精简版规则文件 + 技能系统（推荐）

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

# 或者使用批量安装脚本（推荐）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 4. 同步技能到 AGENTS.md
cd /path/to/your-project
openskills sync -y
```

**特点**：
- ✅ **Token 占用减少约 60%**（从 8597 行减少到 3427 行）
- ✅ **按需加载**，灵活配置
- ✅ **推荐用于所有项目**，特别是大项目
- ⚠️ 需要 OpenSkills 工具支持

### 2.3 方式1：完整版规则文件

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

---

## 三、技能系统使用指南

### 3.1 OpenSkills 命令说明

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `openskills install <path>` | **安装技能** | 从本地目录、GitHub 仓库等安装新技能 |
| `openskills sync -y` | **同步已安装的技能** | 将已安装的技能同步到 AGENTS.md，不安装新技能 |
| `openskills list` | **列出已安装的技能** | 查看项目中已安装的所有技能 |
| `openskills read <skill-name>` | **查看技能内容** | 查看特定技能的详细内容 |
| `openskills update` | **更新技能** | 更新从 GitHub 安装的技能 |

**⚠️ 关键区别**：
- ✅ `openskills install`：可以安装 prompt-engin 自定义的技能（从本地目录）
- ✅ `openskills sync -y`：只同步已安装的技能到 AGENTS.md，**不会安装新技能**

**完整流程**：

```bash
# 1. 先安装技能（从 prompt-engin 项目的技能目录）
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 2. 然后同步到 AGENTS.md（将已安装的技能同步到 AGENTS.md）
openskills sync -y

# 注意：必须先执行步骤1（安装），再执行步骤2（同步）
# 如果只执行 sync，不会安装新技能，只会同步已安装的技能
```

### 3.2 在具体项目中使用

**步骤1：在 prompt-engin 项目中生成精简版规则文件**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 生成的文件约 3427 行（相比完整版 8597 行，减少约 60%）
```

**步骤2：复制规则文件到具体项目**

```bash
# 复制精简版规则文件到具体项目
cp .cursorrules /path/to/your-project/

# 或使用绝对路径
cp /path/to/prompt-engin/.cursorrules /path/to/your-project/
```

**步骤3：在具体项目中安装技能**

```bash
# 进入具体项目目录
cd /path/to/your-project

# ⚠️ 重要：openskills install 用于安装技能
# 方式1：从 prompt-engin 项目安装自定义技能（从本地目录）
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format
openskills install /path/to/prompt-engin/.claude/skills/code-organization
# ... 根据需要安装其他技能

# 方式2：使用批量安装脚本（推荐）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

**步骤4：同步技能到 AGENTS.md**

```bash
# 在具体项目目录中
# ⚠️ 注意：openskills sync -y 只同步已安装的技能，不会安装新技能
openskills sync -y

# 这会自动：
# 1. 扫描 .claude/skills/ 目录中已安装的技能
# 2. 创建或更新 AGENTS.md 文件
# 3. 列出所有已安装的技能到 AGENTS.md
# 4. AI 可以自动识别并使用这些技能
```

**步骤5：验证配置**

```bash
# 检查技能目录
ls -la .claude/skills/

# 检查 AGENTS.md
cat AGENTS.md | head -50

# 应该看到类似以下内容：
# <skills_system priority="1">
# <available_skills>
# <skill>
# <name>document-format</name>
# <description>文档格式规范...</description>
# </skill>
# ...
```

### 3.3 使用效果

**初始上下文**：
- 只有核心规则（~3427 行）
- Token 占用：约 124KB（相比完整版减少约 60%）

**按需加载**：
- 需要文档格式时：AI 自动加载 `document-format` 技能
- 需要时间格式时：AI 自动加载 `time-format` 技能
- 需要问题定位时：AI 自动加载 `problem-location` 技能

**使用示例**：

```
用户："帮我创建一个任务清单"
AI：自动识别需要使用文档格式规范
    → 自动加载 document-format 技能
    → 应用文档格式规范创建任务清单
```

---

## 四、Token 优化指南

### 4.1 Token 问题分析

**规则文件大小**：
- `.cursorrules` 文件：**8597 行**（约 **328KB**）
- 所有规则都在初始上下文中，占用大量 token
- 即使不使用某些规则，也会占用 token

**问题影响**：
- ⚠️ 初始上下文 token 占用大
- ⚠️ 每次对话都会加载所有规则
- ⚠️ 无法按需加载特定规则

### 4.2 Token 优化价值

通过将部分规则转换为技能（Skills），可以实现：
- ✅ 初始上下文 token 减少 **约 60%**（从 8597 行减少到 3427 行）
- ✅ 按需加载，只在需要时加载相关技能
- ✅ 灵活配置，用户可以选择使用方式

### 4.3 优化策略

**规则分类 + Skill 转换**：
1. **核心规则**：保留在 `.cursorrules` 中（必须全局生效）
2. **可选规则**：转换为技能（按需加载）

**优化效果**：

| 方案 | 初始上下文 | Token 占用 | 节省比例 |
|------|-----------|-----------|---------|
| **当前方案**（完整版） | 8597 行 | ~308KB | - |
| **优化方案**（精简版 + Skill） | ~3427 行 | ~124KB | **约 60%** |

### 4.4 规则分类标准

**核心规则**必须满足以下**所有条件**：
- ✅ 必须全局生效，不能按需加载
- ✅ 影响 AI 助手的基础行为
- ✅ 其他规则可能依赖它
- ✅ 使用频率高

**可选规则**满足以下**任一条件**即可：
- ✅ 可按需加载，不影响核心功能
- ✅ 特定场景使用
- ✅ 可以独立使用

### 4.5 效果对比

| 指标 | 完整版 | 精简版 + Skill | 节省 |
|------|--------|--------------|------|
| **初始上下文** | 8597 行 | ~3427 行 | **约 60%** |
| **Token 占用** | ~308KB | ~124KB | **约 60%** |
| **按需加载** | 不支持 | 支持 | - |

---

## 五、技能列表

### 5.1 技能总览

**总计**：16 个技能已创建

**技能目录**：`.claude/skills/`

### 5.2 第一批技能（P0-P1，优先转换）

| 序号 | 技能名称 | 描述 | 规则文件来源 | 状态 |
|------|---------|------|------------|------|
| 1 | `document-format` | 文档格式规范 | `document/document-format.md` | ✅ 已创建 |
| 2 | `time-format` | 时间格式规范 | `document/time-format.md` | ✅ 已创建 |
| 3 | `code-organization` | 代码组织规范 | `code/organization/code-organization.md` | ✅ 已创建 |
| 4 | `problem-location` | 问题定位规范 | `code/problem-location/problem-location.md` | ✅ 已创建 |
| 5 | `design-principles` | 设计原则规范 | `code/design-principles/design-principles.md` | ✅ 已创建 |
| 6 | `wiki-output` | WIKI 文档输出规范 | `documentation/wiki-output.md` | ✅ 已创建 |
| 7 | `document-generation` | 文档生成规范 | `documentation/document-generation.md` | ✅ 已创建 |

### 5.3 第二批技能（P2，后续转换）

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

### 5.4 查看所有技能

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 查看技能目录
ls -la .claude/skills/

# 查看技能列表
ls -1 .claude/skills/ | grep -v README.md
```

---

## 六、批量安装指南

### 6.1 概述

批量安装脚本可以安装 prompt-engin 项目中的技能到你的项目，支持两种方式：
1. **全选安装**：一次性安装所有技能
2. **选择性安装**：交互式选择要安装的技能

安装后，你可以通过 `openskills sync -y` 选择要使用的技能。

**优势**：
- ✅ 支持全选或选择性安装，灵活配置
- ✅ 交互式选择，用户友好
- ✅ 安装后可以选择使用哪些技能
- ✅ 简单快捷，适合首次使用

### 6.2 使用方法

**方法1：从 prompt-engin 项目运行**

```bash
# 1. 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 2. 运行批量安装脚本，指定目标项目目录
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

**方法2：从目标项目运行**

```bash
# 1. 进入你的项目目录
cd /path/to/your-project

# 2. 运行批量安装脚本（使用相对路径）
bash ../prompt-engin/scripts/utils/install_all_skills.sh
```

**方法3：使用绝对路径**

```bash
# 在任何目录运行
bash /path/to/prompt-engin/scripts/utils/install_all_skills.sh /path/to/your-project
```

### 6.3 安装方式说明

**方式1：全选安装（选项 1）**

**适用场景**：
- 首次使用，想安装所有技能
- 不确定需要哪些技能，先全部安装

**操作**：
1. 选择选项 `1`（安装所有技能）
2. 确认安装
3. 等待安装完成

**方式2：选择性安装（选项 2）**

**适用场景**：
- 明确知道需要哪些技能
- 只想安装部分技能，节省时间

**操作**：
1. 选择选项 `2`（选择要安装的技能）
2. 输入技能编号（多个用逗号分隔，如：`1,3,5`）
   - 输入 `all` 选择全部
   - 可以跳过某些技能（不输入其编号）
3. 确认安装
4. 等待安装完成

**输入格式示例**：
- `1` - 只安装第 1 个技能
- `1,3,5` - 安装第 1、3、5 个技能（用逗号分隔）
- `1,2,3,4,5` - 安装第 1-5 个技能（不支持 `1-5` 范围语法，需要逐个输入）
- `all` 或 `ALL` - 选择全部技能（等同于选项 1）
- 输入无效编号会被自动跳过，并显示警告

**注意事项**：
- 技能编号从 1 开始
- 多个编号用逗号分隔，不要有空格（如：`1,3,5`，不是 `1, 3, 5`）
- 输入 `all` 等同于选择选项 1（安装所有技能）
- 如果未选择任何有效技能，脚本会退出

### 6.4 使用示例

**示例1：全选安装所有技能**

```bash
# 1. 进入 prompt-engin 项目
cd /Users/gengxiao/workspace/D-codeup/prompt-engin

# 2. 运行批量安装脚本
bash scripts/utils/install_all_skills.sh /Users/gengxiao/workspace/D-codeup/my-project

# 输出示例：
# ========================================
# 批量安装 prompt-engin 技能
# ========================================
# 
# 技能源目录: /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills
# 目标项目目录: /Users/gengxiao/workspace/D-codeup/my-project
# 
# 找到 16 个技能
# 
# 可用技能列表:
#  1. architecture-diagram-template
#  2. code-organization
#  3. compatibility-check
#  ...
# 
# 请选择安装方式:
#  1. 安装所有技能（全选）
#  2. 选择要安装的技能（交互式选择）
#  3. 取消安装
# 
# 请输入选项 [1-3]: 1
# 
# 已选择：安装所有 16 个技能
# 
# 确认安装到项目: /Users/gengxiao/workspace/D-codeup/my-project? [y/N]: y
# 
# 正在安装: architecture-diagram-template
# ✓ architecture-diagram-template (安装成功)
# ...
# 
# ========================================
# 安装完成
# ========================================
# 
# 成功安装: 16 个技能
```

**示例2：选择性安装技能**

```bash
# 1. 进入 prompt-engin 项目
cd /Users/gengxiao/workspace/D-codeup/prompt-engin

# 2. 运行批量安装脚本
bash scripts/utils/install_all_skills.sh /Users/gengxiao/workspace/D-codeup/my-project

# 输出示例：
# 请选择安装方式:
#  1. 安装所有技能（全选）
#  2. 选择要安装的技能（交互式选择）
#  3. 取消安装
# 
# 请输入选项 [1-3]: 2
# 
# 请选择要安装的技能（输入技能编号，多个用逗号分隔，如: 1,3,5）:
# 提示: 输入 'all' 选择全部，输入 'skip' 跳过某个技能
# 
# 请输入技能编号: 1,3,5,7
# 
# 已选择：安装 4 个技能
# 
# 将要安装的技能:
#  1. architecture-diagram-template
#  2. compatibility-check
#  3. design-principles
#  4. document-format
# 
# 确认安装到项目: /Users/gengxiao/workspace/D-codeup/my-project? [y/N]: y
# 
# 正在安装: architecture-diagram-template
# ✓ architecture-diagram-template (安装成功)
# ...
# 
# ========================================
# 安装完成
# ========================================
# 
# 成功安装: 4 个技能
```

**示例3：选择要使用的技能**

安装完成后，使用 `openskills sync -y` 选择要使用的技能：

```bash
# 进入目标项目目录
cd /path/to/your-project

# 同步技能到 AGENTS.md（交互式选择）
openskills sync -y

# 或者：查看已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format
```

---

## 七、技能创建指南

### 7.1 技能目录位置

**prompt-engin 项目中的技能目录**：`.claude/skills/`

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

### 7.2 创建技能的方法

**方法1：使用规则转技能工具（推荐）**

**工具位置**：`scripts/utils/convert_rule_to_skill.py`

**使用示例**：

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 从规则文件创建技能
python3 scripts/utils/convert_rule_to_skill.py \
  --rule-file prompts/stages/common/document/document-format.md \
  --skill-name document-format \
  --description "文档格式规范，包括任务清单、测试用例、文章报告等格式要求"
```

**参数说明**：
- `--rule-file`：规则文件路径（相对于项目根目录）
- `--skill-name`：技能名称（小写字母、数字、连字符）
- `--description`：技能描述（可选，如果不提供会自动提取）

**方法2：手动创建技能**

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

### 7.3 从规则文件创建技能

**可转换的规则文件**：

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

### 7.4 验证技能

**检查技能目录**：

```bash
# 检查技能目录是否存在
ls -la .claude/skills/

# 检查特定技能
ls -la .claude/skills/document-format/
cat .claude/skills/document-format/SKILL.md | head -20
```

**使用 OpenSkills 验证**：

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

## 八、故障排查指南

### 8.1 常见问题

**Q1：为什么不能直接安装整个技能目录？**

**问题描述**：

```bash
# ❌ 错误：尝试安装整个技能目录
openskills install /path/to/prompt-engin/.claude/skills

# 错误信息：
# Error: Command failed: git clone --depth 1 --quiet "https://github.com//Users" ...
```

**原因**：

`openskills install` **只能安装单个技能目录**，不能安装整个 `.claude/skills/` 目录。

当提供整个技能目录路径时，`openskills` 工具会误认为这是一个 GitHub 仓库路径，尝试执行 `git clone`，导致失败。

**解决方法**：

**方式1：使用批量安装脚本（推荐）**

```bash
# 从 prompt-engin 项目运行
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 或从目标项目运行
cd /path/to/your-project
bash ../prompt-engin/scripts/utils/install_all_skills.sh
```

**方式2：安装单个技能**

```bash
# ✅ 正确：安装单个技能目录
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format
# ... 逐个安装其他技能
```

**Q2：批量安装脚本执行失败**

**可能原因**：
1. **openskills 未安装或未正确配置**
2. **技能目录结构不正确**
3. **路径问题（相对路径 vs 绝对路径）**
4. **权限问题**

**解决方法**：

**步骤1：检查 openskills 安装**

```bash
# 检查 openskills 是否已安装
which openskills

# 如果未安装，安装 OpenSkills
npm install -g openskills

# 验证安装
openskills --version
```

**步骤2：检查技能目录结构**

```bash
# 检查技能目录是否存在
ls -la /path/to/prompt-engin/.claude/skills/

# 检查单个技能目录结构
ls -la /path/to/prompt-engin/.claude/skills/document-format/

# 确保 SKILL.md 文件存在
test -f /path/to/prompt-engin/.claude/skills/document-format/SKILL.md && echo "✓ SKILL.md 存在" || echo "✗ SKILL.md 不存在"
```

**步骤3：测试单个技能安装**

```bash
# 测试安装单个技能
cd /path/to/your-project
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 如果单个技能安装成功，说明 openskills 配置正确
# 如果失败，检查错误信息
```

**Q3：openskills install 提示路径错误**

**解决方法**：

**步骤1：验证路径**

```bash
# 检查路径是否存在
ls -la /path/to/prompt-engin/.claude/skills/document-format

# 使用绝对路径（推荐）
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format
```

**步骤2：使用相对路径（如果在同一工作区）**

```bash
# 如果 prompt-engin 和你的项目在同一工作区
cd /path/to/your-project
openskills install ../prompt-engin/.claude/skills/document-format
```

**步骤3：检查路径格式**

```bash
# ✅ 正确：指向单个技能目录
openskills install /path/to/prompt-engin/.claude/skills/document-format

# ❌ 错误：指向整个技能目录
openskills install /path/to/prompt-engin/.claude/skills

# ❌ 错误：路径中包含空格（需要引号）
openskills install "/path/to/prompt-engin/.claude/skills/document-format"
```

**Q4：openskills sync -y 没有同步技能**

**可能原因**：
1. **技能未正确安装**
2. **技能目录位置不正确**
3. **AGENTS.md 文件权限问题**

**解决方法**：

**步骤1：检查已安装的技能**

```bash
# 列出已安装的技能
openskills list

# 检查技能目录
ls -la .claude/skills/
```

**步骤2：验证技能安装**

```bash
# 检查技能目录是否存在
test -d .claude/skills/document-format && echo "✓ 技能目录存在" || echo "✗ 技能目录不存在"

# 检查 SKILL.md 文件
test -f .claude/skills/document-format/SKILL.md && echo "✓ SKILL.md 存在" || echo "✗ SKILL.md 不存在"
```

**步骤3：手动同步**

```bash
# 确保在项目根目录
cd /path/to/your-project

# 运行同步命令
openskills sync -y

# 检查 AGENTS.md 是否已创建/更新
cat AGENTS.md
```

**Q5：技能安装后无法使用**

**可能原因**：
1. **AGENTS.md 未正确同步**
2. **技能格式不正确**
3. **AI 未读取 AGENTS.md**

**解决方法**：

**步骤1：检查 AGENTS.md**

```bash
# 查看 AGENTS.md 内容
cat AGENTS.md

# 确保技能列表在 <available_skills> 标签中
grep -A 20 "<available_skills>" AGENTS.md
```

**步骤2：验证技能格式**

```bash
# 检查技能文件格式
cat .claude/skills/document-format/SKILL.md | head -20

# 确保包含正确的元数据
# ---
# name: document-format
# description: ...
# tags: ...
# ---
```

**步骤3：重新同步**

```bash
# 重新同步技能到 AGENTS.md
openskills sync -y

# 验证同步结果
cat AGENTS.md
```

### 8.2 调试技巧

**1. 启用详细输出**

```bash
# 批量安装脚本会显示详细输出
bash scripts/utils/install_all_skills.sh /path/to/your-project

# openskills 命令的详细输出
openskills install /path/to/skill --verbose  # 如果支持
```

**2. 检查日志**

```bash
# 检查 openskills 临时目录
ls -la ~/.openskills-temp-*/

# 检查项目中的技能目录
ls -la .claude/skills/
ls -la .agent/skills/  # 如果使用 universal 模式
```

**3. 验证安装**

```bash
# 列出已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format

# 检查技能目录结构
tree .claude/skills/  # 如果安装了 tree 命令
# 或
find .claude/skills/ -type f -name "*.md"
```

### 8.3 最佳实践

**1. 使用批量安装脚本**

**推荐**：使用批量安装脚本，而不是手动逐个安装。

```bash
# ✅ 推荐
bash scripts/utils/install_all_skills.sh /path/to/your-project

# ❌ 不推荐（容易出错）
openskills install /path/to/.claude/skills  # 错误：不能安装整个目录
```

**2. 使用绝对路径**

**推荐**：使用绝对路径，避免路径解析问题。

```bash
# ✅ 推荐：绝对路径
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format

# ⚠️ 谨慎：相对路径（需要确保工作目录正确）
openskills install ../prompt-engin/.claude/skills/document-format
```

**3. 验证安装结果**

**推荐**：安装后验证技能是否正确安装。

```bash
# 安装后验证
openskills list
openskills read document-format
openskills sync -y
cat AGENTS.md
```

---

## 九、使用示例

### 9.1 快速示例

**示例1：生成精简版规则文件（方式2）✅ 重点推荐**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 复制到你的项目
cp .cursorrules /path/to/your-project/

# 完成！Token 占用减少约 60%
```

**结果**：
- 文件大小：3427 行，约 124KB
- 只包含核心规则，Token 占用减少约 60%

**示例2：生成完整版规则文件（方式1）✅ 适用于小项目**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成完整版规则文件
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 复制到你的项目
cp .cursorrules /path/to/your-project/

# 完成！直接使用即可
```

**结果**：
- 文件大小：8597 行，约 308KB
- 包含所有规则，始终可用

**示例3：同时生成完整版和精简版**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成完整版
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.full

# 生成精简版
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# 根据项目需求选择使用：
# - 小项目或不需要 token 优化：使用 .cursorrules.full
# - 大项目或需要 token 优化：使用 .cursorrules.core
```

### 9.2 对比结果

| 指标 | 完整版 | 精简版 | 节省 |
|------|--------|--------|------|
| **行数** | 8597 行 | 3427 行 | **约 60%** |
| **文件大小** | ~308KB | ~124KB | **约 60%** |
| **Token 占用** | 大 | 小 | **约 60%** |
| **使用复杂度** | 简单（复制即用） | 简单（复制即用） | - |

### 9.3 验证生成结果

```bash
# 检查文件大小
wc -l .cursorrules
du -h .cursorrules

# 完整版应该约 8597 行
# 精简版应该约 3427 行
```

---

## 十、快速参考

### 10.1 技能目录位置

**prompt-engin 项目中的技能目录**：`.claude/skills/`

**完整路径**：`/path/to/prompt-engin/.claude/skills/`

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

**具体项目中的技能目录**：

**位置**：`.claude/skills/` 或 `.agent/skills/`

**完整路径**：`/path/to/your-project/.claude/skills/`

**注意**：技能目录会在安装技能时自动创建，不需要手动创建。

### 10.2 快速使用

**方式1：批量安装所有技能（推荐）**

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

**方式2：安装单个技能**

```bash
# 1. 进入你的项目目录
cd /path/to/your-project

# 2. 安装单个技能（使用绝对路径）
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format

# 3. 同步到 AGENTS.md
openskills sync -y
```

**方式3：使用相对路径（如果在同一工作区）**

```bash
# 如果 prompt-engin 和你的项目在同一工作区
cd /path/to/your-project

# 使用相对路径
openskills install ../prompt-engin/.claude/skills/document-format
openskills install ../prompt-engin/.claude/skills/time-format

# 同步到 AGENTS.md
openskills sync -y
```

### 10.3 常见问题速查

**Q1：`.claude/skills` 目录在哪里？**

**A1**：
- **prompt-engin 项目**：`.claude/skills/` 在项目根目录下
- **具体项目**：`.claude/skills/` 在项目根目录下（安装技能后自动创建）

**Q2：如何找到 prompt-engin 的技能目录？**

**A2**：使用绝对路径或相对路径：

```bash
# 绝对路径（推荐）
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format

# 相对路径（如果在同一工作区）
openskills install ../prompt-engin/.claude/skills/document-format
```

**Q3：为什么不能直接安装整个技能目录？**

**A3**：

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

---

## 📚 相关文档

- [V2 版本改进计划](../V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) - 三个平台 + 三种组织方式的完整指南

---

**最后更新**：2025-12-24（本地时间）

