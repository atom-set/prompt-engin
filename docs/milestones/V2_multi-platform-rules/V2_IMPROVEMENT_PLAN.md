# V2 版本改进计划

> **文件说明**：V2 版本大改进计划文档，整合 README 重构方案和多平台多方式规则使用指南
> **版本核心**：三个平台（Cursor、TRAE、Antigravity）+ 三种组织方式（单文件完整版、单文件精简版+技能、多文件目录）
> **创建时间**：2025-12-24（本地时间）
> **更新时间**：2025-12-24（本地时间）

---

## 📋 目录

- [一、V2 版本概述](#一v2-版本概述)
- [二、核心特性：三个平台 + 三种组织方式](#二核心特性三个平台--三种组织方式)
- [三、README.md 重构方案](#三readmemd-重构方案)
- [四、产物目录设计（dist）](#四产物目录设计dist)
- [五、多平台多方式规则使用指南](#五多平台多方式规则使用指南)
- [六、实施计划](#六实施计划)
- [七、预期效果](#七预期效果)

---

## 一、V2 版本概述

### 版本定位

**V2 版本**是 Prompt Engine 的重大改进版本，核心特性是支持**三个平台（Cursor、TRAE、Antigravity）**和**三种组织方式（单文件完整版、单文件精简版+技能、多文件目录）**。

### 核心改进

1. **多平台支持**：
   - ✅ Cursor IDE（完全支持）
   - ✅ TRAE IDE（支持 YAML 格式）
   - ✅ Antigravity IDE（单文件支持）

2. **三种组织方式**：
   - ✅ 方式1：单文件完整版（简单直接）
   - ✅ 方式2：单文件精简版 + 技能系统（Token 优化，推荐）
   - ✅ 方式3：多文件目录（精细控制）

3. **产物目录（dist）**：
   - ✅ 统一存放生成的规则文件产物
   - ✅ 支持 Git 追踪，用户无需安装环境即可使用
   - ✅ 支持通过 `cp` 或脚本同步到具体项目

4. **README.md 重构**：
   - ✅ 简化结构，分为四个主要部分
   - ✅ 添加环境安装和测试部分
   - ✅ 详情跳转到专门文档

---

## 二、核心特性：三个平台 + 三种组织方式

### 平台 × 方式矩阵

| 平台 | 方式1：单文件完整版 | 方式2：单文件精简版+技能 | 方式3：多文件目录 | 状态 |
|------|-------------------|----------------------|------------------|------|
| **Cursor** | ✅ `.cursorrules.all` | ✅ `.cursorrules.core` + 技能 | ✅ `.cursor/rules/` | ✅ 完全支持 |
| **TRAE** | ✅ `.traerules.all` | ⚠️ 待确认 | ✅ `.trae/ai-rules.yml` | ✅ 支持（YAML 格式） |
| **Antigravity** | ✅ `.antigravityrules.all` | ⚠️ 待确认 | ⚠️ `.agent` (代理配置) | ✅ 单文件支持 |

### 三种组织方式详细说明

#### 方式1：单文件完整版

**特点**：
- 单个文件，简单直接
- 包含所有规则（约 8597 行）
- Token 占用较大

**适用场景**：
- ✅ 小项目，不需要 Token 优化
- ✅ 希望所有规则始终可用
- ✅ 简单直接，不想管理多个文件

**生成方式**：
```bash
# Cursor
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.all

# TRAE
python3 scripts/prompt-engine merge --all --ide trae --output .traerules.all

# Antigravity
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules.all
```

**使用方式**（从 dist 目录）：
```bash
# 克隆仓库后，dist 目录已包含所有产物，无需生成

# Cursor
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules

# TRAE
cp dist/trae/single-full/.traerules.all /path/to/your-project/.traerules

# Antigravity
cp dist/antigravity/single-full/.antigravityrules.all /path/to/your-project/.antigravityrules
```

---

#### 方式2：单文件精简版 + 技能系统（推荐）⭐

**特点**：
- 单个文件，但只包含核心规则（约 3427 行）
- Token 占用减少约 60%
- 可选规则转换为技能，按需加载

**适用场景**：
- ✅ 大项目，需要 Token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

**生成方式**：
```bash
# Cursor
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# TRAE
python3 scripts/prompt-engine merge --core-only --ide trae --output .traerules.core

# Antigravity
python3 scripts/prompt-engine merge --core-only --ide antigravity --output .antigravityrules.core
```

**使用方式**（从 dist 目录）：
```bash
# 1. 复制规则文件到目标项目
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 2. 安装技能（按需）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 3. 同步技能到 AGENTS.md
cd /path/to/your-project
openskills sync -y
```

---

#### 方式3：多文件目录

**特点**：
- 多个规则文件，按模块/阶段组织
- 支持路径特定配置（glob 模式）
- 支持文件引用（@file）

**适用场景**：
- ✅ 需要路径特定配置（不同文件类型使用不同规则）
- ✅ 大型项目，需要精细控制
- ✅ 团队协作，需要版本控制规则文件

**目录结构**：

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

**同步方式**（待实现）：
```bash
# Cursor：同步到目标项目的 .cursor/rules/ 目录
bash scripts/utils/sync_to_project.sh --platform cursor --mode multi-files /path/to/project

# TRAE：同步到目标项目的 .trae/ 目录（需要转换为 YAML 格式）
bash scripts/utils/sync_to_project.sh --platform trae --mode multi-files /path/to/project
```

> ⚠️ **Antigravity 说明**：
> - Antigravity 的 `.agent` 文件用于配置 AI 代理，不是规则文件
> - 如果需要多文件规则支持，目前只能使用 `.antigravityrules` 单文件方式
> - `.agent` 文件适用于需要配置 AI 代理行为的场景

---

### 平台支持详细说明

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

**Agent 配置文件**（`.agent` 文件）：
- ✅ **支持**：Antigravity IDE 采用 "Agent-First" 架构
- 文件格式：YAML 或 JSON
- 用途：定义和配置 AI 代理的行为和任务
- ⚠️ **注意**：`.agent` 文件用于配置 AI 代理，与 `.antigravityrules` 规则文件不同

---

## 三、README.md 重构方案

### 重构目标

将 README.md 重新组织为更清晰的结构，分为四个主要部分：
1. **简单介绍**：只保留核心信息，详情跳转到专门文档
2. **环境安装和测试**：包含环境检查和测试脚本
3. **三种方式和三个 IDE 使用手册**：详细的使用指南
4. **其他**：项目结构、贡献、许可证等

### 新结构设计

```
README.md
├── 1. 项目简介（简洁版）
│   ├── 核心定位（1-2 句话）
│   ├── 核心特性（列表，简洁）
│   └── 快速链接（跳转到详细文档）
│
├── 2. 环境安装和测试
│   ├── 系统要求
│   ├── 安装步骤
│   ├── 环境测试脚本
│   └── 常见问题
│
├── 3. 使用手册
│   ├── 三种使用方式快速选择
│   ├── 三个平台支持情况
│   └── 详细文档链接
│
└── 4. 其他
    ├── 项目结构（简化）
    ├── 开发指南（简化）
    ├── 贡献指南（链接）
    ├── 许可证（链接）
    └── 相关资源（链接）
```

### 需要创建的新文档

1. **环境安装和测试文档**：`docs/guides/INSTALLATION_AND_TESTING.md`
2. **使用手册**：`docs/guides/USAGE_MANUAL.md`
3. **快速参考卡片**：`docs/guides/QUICK_REFERENCE.md`

---

## 四、产物目录设计（dist）

### dist 目录结构

**目的**：统一存放生成的规则文件产物，方便分发和同步到具体项目

**目录结构**：
```
dist/
├── README.md                    # 产物说明文档
├── cursor/                      # Cursor IDE 产物
│   ├── single-full/
│   │   └── .cursorrules.all     # 完整版规则文件（8597 行）
│   ├── single-core/
│   │   └── .cursorrules.core    # 精简版规则文件（3427 行）
│   └── multi-files/
│       └── rules/               # 多文件目录
│           ├── 001-common.mdc
│           ├── 002-code.mdc
│           └── ...
├── trae/                        # TRAE IDE 产物
│   ├── single-full/
│   │   └── .traerules.all       # 完整版规则文件
│   ├── single-core/
│   │   └── .traerules.core      # 精简版规则文件
│   └── multi-files/
│       └── .trae/               # 多文件目录
│           ├── ai-rules.yml
│           └── team-rules.yml
└── antigravity/                 # Antigravity IDE 产物
    ├── single-full/
    │   └── .antigravityrules.all # 完整版规则文件
    ├── single-core/
    │   └── .antigravityrules.core # 精简版规则文件
    └── multi-files/
        └── *.agent              # Agent 配置文件（如果支持）
```

### 生成产物脚本

**文件**：`scripts/utils/generate_dist.sh`

**功能**：
- 生成所有平台的三种方式产物
- 自动组织到 `dist/` 目录
- 支持单独生成某个平台或某种方式

**使用方式**：
```bash
# 生成所有平台的三种方式产物
bash scripts/utils/generate_dist.sh --all

# 生成特定平台的产物
bash scripts/utils/generate_dist.sh --platform cursor
bash scripts/utils/generate_dist.sh --platform trae
bash scripts/utils/generate_dist.sh --platform antigravity

# 生成特定方式的产物
bash scripts/utils/generate_dist.sh --mode single-full
bash scripts/utils/generate_dist.sh --mode single-core
bash scripts/utils/generate_dist.sh --mode multi-files

# 生成特定平台和方式的产物
bash scripts/utils/generate_dist.sh --platform cursor --mode single-core
```

### 同步到项目脚本

**文件**：`scripts/utils/sync_to_project.sh`

**功能**：
- 从 `dist/` 目录同步产物到具体项目
- 支持三种方式和三个平台
- 支持预览模式（dry-run）

**使用方式**：
```bash
# 同步到项目（交互式选择）
bash scripts/utils/sync_to_project.sh /path/to/your-project

# 指定平台和方式
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode single-core \
  /path/to/your-project

# 预览模式（不实际同步）
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode single-core \
  --dry-run \
  /path/to/your-project
```

### Git 管理策略

**`.gitignore` 配置**：
```gitignore
# Distribution files (dist/) - 允许追踪，用户可直接使用
# dist/ 目录中的产物文件应该提交到 Git，方便用户直接使用（无需安装环境）
```

**说明**：
- ✅ **允许追踪**：`dist/` 目录中的产物文件应该提交到 Git
- ✅ **用户友好**：用户可以直接从 Git 仓库获取产物，无需安装环境
- ✅ **即开即用**：克隆仓库后即可使用 `dist/` 目录中的产物

**优势**：
1. **无需安装环境**：用户可以直接使用 `dist/` 目录中的产物
2. **快速上手**：克隆仓库后即可使用，无需运行生成脚本
3. **版本同步**：产物文件与代码版本同步，确保一致性
4. **离线使用**：即使没有 Python 环境，也可以直接使用产物

**更新流程**：
```bash
# 1. 生成产物
bash scripts/utils/generate_dist.sh --all

# 2. 验证产物
bash scripts/utils/verify_dist.sh

# 3. 提交到 Git
git add dist/
git commit -m "chore: update distribution files"
git push
```

**用户使用方式**（无需安装环境）：
```bash
# 1. 克隆仓库
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin

# 2. 直接使用 dist 目录中的产物
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 或使用同步脚本
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode single-core \
  /path/to/your-project
```

---

## 五、多平台多方式规则使用指南

### 使用方式对比

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

### 快速使用示例

**场景1：小项目，简单需求**
→ 使用 **方式1（完整版）**
```bash
# 从 dist 目录复制（无需安装环境）
cp dist/cursor/single-full/.cursorrules.all /path/to/project/.cursorrules
```

**场景2：大项目，需要 Token 优化**
→ 使用 **方式2（精简版+技能）**
```bash
# 1. 从 dist 目录复制
cp dist/cursor/single-core/.cursorrules.core /path/to/project/.cursorrules

# 2. 安装技能
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/project

# 3. 同步技能
cd /path/to/project
openskills sync -y
```

**场景3：大型/复杂项目，需要精细控制**
→ 使用 **方式3（多文件目录）**
```bash
# Cursor（Markdown 格式）
bash scripts/utils/sync_to_project.sh --platform cursor --mode multi-files /path/to/project

# TRAE（YAML 格式，需要转换）
bash scripts/utils/sync_to_project.sh --platform trae --mode multi-files /path/to/project
```

---

## 六、实施计划

### 阶段1：创建新文档和目录结构

- [ ] 创建 `dist/` 目录结构
- [ ] 更新 `.gitignore` 规则（允许 dist 目录被追踪）
- [ ] 生成初始产物并提交到 Git（方便用户直接使用）
- [ ] 创建 `dist/README.md` 说明文件
- [ ] 创建 `docs/guides/INSTALLATION_AND_TESTING.md`
- [ ] 创建 `docs/guides/USAGE_MANUAL.md`
- [ ] 创建 `docs/guides/QUICK_REFERENCE.md`
- [ ] 创建 `docs/guides/INTRODUCTION.md`（可选，如果需要）

### 阶段2：创建测试脚本和产物生成工具

- [ ] 创建 `scripts/utils/test_environment.sh`
- [ ] 创建 `scripts/utils/test_environment.py`（可选）
- [ ] 创建 `scripts/utils/generate_dist.sh`（产物生成脚本）
  - [ ] 支持生成所有平台的三种方式产物
  - [ ] 支持单独生成某个平台或某种方式
  - [ ] 自动组织到 `dist/` 目录
- [ ] 创建 `scripts/utils/sync_to_project.sh`（同步到项目脚本）
  - [ ] 支持从 `dist/` 目录同步产物到具体项目
  - [ ] 支持三种方式和三个平台
  - [ ] 支持预览模式（dry-run）
  - [ ] 支持交互式选择
- [ ] 测试脚本功能

### 阶段3：重构 README.md

- [ ] 简化项目简介部分
- [ ] 添加环境安装和测试部分
- [ ] 重构使用手册部分（简化，详情跳转）
- [ ] 简化其他部分（项目结构、开发等）

### 阶段4：验证和测试

- [ ] 验证所有链接正确
- [ ] 测试环境测试脚本
- [ ] 测试产物生成脚本（生成所有平台的三种方式产物）
- [ ] 测试同步到项目脚本（验证同步功能）
- [ ] 验证 dist 目录产物可以直接使用（无需安装环境）
- [ ] 测试从 dist 目录同步到项目的完整流程
- [ ] 检查文档完整性
- [ ] 更新 CHANGELOG.md

---

## 七、预期效果

### 改进前

- README.md 内容较长（446 行）
- 使用方式说明分散
- 缺少环境测试
- 详情和概览混在一起
- 用户需要安装环境才能使用

### 改进后

- README.md 简洁清晰（预计 200-250 行）
- 快速选择表格一目了然（三个平台 × 三种方式）
- 环境测试脚本确保环境正确
- 详情跳转到专门文档，结构清晰
- **dist 目录支持 Git 追踪，用户无需安装环境即可使用** ⭐
- 新用户可以快速上手

---

## 📚 相关文档

- [多平台多方式规则使用指南](../guides/multi-platform-rules-guide.md) - 详细的使用指南
- [README.md 重构方案](../README_RESTRUCTURE_PLAN.md) - 重构方案详细说明

---

**最后更新**：2025-12-24（本地时间）

