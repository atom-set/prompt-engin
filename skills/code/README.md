# 代码开发领域 Skills

本目录包含与代码开发相关的 AI 提示词规范。

## Skills 列表

### organization.md - 代码组织规范
- **描述**：代码组织规范，包括文件大小限制、拆分原则等
- **标签**：`code`, `organization`, `refactoring`
- **使用场景**：代码文件过大、需要重构、代码结构混乱时

### design-principles.md - 设计原则规范
- **描述**：设计原则规范，强调简单设计优先，避免过度设计
- **标签**：`design`, `principles`, `simplicity`
- **使用场景**：技术方案设计、架构设计、功能实现时

### debugging.md - 问题定位与调试规范
- **描述**：问题定位与调试规范，包括调试流程、调试代码规范等
- **标签**：`debugging`, `troubleshooting`, `problem-solving`
- **使用场景**：Bug 修复、问题定位、性能优化时

## 使用方式

```bash
# 查看所有代码相关的 skills
openskills list | grep "code/"

# 加载特定 skill
openskills read design-principles
```

## 相关领域

- **[Core](/skills/core/)** - 核心规则（顶层规则，包含代码格式、命名、函数设计等规范）⭐
- [Documentation](/skills/documentation/) - 文档编写相关规范
- [Workflow](/skills/workflow/) - 工作流程相关规范
