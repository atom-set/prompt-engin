# README.md 重构方案

> ⚠️ **已整合**：本文档内容已整合到 [V2 版本改进计划](./milestones/V2_IMPROVEMENT/V2_IMPROVEMENT_PLAN.md)，建议查看合并后的文档。
> 
> **文件说明**：README.md 重构方案设计文档（历史文档，保留供参考）
> **创建时间**：2025-12-23
> **整合时间**：2025-12-24

---

## 📋 重构目标

将 README.md 重新组织为更清晰的结构，分为四个主要部分：
1. **简单介绍**：只保留核心信息，详情跳转到专门文档
2. **环境安装和测试**：包含环境检查和测试脚本
3. **三种方式和三个 IDE 使用手册**：详细的使用指南
4. **其他**：项目结构、贡献、许可证等

---

## 📐 新结构设计

### 项目目录结构（新增 dist 目录）

```
prompt-engin/
├── dist/                    # 产物目录（新增）
│   ├── cursor/             # Cursor IDE 产物
│   │   ├── single-full/    # 方式1：单文件完整版
│   │   ├── single-core/    # 方式2：单文件精简版
│   │   └── multi-files/    # 方式3：多文件目录
│   ├── trae/               # TRAE IDE 产物
│   │   ├── single-full/
│   │   ├── single-core/
│   │   └── multi-files/
│   └── antigravity/        # Antigravity IDE 产物
│       ├── single-full/
│       ├── single-core/
│       └── multi-files/
├── src/
├── prompts/
├── scripts/
│   └── utils/
│       ├── generate_dist.sh        # 产物生成脚本（新增）
│       ├── sync_to_project.sh     # 同步到项目脚本（新增）
│       └── test_environment.sh    # 环境测试脚本（新增）
└── docs/
```

### README.md 新结构

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

---

## 📄 需要创建的新文档

### 1. 环境安装和测试文档

**文件**：`docs/guides/INSTALLATION_AND_TESTING.md`

**内容**：
- 系统要求（Python 版本、操作系统等）
- 安装步骤（详细说明）
- 环境测试脚本（`scripts/utils/test_environment.sh`）
- 环境验证检查清单
- 常见安装问题排查

### 2. 使用手册（三种方式 × 三个平台）

**文件**：`docs/guides/USAGE_MANUAL.md`

**内容**：
- 三种使用方式详细说明
- 三个平台（Cursor、TRAE、Antigravity）支持情况
- 每种方式的完整使用步骤
- 平台特定的配置说明
- 使用示例和最佳实践

### 3. 快速参考卡片

**文件**：`docs/guides/QUICK_REFERENCE.md`

**内容**：
- 常用命令速查表
- 三种方式对比表
- 三个平台对比表
- 快速选择决策树

---

## 📦 产物目录设计（dist）

### dist 目录结构

**目的**：统一存放生成的规则文件产物，方便分发和同步到具体项目

**目录结构**：
```
dist/
├── cursor/
│   ├── single-full/
│   │   └── .cursorrules.all          # 完整版规则文件
│   ├── single-core/
│   │   └── .cursorrules.core         # 精简版规则文件
│   └── multi-files/
│       └── rules/                    # 多文件目录
│           ├── 001-common.mdc
│           ├── 002-code.mdc
│           └── ...
├── trae/
│   ├── single-full/
│   │   └── .traerules.all            # 完整版规则文件
│   ├── single-core/
│   │   └── .traerules.core           # 精简版规则文件
│   └── multi-files/
│       └── .trae/                    # 多文件目录
│           ├── ai-rules.yml
│           └── team-rules.yml
└── antigravity/
    ├── single-full/
    │   └── .antigravityrules.all      # 完整版规则文件
    ├── single-core/
    │   └── .antigravityrules.core     # 精简版规则文件
    └── multi-files/
        └── *.agent                   # Agent 配置文件（如果支持）
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

### 产物命名规范

**单文件方式**：
- 完整版：`.{platform}rules.all`（如 `.cursorrules.all`）
- 精简版：`.{platform}rules.core`（如 `.cursorrules.core`）

**多文件目录方式**：
- Cursor：`rules/` 目录，包含 `.mdc` 文件
- TRAE：`.trae/` 目录，包含 `.yml` 文件
- Antigravity：`*.agent` 文件（如果支持）

### dist 目录管理

**Git 管理策略**：
- `dist/` 目录中的生成文件应添加到 `.gitignore`
- 保留 `dist/README.md` 说明文件（可选）
- 可以添加 `dist/.gitkeep` 保持目录结构

**更新策略**：
- 产物文件由脚本自动生成，不手动编辑
- 每次生成前清理旧文件
- 支持增量生成（只生成变更的部分）

### 产物生成流程

```bash
# 1. 生成所有产物
bash scripts/utils/generate_dist.sh --all

# 2. 同步到项目（方式1：单文件完整版）
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules

# 3. 同步到项目（方式2：单文件精简版）
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 4. 同步到项目（方式3：多文件目录）
cp -r dist/cursor/multi-files/rules /path/to/your-project/.cursor/

# 或使用同步脚本（推荐）
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode single-core \
  /path/to/your-project
```

---

## 🔧 需要创建的工具

### 1. 环境测试脚本

**文件**：`scripts/utils/test_environment.sh`

**功能**：
- 检查 Python 版本
- 检查依赖包是否安装
- 检查 CLI 工具是否可用
- 测试基本功能（list、validate 等）
- 输出测试报告

**使用方式**：
```bash
bash scripts/utils/test_environment.sh
```

### 2. Python 环境测试脚本（可选）

**文件**：`scripts/utils/test_environment.py`

**功能**：
- 更详细的测试
- 生成测试报告
- 提供修复建议

### 3. 产物生成脚本

**文件**：`scripts/utils/generate_dist.sh`

**功能**：
- 生成所有平台的三种方式产物
- 自动组织到 `dist/` 目录
- 支持单独生成某个平台或某种方式

### 4. 同步到项目脚本

**文件**：`scripts/utils/sync_to_project.sh`

**功能**：
- 从 `dist/` 目录同步产物到具体项目
- 支持三种方式和三个平台
- 支持预览模式（dry-run）

---

## 📝 README.md 新内容设计

### 第一部分：项目简介（简洁版）

```markdown
## 📋 简介

**Prompt Engine** 是一个**提示词（Prompt）**结构化工程，帮助开发者更好地组织、管理和复用提示词。

**核心特性**：
- 📝 结构化组织提示词（按阶段和类型）
- 🔄 支持版本管理和批量处理
- 🎨 提供可复用的提示词模板
- 🔧 提供 CLI 工具
- 📚 支持多个 IDE 平台（Cursor、TRAE、Antigravity）

> 📖 **详细说明**：查看 [完整介绍文档](./docs/guides/INTRODUCTION.md)

**快速开始**：
1. [环境安装和测试](#环境安装和测试) - 确保环境正确
2. [使用手册](#使用手册) - 选择适合的使用方式
3. [快速参考](./docs/guides/QUICK_REFERENCE.md) - 常用命令速查
```

### 第二部分：环境安装和测试

```markdown
## 🔧 环境安装和测试

### 系统要求

- Python 3.8+
- 操作系统：macOS、Linux、Windows

### 安装步骤

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin

# 2. 安装依赖
pip install -r requirements.txt

# 3. 安装到系统（可选）
pip install -e .
```

### 环境测试

运行环境测试脚本，检查环境是否正确配置：

```bash
# 测试环境
bash scripts/utils/test_environment.sh

# 或使用 Python 脚本（更详细）
python3 scripts/utils/test_environment.py
```

**测试内容**：
- ✅ Python 版本检查
- ✅ 依赖包检查
- ✅ CLI 工具可用性检查
- ✅ 基本功能测试

> 📖 **详细说明**：查看 [环境安装和测试指南](./docs/guides/INSTALLATION_AND_TESTING.md)
```

### 第三部分：使用手册

```markdown
## 📖 使用手册

### 三种使用方式快速选择

| 使用方式 | 特点 | Token 占用 | 适用场景 | 推荐度 |
|---------|------|-----------|---------|--------|
| **方式1：单文件完整版** | 简单直接 | 高（8597 行） | 小项目 | ⭐⭐⭐ |
| **方式2：单文件精简版 + 技能** | Token 优化 | 低（3427 行 + 按需） | 大项目 | ⭐⭐⭐⭐⭐ |
| **方式3：多文件目录** | 精细控制 | 中等（按需） | 大型/复杂项目 | ⭐⭐⭐⭐ |

> 💡 **快速选择**：
> - **小项目** → [方式1：单文件完整版](./docs/guides/USAGE_MANUAL.md#方式1单文件完整版)
> - **大项目** → [方式2：单文件精简版 + 技能](./docs/guides/USAGE_MANUAL.md#方式2单文件精简版--技能系统) ⭐ **推荐**
> - **大型/复杂项目** → [方式3：多文件目录](./docs/guides/USAGE_MANUAL.md#方式3多文件目录)

### 三个平台支持

| 平台 | 单文件方式 | 多文件目录 | 状态 |
|------|----------|-----------|------|
| **[Cursor IDE](https://cursor.sh/)** | `.cursorrules` | `.cursor/rules/` | ✅ 完全支持 |
| **[TRAE IDE](https://traeide.ai-kit.cn/)** | `.traerules` | `.trae/ai-rules.yml` | ✅ 支持 |
| **[Antigravity IDE](https://antigravity.dev/)** | `.antigravityrules` | `.agent` (代理配置) | ✅ 单文件支持 |

> 📖 **详细说明**：查看 [完整使用手册](./docs/guides/USAGE_MANUAL.md) 和 [多平台多方式规则使用指南](./docs/guides/multi-platform-rules-guide.md)

### 快速使用示例

**方式1：单文件完整版（最简单）**
```bash
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules
cp .cursorrules /path/to/your-project/
```

**方式2：单文件精简版 + 技能（推荐）**
```bash
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules
cp .cursorrules /path/to/your-project/
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

> 📖 **详细步骤**：查看 [使用手册](./docs/guides/USAGE_MANUAL.md)
```

### 第四部分：其他

```markdown
## 📁 项目结构

```
prompt-engin/
├── src/prompt_engine/    # 核心代码模块
├── prompts/              # 提示词模板目录
├── scripts/              # 工具脚本
├── docs/                 # 文档目录
└── tests/                # 测试目录
```

> 📖 **详细说明**：查看 [项目结构文档](./docs/PROJECT_STRUCTURE.md)

## 🛠️ 开发

- [运行测试](./docs/guides/DEVELOPMENT.md#运行测试)
- [代码质量检查](./docs/guides/DEVELOPMENT.md#代码质量检查)
- [贡献指南](./CONTRIBUTING.md)

## 📚 相关资源

- [快速参考](./docs/guides/QUICK_REFERENCE.md) - 常用命令速查
- [API 文档](./docs/api/README.md)
- [示例项目](./examples/README.md)
- [完整文档索引](./docs/README.md)
```

---

## 📋 实施计划

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

## 🎯 预期效果

### 改进前

- README.md 内容较长（446 行）
- 使用方式说明分散
- 缺少环境测试
- 详情和概览混在一起

### 改进后

- README.md 简洁清晰（预计 200-250 行）
- 快速选择表格一目了然
- 环境测试脚本确保环境正确
- 详情跳转到专门文档，结构清晰
- 新用户可以快速上手

---

## 📝 补充建议

### 1. 创建快速开始流程图

**文件**：`docs/guides/QUICK_START_FLOW.md`

**内容**：
- 决策流程图（Mermaid）
- 根据项目类型选择使用方式
- 根据 IDE 平台选择配置方式

### 2. 创建常见问题 FAQ

**文件**：`docs/guides/FAQ.md`

**内容**：
- 安装问题
- 使用问题
- 平台特定问题
- 故障排查

### 3. 创建视频教程（可选）

**文件**：`docs/guides/VIDEO_TUTORIALS.md`

**内容**：
- 安装教程链接
- 使用方式演示链接
- 平台配置演示链接

### 4. 创建迁移指南

**文件**：`docs/guides/MIGRATION_GUIDE.md`

**内容**：
- 从方式1迁移到方式2
- 从方式2迁移到方式3
- 从旧版本迁移到新版本

---

## ✅ 检查清单

实施前检查：
- [ ] 确认新文档结构合理
- [ ] 确认测试脚本功能完整
- [ ] 确认所有链接正确
- [ ] 确认向后兼容性

实施后检查：
- [ ] README.md 简洁清晰
- [ ] 所有链接可访问
- [ ] 环境测试脚本可用
- [ ] 用户反馈良好

---

## 📦 dist 目录详细设计

### 目录结构

```
dist/
├── README.md                    # 产物说明文档
├── .gitkeep                     # 保持目录结构（可选）
├── cursor/                      # Cursor IDE 产物
│   ├── single-full/
│   │   └── .cursorrules.all     # 完整版规则文件（8597 行）
│   ├── single-core/
│   │   └── .cursorrules.core    # 精简版规则文件（3427 行）
│   └── multi-files/
│       └── rules/               # 多文件目录
│           ├── 001-common.mdc
│           ├── 002-code.mdc
│           ├── 003-mode.mdc
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

### 产物生成脚本详细设计

**文件**：`scripts/utils/generate_dist.sh`

**功能**：
1. **生成单文件产物**：
   ```bash
   # 完整版
   python3 scripts/prompt-engine merge --all --ide cursor --output dist/cursor/single-full/.cursorrules.all
   python3 scripts/prompt-engine merge --all --ide trae --output dist/trae/single-full/.traerules.all
   python3 scripts/prompt-engine merge --all --ide antigravity --output dist/antigravity/single-full/.antigravityrules.all
   
   # 精简版
   python3 scripts/prompt-engine merge --core-only --ide cursor --output dist/cursor/single-core/.cursorrules.core
   python3 scripts/prompt-engine merge --core-only --ide trae --output dist/trae/single-core/.traerules.core
   python3 scripts/prompt-engine merge --core-only --ide antigravity --output dist/antigravity/single-core/.antigravityrules.core
   ```

2. **生成多文件目录产物**：
   - Cursor：需要将规则文件拆分并组织到 `rules/` 目录（`.mdc` 格式）
   - TRAE：需要转换为 YAML 格式，组织到 `.trae/` 目录
   - Antigravity：生成 `.agent` 文件（如果支持）

3. **清理和验证**：
   - 清理旧产物（可选）
   - 验证生成的文件
   - 生成产物清单

**脚本参数**：
```bash
--all              # 生成所有平台的三种方式产物
--platform PLATFORM # 生成特定平台的产物（cursor/trae/antigravity）
--mode MODE        # 生成特定方式的产物（single-full/single-core/multi-files）
--clean            # 生成前清理旧产物
--verify           # 生成后验证产物
```

### 同步到项目脚本详细设计

**文件**：`scripts/utils/sync_to_project.sh`

**功能**：
1. **交互式选择**：
   ```bash
   bash scripts/utils/sync_to_project.sh /path/to/your-project
   # 提示：
   # 1. 选择平台（cursor/trae/antigravity）
   # 2. 选择方式（single-full/single-core/multi-files）
   # 3. 确认同步
   ```

2. **指定参数同步**：
   ```bash
   bash scripts/utils/sync_to_project.sh \
     --platform cursor \
     --mode single-core \
     /path/to/your-project
   ```

3. **同步操作流程**：
   - 检查目标项目目录是否存在
   - 检查产物文件是否存在
   - 备份现有文件（如果存在）
   - 执行同步操作
   - 输出同步结果

**同步规则**：

**方式1：单文件完整版**
```bash
# Cursor
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules

# TRAE
cp dist/trae/single-full/.traerules.all /path/to/your-project/.traerules

# Antigravity
cp dist/antigravity/single-full/.antigravityrules.all /path/to/your-project/.antigravityrules
```

**方式2：单文件精简版**
```bash
# Cursor
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# TRAE
cp dist/trae/single-core/.traerules.core /path/to/your-project/.traerules

# Antigravity
cp dist/antigravity/single-core/.antigravityrules.core /path/to/your-project/.antigravityrules
```

**方式3：多文件目录**
```bash
# Cursor
cp -r dist/cursor/multi-files/rules /path/to/your-project/.cursor/

# TRAE
cp -r dist/trae/multi-files/.trae /path/to/your-project/

# Antigravity
cp dist/antigravity/multi-files/*.agent /path/to/your-project/
```

### 使用示例

**示例1：生成所有产物并同步到项目**

```bash
# 1. 生成所有产物
bash scripts/utils/generate_dist.sh --all

# 2. 同步到项目（方式2：单文件精简版）
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode single-core \
  /path/to/your-project

# 3. 安装技能（如果需要）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

**示例2：手动复制（简单场景）**

```bash
# 1. 生成产物
bash scripts/utils/generate_dist.sh --platform cursor --mode single-full

# 2. 手动复制
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules
```

**示例3：批量同步多个项目**

```bash
# 生成产物
bash scripts/utils/generate_dist.sh --all

# 批量同步到多个项目
for project in /path/to/project1 /path/to/project2 /path/to/project3; do
  bash scripts/utils/sync_to_project.sh \
    --platform cursor \
    --mode single-core \
    "$project"
done
```

### Git 管理策略

**`.gitignore` 配置**：
```gitignore
# Distribution files (dist/) - 允许追踪，用户可直接使用
# dist/ 目录中的产物文件应该提交到 Git，方便用户直接使用
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

**更新策略**：
- 每次发布新版本时，更新 `dist/` 目录中的产物
- 产物文件与代码版本同步提交
- 可以通过 CI/CD 自动生成和提交产物

### 产物更新策略

**自动更新**：
- 每次运行 `generate_dist.sh` 时自动更新产物
- 支持增量生成（只生成变更的部分）
- 支持清理旧产物（`--clean` 选项）

**版本管理**：
- ✅ **提交到 Git**：产物文件提交到 Git，与代码版本同步
- ✅ **版本同步**：每次代码更新时，同步更新产物文件
- ✅ **CI/CD 集成**：可以通过 CI/CD 自动生成和提交产物
- ✅ **标签发布**：可以通过 Git 标签标记产物版本

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

**最后更新**：2025-12-23

