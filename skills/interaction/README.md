# 交互领域 Skills

本目录包含与用户交互和确认机制相关的 AI 提示词规范。

## Skills 列表

### open-question-confirmation.md - 开放性问题确认规范
- **描述**：开放性问题确认规范，针对开放性问题必须通过询问方式与用户达成一致
- **标签**：`interaction`, `confirmation`, `open-question`
- **使用场景**：遇到需求不明确或有多种实现方案时

### time-check.md - 时间字段强制检查机制
- **描述**：时间字段强制检查机制，创建包含时间字段的文档时必须先通过工具获取当前时间
- **标签**：`time`, `validation`, `automation`
- **使用场景**：创建包含时间信息的文档或记录时

## 使用方式

```bash
# 查看所有交互相关的 skills
openskills list | grep "interaction/"

# 加载特定 skill
openskills read open-question-confirmation
```

## 相关领域

- **[Core](/skills/core/)** - 核心规则（顶层规则，包含模式、权限等规范）⭐
- [Workflow](/skills/workflow/) - 工作流程相关规范
- [Documentation](/skills/documentation/) - 文档编写相关规范
