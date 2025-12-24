# 多平台多方式规则使用指南

> **文件说明**：本指南说明如何在多个 IDE 平台（Cursor、TRAE、Antigravity）中使用不同的规则文件方式
> **创建时间**：2025-12-23
> **更新时间**：2025-12-23

---

## 📋 目录

- [概述](#概述)
- [三种使用方式](#三种使用方式)
- [三个平台支持](#三个平台支持)
- [使用方式对比](#使用方式对比)
- [同步方案设计](#同步方案设计)
- [实施计划](#实施计划)
- [使用建议](#使用建议)

---

## 概述

Prompt Engine 支持在多个 IDE 平台（Cursor、TRAE、Antigravity）中使用规则文件，每种平台都支持三种使用方式：

1. **方式1**：单个规则文件（完整版）
2. **方式2**：单个规则文件（精简版）+ 技能系统
3. **方式3**：多文件目录（新规则系统）

---

## 三种使用方式

### 方式1：单个规则文件（完整版）

**特点**：
- 单个文件，简单直接
- 包含所有规则（约 8597 行）
- Token 占用较大

**生成方式**：
```bash
# Cursor
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# TRAE
python3 scripts/prompt-engine merge --all --ide trae --output .traerules

# Antigravity
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules
```

**使用方式**：
```bash
# 复制到目标项目根目录
cp .cursorrules /path/to/project/
# 或
cp .traerules /path/to/project/
# 或
cp .antigravityrules /path/to/project/
```

**适用场景**：
- ✅ 小项目，不需要 Token 优化
- ✅ 希望所有规则始终可用
- ✅ 简单直接，不想管理多个文件

---

### 方式2：单个规则文件（精简版）+ 技能系统

**特点**：
- 单个文件，但只包含核心规则（约 3427 行）
- Token 占用减少约 60%
- 可选规则转换为技能，按需加载

**生成方式**：
```bash
# Cursor
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# TRAE
python3 scripts/prompt-engine merge --core-only --ide trae --output .traerules.core

# Antigravity
python3 scripts/prompt-engine merge --core-only --ide antigravity --output .antigravityrules.core
```

**使用方式**：
```bash
# 1. 复制规则文件到目标项目
cp .cursorrules.core /path/to/project/.cursorrules

# 2. 安装技能（按需）
bash scripts/utils/install_all_skills.sh /path/to/project

# 3. 同步技能到 AGENTS.md
cd /path/to/project
openskills sync -y
```

**适用场景**：
- ✅ 大项目，需要 Token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

---

### 方式3：多文件目录（新规则系统）

**特点**：
- 多个规则文件，按模块/阶段组织
- 支持路径特定配置（glob 模式）
- 支持文件引用（@file）
- Cursor 新规则系统（推荐）

**目录结构示例**：

**Cursor**：
```
项目根目录/
└── .cursor/
    └── rules/
        ├── 001-common.mdc       # 通用规则（优先级最高）
        ├── 002-code.mdc         # 代码规范
        ├── 003-mode.mdc         # 模式规则
        ├── 010-frontend.mdc     # 前端规则（适用于 **/*.tsx, **/*.jsx）
        └── 020-backend.mdc      # 后端规则（适用于 **/*.py, **/*.go）
```

**TRAE**：
```
项目根目录/
└── .trae/
    ├── ai-rules.yml             # 项目特定规则
    └── team-rules.yml           # 团队规则（可选）
```

**Antigravity**：
```
项目根目录/
├── .antigravityrules          # 规则文件（单文件方式）
└── *.agent                    # 代理配置文件（Agent-First 架构）
    ├── code_generator.agent   # 代码生成代理
    ├── test_writer.agent      # 测试编写代理
    └── ...
```

**规则文件格式示例**：

**Cursor**（Markdown 格式）：
```markdown
# 前端规则

[适用于: **/*.tsx, **/*.jsx, **/*.vue]

前端组件开发规范...

@file: common.mdc
@file: code.mdc
```

**TRAE**（YAML 格式）：
```yaml
# .trae/ai-rules.yml
rules:
  - name: 代码规范
    description: 项目代码规范
    content: |
      代码格式规范...
  
  - name: 命名规范
    description: 命名规范
    content: |
      命名规范要求...
```

**Antigravity**（Agent 配置文件，YAML 格式）：
```yaml
# code_generator.agent
name: "代码生成代理"
description: "负责根据需求生成代码的代理"
model: "Gemini 3 Pro"
tasks:
  - description: "分析需求文档"
    input: "需求文档路径"
  - description: "生成代码结构"
    output: "代码文件"
dependencies:
  - DocumentationAgent
```

**同步方式**（待实现）：
```bash
# Cursor：同步到目标项目的 .cursor/rules/ 目录
bash scripts/utils/sync_rules.sh --platform cursor --mode multi-files /path/to/project

# TRAE：同步到目标项目的 .trae/ 目录（需要转换为 YAML 格式）
bash scripts/utils/sync_rules.sh --platform trae --mode multi-files /path/to/project
```

**适用场景**：
- ✅ 需要路径特定配置（不同文件类型使用不同规则）
- ✅ 大型项目，需要精细控制
- ✅ 团队协作，需要版本控制规则文件
- ✅ 使用 Cursor 新规则系统（`.cursor/rules/`）
- ✅ 使用 TRAE 项目/团队规则（`.trae/ai-rules.yml`）

> ⚠️ **Antigravity 说明**：
> - Antigravity 的 `.agent` 文件用于配置 AI 代理，不是规则文件
> - 如果需要多文件规则支持，目前只能使用 `.antigravityrules` 单文件方式
> - `.agent` 文件适用于需要配置 AI 代理行为的场景

---

## 三个平台支持

### 平台配置映射表

| 平台 | 单文件方式 | 多文件目录 | 规则文件格式 | 状态 |
|------|----------|-----------|------------|------|
| **Cursor** | `.cursorrules` | `.cursor/rules/` | `.mdc` | ✅ 完全支持 |
| **TRAE** | `.traerules` | `.trae/ai-rules.yml` | `.yml` (YAML) | ✅ 支持（YAML 格式） |
| **Antigravity** | `.antigravityrules` | `.agent` (代理配置) | `.agent` (YAML/JSON) | ✅ 单文件支持，`.agent` 支持（非规则文件） |

### 平台特定说明

#### Cursor IDE

**单文件方式**：
- 文件位置：项目根目录
- 文件名：`.cursorrules`
- 自动识别：✅ 是

**多文件目录方式**：
- 目录位置：`.cursor/rules/`
- 文件格式：`.mdc` 文件
- 优先级：文件名前缀数字，数字越小优先级越高
- 路径配置：支持 glob 模式
- 文件引用：支持 `@file` 引用

#### TRAE IDE

**单文件方式**：
- 文件位置：项目根目录
- 文件名：`.traerules`
- 自动识别：✅ 是

**多文件目录方式**：
- ✅ **支持**：`.trae/` 目录下的配置文件
- 文件格式：YAML 格式（`.yml`）
- 配置文件：
  - `.trae/ai-rules.yml` - 项目特定规则
  - `.trae/team-rules.yml` - 团队规则（可选）
- 规则优先级：
  1. 项目特定规则 (`.trae/ai-rules.yml`)
  2. 团队规则 (`.trae/team-rules.yml`)
  3. 全局用户规则（用户设置）
  4. 默认规则（TRAE 内置）
- ⚠️ **注意**：TRAE 使用 YAML 格式，不是 Markdown 格式

#### Antigravity IDE

**单文件方式**：
- 文件位置：项目根目录
- 文件名：`.antigravityrules`
- 自动识别：✅ 是

**多文件目录方式（规则文件）**：
- ⚠️ **未确认**：目前公开资料中未明确提及对多规则文件的支持
- ⚠️ **状态**：Antigravity 仍处于公开预览阶段，相关功能可能尚未完善或文档化
- ⚠️ **建议**：参考官方指南或联系 Antigravity 支持团队获取最新信息

> 💡 **说明**：Antigravity 的 `.agent` 文件是**代理配置文件**，不是规则文件。如果需要多文件规则支持，目前只能使用 `.antigravityrules` 单文件方式。

**Agent 配置文件**（`.agent` 文件）：
- ✅ **支持**：Antigravity IDE 采用 "Agent-First" 架构
- 文件格式：YAML 或 JSON
- 用途：定义和配置 AI 代理的行为和任务
- 配置内容：
  - `name`：代理名称
  - `description`：代理功能描述
  - `model`：使用的 AI 模型（如 Gemini 3 Pro、Claude Sonnet 4.5、GPT-OSS）
  - `tasks`：代理需要执行的任务列表
  - `dependencies`：代理依赖的其他代理或资源
- 使用方式：
  1. 在项目目录中创建 `.agent` 文件（如 `my_agent.agent`）
  2. 使用 YAML 或 JSON 格式定义代理配置
  3. 在 Antigravity IDE 的 Agent Manager 中加载代理
  4. 代理将根据配置自动执行任务

**示例 `.agent` 文件**：
```yaml
name: "代码生成代理"
description: "负责根据需求生成代码的代理"
model: "Gemini 3 Pro"
tasks:
  - description: "分析需求文档"
    input: "需求文档路径"
  - description: "生成代码结构"
    output: "代码文件"
  - description: "编写测试用例"
    output: "测试文件"
dependencies:
  - DocumentationAgent
```

> 💡 **注意**：`.agent` 文件用于配置 AI 代理，与 `.antigravityrules` 规则文件不同。规则文件用于定义代码规范，而 `.agent` 文件用于定义 AI 代理的行为。

---

## 使用方式对比

### 三种方式对比表

| 特性 | 方式1：完整版 | 方式2：精简版+技能 | 方式3：多文件目录 |
|------|-------------|------------------|------------------|
| **文件数量** | 1 个文件 | 1 个文件 + N 个技能 | N 个规则文件 |
| **Token 占用** | 高（8597 行） | 低（3427 行 + 按需） | 中等（按需加载） |
| **配置灵活性** | 低 | 中 | 高（路径特定） |
| **维护复杂度** | 低 | 中 | 高 |
| **适用项目** | 小项目 | 大项目 | 大型/复杂项目 |
| **Cursor** | ✅ 支持 | ✅ 支持 | ✅ 支持（新方式） |
| **TRAE** | ✅ 支持 | ⚠️ 待确认 | ✅ 支持（YAML 格式） |
| **Antigravity** | ✅ 支持 | ⚠️ 待确认 | ⚠️ 多文件规则未确认，`.agent` 支持（代理配置） |

### 选择建议

**方式1：完整版** → 适合：
- 小项目、简单需求
- 不需要 Token 优化
- 希望所有规则始终可用

**方式2：精简版+技能** → 适合：
- 大项目、需要 Token 优化
- 希望按需加载规则
- 已安装 OpenSkills 工具

**方式3：多文件目录** → 适合：
- 大型/复杂项目
- 需要路径特定配置
- 需要精细控制规则应用
- 团队协作，需要版本控制

---

## 同步方案设计

### 统一同步脚本设计

**脚本功能**：
- 支持选择平台（cursor、trae、antigravity、all）
- 支持选择方式（single-full、single-core、multi-files）
- 支持预览模式（dry-run）
- 支持增量同步和备份

**使用方式**：
```bash
# 方式1：单文件完整版
bash scripts/utils/sync_rules.sh \
  --platform cursor \
  --mode single-full \
  --target /path/to/project

# 方式2：单文件精简版 + 技能
bash scripts/utils/sync_rules.sh \
  --platform cursor \
  --mode single-core \
  --target /path/to/project

# 方式3：多文件目录
bash scripts/utils/sync_rules.sh \
  --platform cursor \
  --mode multi-files \
  --target /path/to/project

# 预览模式
bash scripts/utils/sync_rules.sh \
  --platform cursor \
  --mode multi-files \
  --target /path/to/project \
  --dry-run

# 同时支持多个平台
bash scripts/utils/sync_rules.sh \
  --platform all \
  --mode single-full \
  --target /path/to/project
```

### 平台配置映射

**配置文件**（待实现）：
```yaml
platforms:
  cursor:
    single_file: .cursorrules
    single_file_core: .cursorrules.core
    rules_dir: .cursor/rules/
    file_ext: .mdc
    supported_modes:
      - single-full
      - single-core
      - multi-files
  trae:
    single_file: .traerules
    single_file_core: .traerules.core
    rules_dir: .trae/
    rules_file: ai-rules.yml
    team_rules_file: team-rules.yml
    file_ext: .yml  # YAML 格式
    supported_modes:
      - single-full
      - single-core
      - multi-files  # 支持，但需要转换为 YAML 格式
  antigravity:
    single_file: .antigravityrules
    single_file_core: .antigravityrules.core
    agent_files: *.agent  # Agent 配置文件
    file_ext: .agent  # YAML 或 JSON 格式
    supported_modes:
      - single-full
      - single-core
      - multi-files  # 通过 .agent 文件实现
    note: ".agent 文件用于配置 AI 代理，与规则文件不同"
```

### 规则文件组织策略

**多文件目录组织方式**：

1. **按模块组织**：
   - `001-common.md` - 通用规则
   - `002-code.md` - 代码规范
   - `003-mode.md` - 模式规则
   - `004-project.md` - 项目规范

2. **按阶段组织**：
   - `010-requirements.md` - 需求分析阶段
   - `020-design.md` - 设计阶段
   - `030-development.md` - 开发阶段
   - `040-testing.md` - 测试阶段

3. **按文件类型组织**（路径特定）：
   - `100-frontend.md` - 前端规则（适用于 `**/*.tsx, **/*.jsx`）
   - `110-backend.md` - 后端规则（适用于 `**/*.py, **/*.go`）
   - `120-mobile.md` - 移动端规则（适用于 `**/*.ts, **/*.swift`）

---

## 实施计划

### 阶段1：确认平台支持（已完成）

- [x] 确认 TRAE 支持 `.trae/ai-rules.yml` 配置文件（YAML 格式）
- [x] 确认 TRAE 支持团队规则 `.trae/team-rules.yml`
- [x] 确认 Antigravity 支持 `.agent` 文件（Agent 配置文件，不是规则文件）
- [x] 确认 Cursor 使用 `.cursor/rules/` 目录（Markdown 格式）
- [x] 确认 TRAE 使用 `.trae/` 目录（YAML 格式）
- [x] 确认 Antigravity 支持 `.agent` 文件（Agent 配置文件，YAML/JSON 格式）

### 阶段2：实现单文件方式（已完成）

- [x] 方式1：单文件完整版（已支持三个平台）
- [x] 方式2：单文件精简版 + 技能（已支持 Cursor）
- [ ] 方式2：扩展到 TRAE 和 Antigravity

### 阶段3：实现多文件目录方式（待实现）

- [ ] 创建规则文件组织策略
- [ ] 实现 Cursor 的 `.cursor/rules/` 同步脚本（Markdown 格式）
- [ ] 实现 TRAE 的 `.trae/ai-rules.yml` 同步脚本（需要 Markdown 转 YAML）
- [ ] 实现 Antigravity 的 `.agent` 文件同步脚本（需要转换为 Agent 配置格式）
- [ ] 创建统一的同步脚本（支持多平台）
- [ ] 扩展 `install_all_skills.sh` 添加选项
- [ ] 实现 Markdown 到 YAML 的转换工具（用于 TRAE）

### 阶段4：文档和测试（待实现）

- [ ] 更新 README.md 说明三种方式
- [ ] 创建使用示例
- [ ] 测试同步脚本功能
- [ ] 更新 CHANGELOG.md

---

## 使用建议

### 快速选择指南

**场景1：小项目，简单需求**
→ 使用 **方式1（完整版）**
```bash
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules
cp .cursorrules /path/to/project/
```

**场景2：大项目，需要 Token 优化**
→ 使用 **方式2（精简版+技能）**
```bash
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core
cp .cursorrules.core /path/to/project/.cursorrules
bash scripts/utils/install_all_skills.sh /path/to/project
```

**场景3：大型/复杂项目，需要精细控制**
→ 使用 **方式3（多文件目录）**
```bash
# Cursor（Markdown 格式）
bash scripts/utils/sync_rules.sh --platform cursor --mode multi-files /path/to/project

# TRAE（YAML 格式，需要转换）
bash scripts/utils/sync_rules.sh --platform trae --mode multi-files /path/to/project
```

### 平台选择建议

**使用 Cursor IDE**：
- ✅ 三种方式都支持
- ✅ 推荐使用方式3（多文件目录，`.cursor/rules/`）

**使用 TRAE IDE**：
- ✅ 方式1（完整版）已支持
- ⚠️ 方式2（精简版+技能）待确认
- ✅ 方式3（多文件目录）已支持，使用 `.trae/ai-rules.yml`（YAML 格式）

**使用 Antigravity IDE**：
- ✅ 方式1（完整版）已支持（`.antigravityrules`）
- ⚠️ 方式2（精简版+技能）待确认
- ⚠️ 方式3（多文件规则）未确认（目前只支持单文件 `.antigravityrules`）
- ✅ `.agent` 文件支持（用于配置 AI 代理，不是规则文件）
- 💡 **重要说明**：
  - `.antigravityrules` - 规则文件，用于定义代码规范（类似 `.cursorrules`）
  - `.agent` - 代理配置文件，用于定义 AI 代理的行为和任务（与规则文件不同）
  - 如果需要多文件规则支持，目前只能使用 `.antigravityrules` 单文件方式

### 迁移建议

**从方式1迁移到方式2**：
1. 生成精简版规则文件
2. 复制到项目并重命名
3. 安装需要的技能
4. 测试功能是否正常

**从方式1/方式2迁移到方式3**：
1. 确认平台支持：
   - Cursor：✅ 支持 `.cursor/rules/` 目录（Markdown 格式）
   - TRAE：✅ 支持 `.trae/ai-rules.yml`（需要转换为 YAML 格式）
   - Antigravity：✅ 支持 `.agent` 文件（Agent 配置文件，YAML/JSON 格式）
2. 使用同步脚本同步规则文件
3. 配置路径特定规则（如需要）
4. 测试功能是否正常

> 💡 **重要说明**：
> - **Cursor**：方式3 使用 `.cursor/rules/` 目录，规则文件用于定义代码规范
> - **TRAE**：方式3 使用 `.trae/ai-rules.yml`，需要将 Markdown 规则转换为 YAML 格式
> - **Antigravity**：方式3 使用 `.agent` 文件，但这是**代理配置文件**，不是规则文件。`.agent` 文件用于配置 AI 代理的行为，与 `.antigravityrules` 规则文件用途不同

---

## 相关文档

- [快速开始指南](../QUICK_START.md)
- [技能使用指南](./skills-usage-guide.md)
- [Token 优化指南](./token-optimization-guide.md)
- [使用示例](./USAGE_EXAMPLE.md)

---

## 更新日志

- **2025-12-23**：
  - 创建文档，记录多平台多方式使用方案
  - 确认 TRAE 支持 `.trae/ai-rules.yml`（YAML 格式）
  - 确认 Antigravity 支持 `.agent` 文件（Agent 配置文件，YAML/JSON 格式）
  - 更新平台配置映射表和使用建议
  - 添加 Antigravity `.agent` 文件使用说明和示例

---

**最后更新**：2025-12-23

