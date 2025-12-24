# 技能系统使用指南

> **创建时间**: 2025-12-20（本地时间）  
> **文档版本**: v1.0.0  
> **适用对象**: 所有使用 Prompt Engine 的开发者

## 🎯 推荐说明

Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：

- **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
- **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用

> **重要**：两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

**选择建议**：
- **⭐ 所有项目（推荐）** → 使用方式2（精简版规则文件 + 技能系统）
- **小项目或不需要 token 优化** → 使用方式1（完整版规则文件）

## 📑 目录导航

- [一、快速开始](#一快速开始)
- [二、OpenSkills 命令说明](#二openskills-命令说明)
- [三、在具体项目中使用](#三在具体项目中使用)
- [四、安装 prompt-engin 自定义技能](#四安装-prompt-engin-自定义技能)
- [五、两种方式并存](#五两种方式并存)
- [六、同步和更新](#六同步和更新)
- [七、常见问题](#七常见问题)

---

## 一、快速开始

### 1.1 前提条件

**必需环境**：
- Node.js 20.6+（OpenSkills 依赖）
- OpenSkills 已全局安装：`npm i -g openskills`

**验证安装**：

```bash
# 检查 OpenSkills 版本
openskills --version
# 应该显示：1.2.1 或更高版本
```

### 1.2 基本流程

```bash
# 1. 生成精简版规则文件
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 2. 复制到项目
cp .cursorrules /path/to/project/

# 3. 安装技能
cd /path/to/project
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 4. 同步到 AGENTS.md
openskills sync -y
```

---

## 二、OpenSkills 命令说明

### 2.1 核心命令对比

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `openskills install <path>` | **安装技能** | 从本地目录、GitHub 仓库等安装新技能 |
| `openskills sync -y` | **同步已安装的技能** | 将已安装的技能同步到 AGENTS.md，不安装新技能 |
| `openskills list` | **列出已安装的技能** | 查看项目中已安装的所有技能 |
| `openskills read <skill-name>` | **查看技能内容** | 查看特定技能的详细内容 |
| `openskills update` | **更新技能** | 更新从 GitHub 安装的技能 |

### 2.2 重要说明

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

---

## 三、在具体项目中使用

### 3.1 使用流程（精简版规则文件 + 技能系统）

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

# 方式2：从 GitHub 安装（如果 prompt-engin 的技能已发布到 GitHub）
openskills install username/prompt-engin-skills

# 方式3：从 Anthropic 官方技能库安装（如果 prompt-engin 的技能已合并到官方库）
openskills install anthropics/skills
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

### 3.2 使用效果

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

## 四、安装 prompt-engin 自定义技能

### 4.1 安装方式

**方式1：从本地目录安装（推荐）**

```bash
# 假设 prompt-engin 项目在 /path/to/prompt-engin
# 技能存储在 .claude/skills/ 目录中

# 进入具体项目
cd /path/to/your-project

# 安装 prompt-engin 自定义技能
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format

# 同步到 AGENTS.md
openskills sync -y
```

**方式2：从 GitHub 安装（如果技能已发布）**

```bash
# 如果 prompt-engin 的技能已发布到 GitHub
openskills install username/prompt-engin-skills

# 或安装特定技能
openskills install username/prompt-engin-skills/document-format
```

**方式3：批量安装**

```bash
# 安装多个技能
for skill in document-format time-format code-organization; do
  openskills install /path/to/prompt-engin/.claude/skills/$skill
done

# 同步到 AGENTS.md
openskills sync -y
```

### 4.2 验证安装

```bash
# 列出已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format

# 检查技能目录
ls -la .claude/skills/
```

---

## 五、两种方式并存

### 5.1 设计原则

**同时支持两种方式**：
- **方式1**：完整版规则文件（简单直接，复制即用）
- **方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）

### 5.2 实现方案

**方案A：命令行参数控制（推荐）**

```bash
# 生成完整版规则文件（方式1）
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.full

# 生成精简版规则文件（方式2）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# 用户根据需要选择使用哪个文件
cp .cursorrules.full /path/to/project/  # 方式1
# 或
cp .cursorrules.core /path/to/project/  # 方式2
```

**方案B：默认生成两种文件**

```bash
# 同时生成完整版和精简版
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.full
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# 用户根据项目需求选择：
# - 小项目或不需要 token 优化：使用 .cursorrules.full
# - 大项目或需要 token 优化：使用 .cursorrules.core + 技能系统
```

### 5.3 使用建议

**选择完整版规则文件**：
- ✅ 小项目，不需要 token 优化
- ✅ 希望所有规则始终可用
- ✅ 不想安装 OpenSkills 工具

**选择精简版规则文件 + 技能系统**：
- ✅ 大项目，需要 token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

---

## 六、同步和更新

### 6.1 同步策略

**策略1：通过 OpenSkills 自动更新（推荐，适用于 GitHub 技能）**

```bash
# 在具体项目中
cd /path/to/your-project

# 更新所有已安装的技能（适用于从 GitHub 安装的技能）
openskills update

# 或更新特定技能
openskills update document-format
openskills update time-format

# ⚠️ 注意：openskills update 主要用于更新从 GitHub 安装的技能
# 对于从本地目录安装的技能，需要重新安装
```

**策略2：通过 prompt-engin 项目同步（适用于本地技能）**

如果 prompt-engin 项目提供同步脚本：

```bash
# 在 prompt-engin 项目目录
cd /path/to/prompt-engin

# 同步技能到具体项目
python3 scripts/skills_sync/sync_skill.py \
  --project /path/to/your-project \
  --skills document-format time-format code-organization
```

**策略3：手动重新安装（适用于本地技能）**

```bash
# 在具体项目中
cd /path/to/your-project

# 方式1：删除旧技能后重新安装
rm -rf .claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills sync -y

# 方式2：直接重新安装（会覆盖旧版本）
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills sync -y

# 方式3：批量重新安装所有 prompt-engin 技能
for skill in document-format time-format code-organization; do
  openskills install /path/to/prompt-engin/.claude/skills/$skill
done
openskills sync -y
```

### 6.2 版本管理

**方案A：技能版本化**

```bash
# prompt-engin 项目中的技能目录结构
.claude/skills/
├── document-format/
│   ├── v1.0.0/
│   │   └── SKILL.md
│   ├── v1.1.0/
│   │   └── SKILL.md
│   └── latest -> v1.1.0
└── time-format/
    ├── v1.0.0/
    │   └── SKILL.md
    └── latest -> v1.0.0
```

**方案B：通过 Git 管理**

```bash
# 在具体项目中，通过 Git 拉取最新技能
cd /path/to/your-project
git pull origin main  # 如果技能存储在 Git 仓库中

# 或使用 Git Submodule
git submodule update --remote skills/
```

### 6.3 最佳实践

1. **定期更新**：
   - 建议每月检查一次技能更新
   - 使用 `openskills update` 或同步脚本

2. **版本控制**：
   - 在项目的 `package.json` 或配置文件中记录技能版本
   - 使用语义化版本号管理技能版本

3. **测试验证**：
   - 更新技能后，测试相关功能是否正常
   - 检查 AGENTS.md 是否正确更新

4. **回滚机制**：
   - 保留旧版本技能，支持快速回滚
   - 使用 Git 管理技能变更历史

---

## 七、常见问题

### Q1：`openskills sync -y` 可以安装 prompt-engin 自定义的技能吗？

**A1**：不可以。`openskills sync -y` 只同步已安装的技能到 AGENTS.md，不会安装新技能。

**正确流程**：
```bash
# 1. 先安装技能
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 2. 然后同步到 AGENTS.md
openskills sync -y
```

### Q2：如何知道哪些技能需要安装？

**A2**：根据项目需求选择：
- 需要创建文档 → 安装 `document-format`、`time-format`
- 需要问题定位 → 安装 `problem-location`
- 需要代码组织 → 安装 `code-organization`
- 需要 WIKI 文档 → 安装 `wiki-output`

### Q3：可以同时使用完整版和精简版规则文件吗？

**A3**：不建议。应该根据项目需求选择一种方式：
- 小项目或不需要 token 优化 → 使用完整版
- 大项目或需要 token 优化 → 使用精简版 + 技能系统

### Q4：如何更新 prompt-engin 自定义的技能？

**A4**：对于从本地目录安装的技能，需要重新安装：
```bash
# 重新安装技能（会覆盖旧版本）
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills sync -y
```

### Q5：技能安装后在哪里？

**A5**：技能安装在项目的 `.claude/skills/` 目录中：
```bash
# 查看已安装的技能
ls -la .claude/skills/

# 每个技能是一个目录，包含 SKILL.md 文件
.claude/skills/document-format/SKILL.md
```

---

## 相关文档

- [Token 优化指南](./token-optimization-guide.md) - Token 优化详细说明
- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法

---

**最后更新**: 2025-12-20（本地时间）
