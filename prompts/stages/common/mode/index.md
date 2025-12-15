# 模式规则索引

> **文件说明**：本文件提供模式相关规则的索引和导航
> **创建时间**：2025-12-12（本地时间）

---

## 📑 模块列表

### Plan 模式规则

| 模块 | 文件路径 | 说明 |
|------|---------|------|
| 行为规范 | `mode/plan/behavior.md` | Plan 模式基础行为规范 |
| 大文件读取策略 | `mode/plan/file-reading.md` | 大文件读取策略 |
| 工具调用检查 | `mode/plan/tool-check.md` | 工具调用前的统一检查机制 |
| 禁止行为清单 | `mode/plan/forbidden-behaviors.md` | 统一列出所有禁止的行为 |
| 方案输出机制 | `mode/plan/solution-output.md` | 代码修改前的方案输出机制 |
| 方案完整性判断 | `mode/plan/solution-completeness.md` | 方案完整性判断标准 |
| 问题修复处理 | `mode/plan/problem-fix.md` | 问题修复场景的特殊处理 |
| 例外情况处理 | `mode/plan/exception-handling.md` | 例外情况的处理流程 |
| 方案模块化输出 | `mode/plan/modular-output.md` | 完整方案模块化输出策略 |
| 兼容性确认机制 | `mode/plan/compatibility-check.md` | 技术方案调整的兼容性确认机制 |

### Act 模式规则

| 模块 | 文件路径 | 说明 |
|------|---------|------|
| 行为规范 | `mode/act/behavior.md` | Act 模式基础行为规范 |
| 文件写入规则 | `mode/act/file-write.md` | 文件写入规则 |
| 长文本写入检查 | `mode/act/long-text-check.md` | 长文本写入强制检查机制 |
| 时间字段检查 | `mode/act/time-check.md` | 时间字段强制检查机制 |
| 分阶段实施规则 | `mode/act/phase-implementation.md` | 大型工程分阶段实施规则 |

### Debug 模式规则

| 模块 | 文件路径 | 说明 |
|------|---------|------|
| Debug 模式规范 | `mode/debug/debug-mode.md` | Debug 模式完整规则 |

### 模式通用规则

| 模块 | 文件路径 | 说明 |
|------|---------|------|
| 模式通用规则 | `mode/common/mode-common.md` | 模式切换、响应格式等通用规则 |

### 安全权限规则

| 模块 | 文件路径 | 说明 |
|------|---------|------|
| 安全权限规则 | `mode/security/security-permissions.md` | 安全规则和权限规则 |

---

## 🔗 依赖关系

- **Plan 模式** → **模式通用规则**：Plan 模式依赖模式通用规则中的模式切换规则
- **Act 模式** → **模式通用规则**：Act 模式依赖模式通用规则中的模式切换规则
- **Debug 模式** → **模式通用规则**：Debug 模式依赖模式通用规则中的响应格式规则

---

## 📝 扩展指南

### 如何添加新的模式规则

1. **确定规则类型**：
   - 如果是 Plan 模式相关规则，添加到 `mode/plan/` 目录
   - 如果是 Act 模式相关规则，添加到 `mode/act/` 目录
   - 如果是 Debug 模式相关规则，添加到 `mode/debug/` 目录
   - 如果是通用规则，添加到 `mode/common/` 目录

2. **创建规则文件**：
   - 文件命名：使用 kebab-case（如 `new-rule.md`）
   - 文件头：包含文件说明和规则来源注释

3. **更新索引**：
   - 在本文件中添加新模块的说明
   - 更新依赖关系（如果有）

---

## 📖 使用说明

- 所有模式规则都通过合并脚本自动合并到 `.cursorrules` 文件中
- 索引文件（`index.md`）不会被合并，仅用于导航和说明
- 规则文件按字母顺序合并，索引文件优先合并

