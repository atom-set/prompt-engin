# 文档领域 Skills

本目录包含与文档编写和生成相关的 AI 提示词规范。

## Skills 列表

### format.md - 文档格式规范
- **描述**：文档格式规范，包括任务清单、测试用例、文章报告等格式要求
- **标签**：`documentation`, `format`, `standards`
- **使用场景**：创建各类文档时自动应用此规范

### generation.md - 文档生成规范
- **描述**：文档生成规范，整合技术方案、架构图、WIKI 等文档类型的规范
- **标签**：`documentation`, `generation`, `automation`
- **使用场景**：生成技术文档、项目文档时

### architecture-diagram.md - 架构图文档模板规范
- **描述**：架构图文档模板规范，包括图表模块化、说明可折叠、便于导航等
- **标签**：`architecture`, `diagram`, `template`
- **使用场景**：创建架构图文档时

### wiki-output.md - WIKI 文档输出规范
- **描述**：WIKI 文档输出规范，包括文档结构、格式要求、Mermaid 图表转换等
- **标签**：`wiki`, `output`, `mermaid`
- **使用场景**：生成 WIKI 格式的文档时

### time-format.md - 时间格式规范
- **描述**：时间格式规范，强制要求所有时间字段都必须通过工具动态获取
- **标签**：`time`, `format`, `standards`
- **使用场景**：处理时间相关的内容时自动应用

## 使用方式

```bash
# 查看所有文档相关的 skills
openskills list | grep "documentation/"

# 加载特定 skill
openskills read architecture-diagram
```

## 相关领域

- **[Core](/skills/core/)** - 核心规则（顶层规则）⭐
- [Code](/skills/code/) - 代码开发相关规范
- [Workflow](/skills/workflow/) - 工作流程相关规范
