# 提示词优化和整合方案

> **创建时间**：2025-12-16（本地时间）
> **完成时间**：2025-12-19（本地时间）
> **目的**：分析提示词目录，提出优化和整合建议
> **状态**：✅ 已完成

---

## 📋 优化建议汇总

### ✅ 建议整合的内容

#### 1. 文件写入规则整合（高优先级）

**现状**：
- `mode/act/file-write.md` - 文件写入规则（框架优先策略）
- `mode/act/long-text-check.md` - 长文本写入检查（大小检查机制）

**问题**：
- 两个文件都是关于文件写入的，内容有重叠
- `file-write.md` 强调"框架优先"策略
- `long-text-check.md` 强调"大小检查"机制
- 实际使用中需要同时参考两个文件

**优化方案**：
- **方案A（推荐）**：将 `long-text-check.md` 的内容整合到 `file-write.md` 中
  - 在 `file-write.md` 中添加"文件大小检查"章节
  - 将大小检查作为写入前的第一步检查
  - 删除 `long-text-check.md` 文件
  - 更新 `mode/act/index.md` 索引

- **方案B**：保持两个文件，但明确职责边界
  - `file-write.md`：文件写入策略和流程
  - `long-text-check.md`：文件大小检查机制（作为 `file-write.md` 的补充）

**推荐**：方案A，因为大小检查是文件写入流程的一部分，整合后更完整。

---

#### 2. 时间相关规则优化（中优先级）

**现状**：
- `document/time-format.md` - 时间格式规范（通用规范）
- `mode/act/time-check.md` - 时间字段检查（Act 模式检查流程）

**问题**：
- 两个文件有部分重复内容（禁止假设时间、获取时间方法等）
- `time-check.md` 更侧重于 Act 模式下的检查流程
- `time-format.md` 是通用的时间格式规范

**优化方案**：
- **方案A（推荐）**：在 `time-check.md` 中引用 `time-format.md`
  - 在 `time-check.md` 开头添加："时间格式要求请参考 `document/time-format.md`"
  - 保留 `time-check.md` 中的检查流程部分
  - 删除重复的禁止清单和获取方法说明

- **方案B**：保持现状，但明确职责边界
  - `time-format.md`：通用时间格式规范（所有场景）
  - `time-check.md`：Act 模式下的时间检查流程（特定场景）

**推荐**：方案A，减少重复，保持引用关系。

---

#### 3. 文档阶段规范说明（低优先级）

**现状**：
- `documentation/document-generation.md` - 文档生成规范（整合版）
- `documentation/architecture-diagram-template.md` - 架构图文档模板规范
- `documentation/wiki-output.md` - WIKI 输出规范

**问题**：
- `document-generation.md` 已经整合了架构图和 WIKI 的规范
- 但 `architecture-diagram-template.md` 和 `wiki-output.md` 仍然存在
- 用户可能不知道应该使用哪个文件

**优化方案**：
- **方案A（推荐）**：在 `documentation/README.md` 中明确说明
  - 说明 `document-generation.md` 是整合版，推荐优先使用
  - 说明 `architecture-diagram-template.md` 和 `wiki-output.md` 作为快速参考保留
  - 在 `document-generation.md` 开头添加说明，引用这两个文件作为详细参考

- **方案B**：删除 `architecture-diagram-template.md` 和 `wiki-output.md`
  - 所有内容都整合到 `document-generation.md` 中
  - 风险：如果用户需要快速查看特定文档类型的规范，需要查找整合文件

**推荐**：方案A，保留快速参考文件，但明确主次关系。

---

### ⚠️ 不建议整合的内容

#### 1. 错误处理规范（保持现状）

**现状**：
- `code/error-handling/strategy.md` - 错误处理策略
- `code/error-handling/logging.md` - 错误日志记录
- `code/error-handling/message-format.md` - 错误信息格式
- `code/error-handling/return-values.md` - 返回值规范

**分析**：
- 虽然都是错误处理相关，但每个文件职责单一明确
- 文件大小适中（每个文件 100-200 行）
- 符合功能单一原则
- 便于独立维护和扩展

**建议**：保持现状，不整合。

---

#### 2. 代码规范各模块（保持现状）

**现状**：
- `code/naming/` - 命名规范
- `code/function/` - 函数设计规范
- `code/format/` - 代码格式规范
- `code/comments/` - 注释规范
- `code/organization/` - 代码组织规范
- `code/error-handling/` - 错误处理规范
- `code/problem-location/` - 问题定位规范

**分析**：
- 每个模块职责单一，边界清晰
- 文件大小适中
- 符合模块化原则

**建议**：保持现状，不整合。

---

## 📝 实施计划

### ✅ 阶段1：文件写入规则整合（高优先级）- 已完成

1. ✅ **整合 `long-text-check.md` 到 `file-write.md`**
   - ✅ 在 `file-write.md` 中添加"文件大小检查"章节
   - ✅ 将大小检查作为写入前的第一步
   - ✅ 整合检查流程和判断标准
   - ✅ 整合常见错误和纠正示例

2. ✅ **更新索引文件**
   - ✅ 更新 `mode/act/index.md`，移除 `long-text-check.md` 的引用
   - ✅ 更新依赖关系说明

3. ✅ **删除文件**
   - ✅ 删除 `mode/act/long-text-check.md`

### ✅ 阶段2：时间相关规则优化（中优先级）- 已完成

1. ✅ **优化 `time-check.md`**
   - ✅ 在开头添加对 `time-format.md` 的引用
   - ✅ 删除重复的禁止清单和获取方法说明
   - ✅ 保留检查流程部分
   - ✅ 明确说明本文件仅包含 Act 模式下的检查流程

2. ✅ **更新文档**
   - ✅ 更新文件说明，明确引用关系

### ✅ 阶段3：文档阶段规范说明（低优先级）- 已完成

1. ✅ **更新 `documentation/README.md`**
   - ✅ 明确说明 `document-generation.md` 是整合版，推荐优先使用
   - ✅ 说明其他两个文件作为快速参考保留
   - ✅ 添加推荐度标识（⭐⭐⭐/⭐⭐）

2. ✅ **更新 `document-generation.md`**
   - ✅ 在开头添加说明，引用 `architecture-diagram-template.md` 和 `wiki-output.md` 作为详细参考
   - ✅ 明确主次关系

3. ✅ **更新 `PROMPTS_OVERVIEW.md`**
   - ✅ 添加 `document-generation.md` 的描述
   - ✅ 更新架构图和 WIKI 规范的说明，说明它们已被整合

---

## ✅ 检查清单

### 整合前检查

- [ ] 确认两个文件的内容确实有重叠
- [ ] 确认整合后不会丢失重要信息
- [ ] 确认整合后的文件大小不会超过 500 行
- [ ] 确认整合后职责仍然单一明确

### 整合后检查

- [ ] 整合后的文件结构清晰
- [ ] 所有重要内容都已保留
- [ ] 索引文件已更新
- [ ] 相关文档已更新
- [ ] 没有破坏引用关系

---

## 📊 预期效果

### 优化前

- 文件写入相关规则分散在 2 个文件中
- 时间相关规则有重复内容
- 文档阶段规范主次关系不明确

### 优化后

- 文件写入相关规则整合到 1 个文件中，更完整
- 时间相关规则减少重复，保持引用关系
- 文档阶段规范主次关系明确，便于使用

---

## 🔗 相关文件

- `prompts/stages/common/mode/act/file-write.md`
- `prompts/stages/common/mode/act/long-text-check.md`
- `prompts/stages/common/document/time-format.md`
- `prompts/stages/common/mode/act/time-check.md`
- `prompts/stages/documentation/document-generation.md`
- `prompts/stages/documentation/architecture-diagram-template.md`
- `prompts/stages/documentation/wiki-output.md`
