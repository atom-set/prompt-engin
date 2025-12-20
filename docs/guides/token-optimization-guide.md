# Token 优化指南

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

- [一、Token 问题分析](#一token-问题分析)
- [二、优化策略](#二优化策略)
- [三、规则分类标准](#三规则分类标准)
- [四、使用方式](#四使用方式)
- [五、效果对比](#五效果对比)

---

## 一、Token 问题分析

### 1.1 当前情况

**规则文件大小**：
- `.cursorrules` 文件：**8597 行**（约 **328KB**）
- 所有规则都在初始上下文中，占用大量 token
- 即使不使用某些规则，也会占用 token

**问题影响**：
- ⚠️ 初始上下文 token 占用大
- ⚠️ 每次对话都会加载所有规则
- ⚠️ 无法按需加载特定规则

### 1.2 Token 优化价值

通过将部分规则转换为技能（Skills），可以实现：
- ✅ 初始上下文 token 减少 **约 60%**（从 8597 行减少到 3427 行）
- ✅ 按需加载，只在需要时加载相关技能
- ✅ 灵活配置，用户可以选择使用方式

---

## 二、优化策略

### 2.1 核心思路

**规则分类 + Skill 转换**：
1. **核心规则**：保留在 `.cursorrules` 中（必须全局生效）
2. **可选规则**：转换为技能（按需加载）

### 2.2 优化效果

| 方案 | 初始上下文 | Token 占用 | 节省比例 |
|------|-----------|-----------|---------|
| **当前方案**（完整版） | 8597 行 | ~308KB | - |
| **优化方案**（精简版 + Skill） | ~3427 行 | ~124KB | **约 60%** |

---

## 三、规则分类标准

### 3.1 核心规则判断标准

**核心规则**必须满足以下**所有条件**：
- ✅ 必须全局生效，不能按需加载
- ✅ 影响 AI 助手的基础行为
- ✅ 其他规则可能依赖它
- ✅ 使用频率高

### 3.2 可选规则判断标准

**可选规则**满足以下**任一条件**即可：
- ✅ 可按需加载，不影响核心功能
- ✅ 特定场景使用
- ✅ 可以独立使用

### 3.3 当前项目规则分类

**核心规则（保留在 .cursorrules）**：

| 规则文件 | 行数 | 保留原因 |
|---------|------|---------|
| `mode/tool-permission-system.md` | 556 | 工具权限系统，必须全局生效 |
| `mode/common/mode-common.md` | 465 | 模式通用规则，必须全局生效 |
| `mode/security/security-permissions.md` | 411 | 安全权限规则，必须全局生效 |
| `code/format/code-format.md` | 133 | 代码格式规范，使用频率高 |
| `code/naming/naming.md` | ~100 | 命名规范，使用频率高 |
| `code/function/function-design.md` | 202 | 函数设计规范，使用频率高 |
| `code/comments/comments.md` | 143 | 注释规范，使用频率高 |
| `code/error-handling/strategy.md` | 170 | 错误处理策略，使用频率高 |
| `code/error-handling/logging.md` | ~100 | 错误日志记录，使用频率高 |
| `code/error-handling/message-format.md` | 135 | 错误信息格式，使用频率高 |
| `code/error-handling/return-values.md` | 159 | 返回值规范，使用频率高 |
| `mode/plan/behavior.md` | ~100 | Plan 模式行为规范，必须全局生效 |
| `mode/act/behavior.md` | ~100 | Act 模式行为规范，必须全局生效 |
| `mode/plan/solution-output.md` | 183 | 方案输出机制，必须全局生效 |
| `mode/act/file-write.md` | 403 | 文件写入规则，必须全局生效 |
| **小计** | **~3427 行** | **核心规则**（实际生成约 3427 行，包含分隔线和注释） |

**可选规则（转换为技能）**：

| 规则文件 | 行数 | 转换优先级 | 使用场景 |
|---------|------|-----------|---------|
| `document/document-format.md` | 303 | P0（试点） | 文档输出时加载 |
| `document/time-format.md` | 354 | P1 | 时间处理时加载 |
| `code/organization/code-organization.md` | 202 | P1 | 代码组织时加载 |
| `code/problem-location/problem-location.md` | 647 | P1 | 问题定位时加载 |
| `code/design-principles/design-principles.md` | 264 | P1 | 设计原则时加载 |
| `project/project-clean-principle.md` | 346 | P2 | 项目清理时加载 |
| `documentation/wiki-output.md` | ~300 | P1 | WIKI 文档时加载 |
| `documentation/architecture-diagram-template.md` | ~200 | P2 | 架构图时加载 |
| `documentation/document-generation.md` | ~400 | P1 | 文档生成时加载 |
| `interaction/open-question-confirmation.md` | 364 | P2 | 开放性问题确认时加载 |
| `mode/plan/modular-output.md` | ~100 | P2 | 模块化输出时加载 |
| `mode/plan/exception-handling.md` | ~100 | P2 | 例外情况处理时加载 |
| `mode/plan/compatibility-check.md` | ~100 | P2 | 兼容性确认时加载 |
| `mode/plan/file-reading.md` | ~80 | P2 | 大文件读取时加载 |
| `mode/act/phase-implementation.md` | 223 | P2 | 分阶段实施时加载 |
| `mode/act/time-check.md` | ~150 | P2 | 时间字段检查时加载 |
| **小计** | **~3770 行** | **可选规则** |

---

## 四、使用方式

### 4.1 ⭐ 方式2：精简版规则文件 + 技能系统 ✅ **重点推荐**

**特点**：
- ✅ **Token 占用减少约 60%**（从 8597 行减少到 3427 行）
- ✅ **按需加载**，灵活配置
- ✅ **推荐用于所有项目**，特别是大项目
- ⚠️ 需要 OpenSkills 工具支持

**适用场景**：
- ✅ **所有项目**（推荐优先使用）
- ✅ 大项目，需要 token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

**使用步骤**：

```bash
# 1. 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 2. 复制到项目
cp .cursorrules /path/to/project/

# 3. 安装技能（按需）
cd /path/to/project
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format
# ... 根据需要安装其他技能

# 4. 同步到 AGENTS.md
openskills sync -y
```

---

### 4.2 方式1：完整版规则文件 ✅ **适用于小项目**

**特点**：
- ✅ 简单直接，复制即用
- ✅ 所有规则始终可用
- ⚠️ Token 占用较大（8597 行）

**适用场景**：
- ✅ 小项目，不需要 token 优化
- ✅ 希望所有规则始终可用
- ✅ 不想安装 OpenSkills 工具

**使用步骤**：

```bash
# 1. 生成完整版规则文件
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 2. 复制到项目
cp .cursorrules /path/to/project/
```

### 4.3 两种方式对比

| 特性 | 方式1（完整版） | 方式2（精简版 + Skill） |
|------|---------------|----------------------|
| **Token 占用** | 大（8597 行） | 小（~3356 行） |
| **使用复杂度** | 简单（复制即用） | 中等（需要安装技能） |
| **灵活性** | 低（所有规则始终加载） | 高（按需加载） |
| **适用场景** | 小项目、不需要 token 优化 | 大项目、需要 token 优化 |

---

## 五、效果对比

### 5.1 Token 节省效果

| 指标 | 完整版 | 精简版 + Skill | 节省 |
|------|--------|--------------|------|
| **初始上下文** | 8597 行 | ~3427 行 | **约 60%** |
| **Token 占用** | ~308KB | ~124KB | **约 60%** |
| **按需加载** | 不支持 | 支持 | - |

### 5.2 使用场景对比

**场景1：创建任务清单**

- **完整版**：所有规则都在上下文中，直接应用文档格式规范
- **精简版 + Skill**：AI 自动识别需要文档格式，加载 `document-format` 技能

**场景2：问题定位**

- **完整版**：所有规则都在上下文中，直接应用问题定位规范
- **精简版 + Skill**：AI 自动识别需要问题定位，加载 `problem-location` 技能

**场景3：代码编写**

- **完整版**：所有规则都在上下文中，直接应用代码风格规范
- **精简版 + Skill**：核心规则（代码风格）已在上下文中，直接应用

---

## 六、最佳实践

### 6.1 选择建议

**使用完整版规则文件**：
- ✅ 小项目，不需要 token 优化
- ✅ 希望所有规则始终可用
- ✅ 不想安装 OpenSkills 工具

**使用精简版规则文件 + 技能系统**：
- ✅ 大项目，需要 token 优化
- ✅ 希望按需加载规则
- ✅ 已安装 OpenSkills 工具

### 6.2 迁移建议

**从完整版迁移到精简版 + 技能系统**：

1. **评估需求**：确定项目是否需要 token 优化
2. **安装 OpenSkills**：`npm install -g openskills`
3. **生成精简版规则文件**：`python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules`
4. **安装常用技能**：根据项目需求安装相关技能
5. **测试验证**：验证功能是否正常

---

## 相关文档

- [技能使用指南](./skills-usage-guide.md) - 详细的使用指南
- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法

---

**最后更新**: 2025-12-20（本地时间）
