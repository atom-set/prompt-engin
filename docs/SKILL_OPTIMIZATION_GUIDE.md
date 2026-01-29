# Skills 优化指南

本指南介绍如何使用 `analyze` 和 `apply-optimize` 命令来分析和优化 skills。

## 命令概述

### 1. `analyze` - 分析 Skills 并生成报告

分析当前项目中的所有 skills，生成包含优化建议的详细报告。

**基本用法：**
```bash
# 分析所有 skills 并生成报告
skill-engine analyze

# 分析所有 skills 并指定输出文件
skill-engine analyze --output my_report.md

# 分析单个 skill
skill-engine analyze --skill core/act-mode

# 生成 JSON 格式的报告
skill-engine analyze --format json
```

**输出：**
- 默认生成 `skills_report.md` 文件
- 包含以下内容：
  - 检验报告（质量问题、缺少章节、重复内容）
  - 优先级分析
  - 整合建议
  - 优化建议（这是 `apply-optimize` 命令使用的部分）

### 2. `apply-optimize` - 根据报告应用优化

根据分析报告对需要优化的 skills 进行自动优化。

**基本用法：**
```bash
# 根据默认报告文件应用优化（实际修改）
skill-engine apply-optimize

# 试运行模式（查看优化计划，不实际修改）
skill-engine apply-optimize --dry-run

# 指定报告文件
skill-engine apply-optimize --from-report my_report.md

# 只优化指定的 skill
skill-engine apply-optimize --skill core/act-mode

# 应用优化并生成优化报告
skill-engine apply-optimize --output optimization_report.md
```

**工作流程：**
1. 读取报告文件中的优化建议（默认：`skills_report.md`）
2. 解析优化建议并生成优化计划
3. 显示优化计划（包括可自动应用和需手动处理的项目）
4. 应用可自动应用的优化（如添加依赖关系）
5. 生成优化报告

## 完整工作流程示例

### 步骤 1: 分析 Skills

```bash
# 生成分析报告
skill-engine analyze
```

这将生成 `skills_report.md` 文件，包含所有 skills 的分析结果和优化建议。

### 步骤 2: 查看优化计划（可选）

```bash
# 试运行模式，查看将要应用的优化
skill-engine apply-optimize --dry-run
```

这将显示优化计划，但不会实际修改文件。

### 步骤 3: 应用优化

```bash
# 实际应用优化
skill-engine apply-optimize
```

这将：
- 读取 `skills_report.md` 中的优化建议
- 自动应用可自动应用的优化（如添加依赖关系）
- 标记需要手动处理的优化项

### 步骤 4: 验证结果

```bash
# 验证优化后的 skill
skill-engine validate core/act-mode

# 或者重新生成报告查看改进
skill-engine analyze
```

## 优化类型

### 可自动应用的优化

- **添加依赖关系**：自动在 "与其他规则的配合" 章节添加依赖关系

### 需手动处理的优化

- **添加代码示例**：需要在 skill 文件中手动添加示例章节
- **扩展描述**：需要手动扩展 skill 的描述
- **其他内容改进**：需要根据具体情况手动处理

## 注意事项

1. **备份重要文件**：在应用优化前，建议先提交代码到版本控制系统
2. **检查优化计划**：使用 `--dry-run` 参数先查看优化计划
3. **手动处理项**：某些优化需要手动处理，请仔细查看优化报告
4. **验证结果**：应用优化后，建议运行验证命令检查结果

## 常见问题

### Q: 报告文件找不到怎么办？

A: 确保先运行 `skill-engine analyze` 生成报告，或者使用 `--from-report` 参数指定报告文件路径。

### Q: 如何只优化特定的 skill？

A: 使用 `--skill` 参数：
```bash
skill-engine apply-optimize --skill core/act-mode
```

### Q: 优化失败了怎么办？

A: 检查错误信息，通常是因为：
- 报告文件格式不正确
- Skill 文件不存在
- 文件权限问题

### Q: 如何查看优化历史？

A: 每次应用优化都会生成优化报告（如果指定了 `--output` 参数），可以查看这些报告了解优化历史。

## 相关命令

- `skill-engine report` - 生成完整分析报告（简化版）
- `skill-engine optimize` - 一键优化 skills（旧版命令，仍可使用）
- `skill-engine manage` - 管理 skills（检验、优化、整合、优先级）
- `skill-engine validate` - 验证 skill 格式
