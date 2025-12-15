# 提示词规则验证项目

> **文档说明**：本目录包含提示词规则验证的完整方案和工具
> **创建时间**：2025-12-15（本地时间）

---

## 📋 目录

本目录包含以下文档：

1. **快速开始指南** (`quick-start.md`)
   - 5 分钟快速上手验证
   - 包含第一个验证示例

2. **完整验证指南** (`rule-validation-guide.md`)
   - 详细的验证方案和说明
   - 包含所有验证场景和预期行为
   - 包含验证结果记录表

3. **提问词集合** (`prompts-collection.md`)
   - 所有验证提问词，可直接复制使用
   - 包含验证要点说明
   - 包含快速记录表

---

## 🎯 验证目标

通过实际项目（待办事项管理 CLI 工具）验证系统提示词规则的效果，包括：

- ✅ **模式规则**：Plan/Act/Debug 模式的行为规范
- ✅ **代码规范**：命名、函数设计、错误处理、问题定位等
- ✅ **文档规范**：时间格式、文档格式、禁止 QA 等
- ✅ **交互规范**：开放性问题确认、兼容性确认等
- ✅ **Act 规则**：文件写入、长文本检查、分阶段实施等

---

## 🚀 快速开始

### 第一步：创建测试项目

```bash
mkdir todo-cli-validation
cd todo-cli-validation
cp /path/to/prompt-engin/.cursorrules .
```

### 第二步：打开项目

在 Cursor 中打开 `todo-cli-validation` 目录。

### 第三步：执行验证

按照 `quick-start.md` 或 `prompts-collection.md` 中的提问词，向 AI 提问并验证规则效果。

---

## 📖 使用建议

1. **首次使用**：先阅读 `quick-start.md`，快速了解验证流程
2. **完整验证**：参考 `rule-validation-guide.md`，执行完整的验证流程
3. **直接使用**：从 `prompts-collection.md` 复制提问词，直接开始验证

---

## 📊 验证结果

验证完成后，请填写验证结果记录表（见 `rule-validation-guide.md` 或 `prompts-collection.md`），记录：

- 哪些规则生效 ✅
- 哪些规则未生效 ❌
- 需要改进的地方 ⚠️

---

## 🔗 相关文档

- [项目 README](../../README.md)
- [提示词概述](../../PROMPTS_OVERVIEW.md)
- [使用指南](../guides/user-guide.md)

---

**最后更新**：2025-12-15（本地时间）

