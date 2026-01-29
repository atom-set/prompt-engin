# 工作流程领域 Skills

本目录包含与工作流程和执行策略相关的 AI 提示词规范。

## Skills 列表

### phase-implementation.md - 大型工程分阶段实施规则
- **描述**：大型工程必须分阶段实施，每个阶段完成后确认和测试再继续
- **标签**：`workflow`, `phase`, `implementation`
- **使用场景**：大型项目、复杂功能开发时

### compatibility-check.md - 兼容性确认机制
- **描述**：技术方案调整的兼容性确认机制，涉及技术方案调整时必须明确询问用户
- **标签**：`compatibility`, `migration`, `breaking-changes`
- **使用场景**：技术方案变更、版本升级时

### exception-handling.md - 例外情况处理流程
- **描述**：例外情况的处理流程，包括明显的语法错误、已知的简单问题等
- **标签**：`exception`, `error-handling`, `edge-cases`
- **使用场景**：遇到特殊情况或简单明确的问题时

### file-reading.md - 大文件读取策略
- **描述**：大文件读取策略，对于大文件的读取应采用阶段性读取策略
- **标签**：`file-reading`, `performance`, `strategy`
- **使用场景**：处理大型文件时

### modular-output.md - 完整方案模块化输出策略
- **描述**：完整方案模块化输出策略，适用于复杂内容的输出
- **标签**：`modular`, `output`, `organization`
- **使用场景**：输出复杂技术方案或长文档时

## 使用方式

```bash
# 查看所有工作流程相关的 skills
openskills list | grep "workflow/"

# 加载特定 skill
openskills read phase-implementation
```

## 相关领域

- **[Core](/skills/core/)** - 核心规则（顶层规则，包含模式、权限、文件写入等规范）⭐
- [Code](/skills/code/) - 代码开发相关规范
- [Interaction](/skills/interaction/) - 用户交互相关规范
