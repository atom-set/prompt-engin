# 使用手册

> **创建时间**：2025-12-24（本地时间）  
> **最后更新**：2025-12-24（本地时间）

---

## 概述

本手册提供 Prompt Engine 的详细使用指南，包括三种使用方式（单文件完整版、单文件精简版+技能、多文件目录）和三个平台（Cursor、TRAE、Antigravity）的完整使用说明。

---

## 📑 目录导航

- [一、快速选择指南](#一快速选择指南)
- [二、方式1：单文件完整版](#二方式1单文件完整版)
- [三、方式2：单文件精简版 + 技能系统](#三方式2单文件精简版--技能系统)
- [四、方式3：多文件目录](#四方式3多文件目录)
- [五、平台支持说明](#五平台支持说明)
- [六、常见问题](#六常见问题)

---

## 一、快速选择指南

### 使用方式对比

| 使用方式 | 特点 | Token 占用 | 适用场景 | 推荐度 |
|---------|------|-----------|---------|--------|
| **方式1：单文件完整版** | 简单直接，所有规则在一个文件 | 高（8597 行） | 小项目 | ⭐⭐⭐ |
| **方式2：单文件精简版 + 技能** | Token 优化，按需加载 | 低（3427 行 + 按需） | 大项目 | ⭐⭐⭐⭐⭐ |
| **方式3：多文件目录** | 精细控制，路径特定配置 | 中等（按需加载） | 大型/复杂项目 | ⭐⭐⭐⭐ |

### 平台支持情况

| 平台 | 单文件方式 | 多文件目录 | 状态 |
|------|----------|-----------|------|
| **[Cursor IDE](https://cursor.sh/)** | `.cursorrules` | `.cursor/rules/` | ✅ 完全支持 |
| **[TRAE IDE](https://traeide.ai-kit.cn/)** | `.traerules` | `.trae/ai-rules.yml` | ✅ 支持（YAML 格式） |
| **[Antigravity IDE](https://antigravity.dev/)** | `.antigravityrules` | `.agent` (代理配置) | ✅ 单文件支持 |

### 快速选择建议

- **小项目** → [方式1：单文件完整版](#二方式1单文件完整版)
- **大项目** → [方式2：单文件精简版 + 技能系统](#三方式2单文件精简版--技能系统) ⭐ **推荐**
- **大型/复杂项目** → [方式3：多文件目录](#四方式3多文件目录)

---

## 二、方式1：单文件完整版

### 适用场景

- 小项目，不需要 Token 优化
- 需要所有规则支持
- 希望简单直接的使用方式

### Cursor IDE

#### 步骤1：生成规则文件

```bash
# 从 dist 目录复制（推荐，无需安装环境）
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules

# 或使用脚本生成
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules
cp .cursorrules /path/to/your-project/
```

#### 步骤2：在项目中使用

在 Cursor IDE 中打开项目，规则文件会自动加载。

**快速引用**：
- 使用 `@.cursorrules` 引用全部规则

### TRAE IDE

#### 步骤1：生成规则文件

```bash
# 从 dist 目录复制（推荐）
cp dist/trae/single-full/.traerules.all /path/to/your-project/.traerules

# 或使用脚本生成
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --all --ide trae --output .traerules
cp .traerules /path/to/your-project/
```

#### 步骤2：在项目中使用

在 TRAE IDE 中打开项目，规则文件会自动加载。

### Antigravity IDE

#### 步骤1：生成规则文件

```bash
# 从 dist 目录复制（推荐）
cp dist/antigravity/single-full/.antigravityrules.all /path/to/your-project/.antigravityrules

# 或使用脚本生成
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --all --ide antigravity --output .antigravityrules
cp .antigravityrules /path/to/your-project/
```

#### 步骤2：在项目中使用

在 Antigravity IDE 中打开项目，规则文件会自动加载。

---

## 三、方式2：单文件精简版 + 技能系统

### 适用场景

- 大项目，需要 Token 优化
- 需要按需加载规则
- 希望灵活配置

### 优势

- ✅ Token 占用减少约 60%（从 8597 行减少到 3427 行）
- ✅ 按需加载，灵活配置
- ✅ 推荐用于所有项目，特别是大项目

### Cursor IDE

#### 步骤1：生成精简版规则文件

```bash
# 从 dist 目录复制（推荐）
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 或使用脚本生成
cd /path/to/prompt-engin
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules
cp .cursorrules /path/to/your-project/
```

#### 步骤2：安装技能（批量安装，推荐）

```bash
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

#### 步骤3：同步技能到 AGENTS.md

```bash
cd /path/to/your-project
openskills sync -y
```

#### 步骤4：在项目中使用

在 Cursor IDE 中打开项目，规则文件和技能会自动加载。

**快速引用**：
- 使用 `@.cursorrules` 引用核心规则
- 使用 `@技能名称` 引用特定技能

### TRAE IDE

TRAE IDE 的技能系统支持方式与 Cursor 类似，但需要转换为 YAML 格式。

### Antigravity IDE

Antigravity IDE 目前主要支持单文件方式，技能系统支持待确认。

---

## 四、方式3：多文件目录

### 适用场景

- 大型/复杂项目，需要路径特定配置
- 需要精细控制规则加载
- 需要模块化的规则组织

### Cursor IDE

#### 步骤1：生成 multi-files 模式的产物

```bash
cd /path/to/prompt-engin
bash scripts/utils/generate_dist.sh --platform cursor --mode multi-files
```

#### 步骤2：同步到项目

```bash
# 使用同步脚本（推荐）
bash scripts/utils/sync_to_project.sh --platform cursor --mode multi-files /path/to/your-project

# 或手动复制
cp -r dist/cursor/multi-files/rules /path/to/your-project/.cursor/
```

#### 步骤3：在项目中使用

在 Cursor IDE 中打开项目，`.cursor/rules/` 目录中的规则文件会自动加载。

**目录结构**：
```
.cursor/
└── rules/
    ├── common/
    │   ├── code/
    │   ├── document/
    │   └── mode/
    ├── requirements/
    ├── design/
    └── ...
```

### TRAE IDE

#### 步骤1：生成 multi-files 模式的产物

```bash
cd /path/to/prompt-engin
bash scripts/utils/generate_dist.sh --platform trae --mode multi-files
```

#### 步骤2：同步到项目

```bash
# 使用同步脚本（推荐）
bash scripts/utils/sync_to_project.sh --platform trae --mode multi-files /path/to/your-project

# 或手动复制
cp -r dist/trae/multi-files/.trae /path/to/your-project/
```

#### 步骤3：在项目中使用

在 TRAE IDE 中打开项目，`.trae/ai-rules.yml` 文件会自动加载。

**注意**：TRAE 使用 YAML 格式，需要将 Markdown 规则转换为 YAML 格式。

### Antigravity IDE

Antigravity IDE 的多文件规则支持待确认，目前主要支持单文件方式。

---

## 五、平台支持说明

### Cursor IDE

- **单文件方式**：`.cursorrules` 文件
- **多文件目录**：`.cursor/rules/` 目录（Markdown 格式）
- **技能系统**：完全支持
- **快速引用**：`@.cursorrules`、`@.cursorrules.all`、`@.cursorrules.core`

### TRAE IDE

- **单文件方式**：`.traerules` 文件
- **多文件目录**：`.trae/ai-rules.yml`（YAML 格式）
- **技能系统**：支持（需要转换为 YAML）
- **快速引用**：根据 TRAE IDE 的引用方式

### Antigravity IDE

- **单文件方式**：`.antigravityrules` 文件
- **多文件目录**：待确认
- **技能系统**：待确认
- **快速引用**：根据 Antigravity IDE 的引用方式

---

## 六、常见问题

### Q1：如何选择使用方式？

**A1**：根据项目规模和需求选择：
- **小项目**：使用方式1（单文件完整版）
- **大项目**：使用方式2（单文件精简版+技能）⭐ **推荐**
- **大型/复杂项目**：使用方式3（多文件目录）

### Q2：如何从 dist 目录直接使用？

**A2**：dist 目录中的产物可以直接使用，无需安装环境：

```bash
# 直接复制产物文件
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules
```

### Q3：如何更新规则文件？

**A3**：更新规则文件的方法：

1. **从 dist 目录更新**（推荐）：
   ```bash
   cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules
   ```

2. **使用同步脚本更新**：
   ```bash
   bash scripts/utils/sync_to_project.sh --platform cursor --mode single-full /path/to/your-project
   ```

3. **重新生成并复制**：
   ```bash
   cd /path/to/prompt-engin
   python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules
   cp .cursorrules /path/to/your-project/
   ```

### Q4：多文件模式需要先生成产物吗？

**A4**：是的，使用 multi-files 模式前，必须先运行 `generate_dist.sh` 生成产物：

```bash
bash scripts/utils/generate_dist.sh --platform cursor --mode multi-files
```

### Q5：如何验证规则文件是否正确？

**A5**：使用验证脚本：

```bash
# 验证提示词文件格式
bash scripts/utils/validate_prompts.sh

# 验证 CLI 工具
python3 scripts/prompt-engine validate prompts/
```

---

## 相关文档

- [环境安装和测试指南](./INSTALLATION_AND_TESTING.md) - 环境配置指南
- [快速参考](./QUICK_REFERENCE.md) - 常用命令速查
- [V2 版本改进计划](../milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md) - 详细改进计划
- [README.md](../../README.md) - 项目主文档

---

**最后更新**：2025-12-24（本地时间）

