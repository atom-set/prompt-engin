
<skills_system priority="1">

## Available Skills

<!-- SKILLS_TABLE_START -->
<usage>
When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.

How to use skills:
- Invoke: Bash("openskills read <skill-name>")
- The skill content will load with detailed instructions on how to complete the task
- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)

Usage notes:
- Only use skills listed in <available_skills> below
- Do not invoke a skill that is already loaded in your context
- Each skill invocation is stateless
</usage>

<available_skills>

<skill>
<name>architecture-diagram-template</name>
<description>架构图文档模板规范，包括图表模块化、说明可折叠、便于导航等</description>
<location>project</location>
</skill>

<skill>
<name>code-organization</name>
<description>代码组织规范，包括文件大小限制、拆分原则等</description>
<location>project</location>
</skill>

<skill>
<name>compatibility-check</name>
<description>技术方案调整的兼容性确认机制，涉及技术方案调整时必须明确询问用户是否需要向下兼容</description>
<location>project</location>
</skill>

<skill>
<name>design-principles</name>
<description>设计原则规范，强调简单设计优先，避免过度设计</description>
<location>project</location>
</skill>

<skill>
<name>document-format</name>
<description>文档格式规范，包括任务清单、测试用例、文章报告等格式要求。当用户需要创建文档时，自动应用此规范。</description>
<location>project</location>
</skill>

<skill>
<name>document-generation</name>
<description>文档生成规范，整合技术方案、架构图、WIKI 等文档类型的规范</description>
<location>project</location>
</skill>

<skill>
<name>exception-handling</name>
<description>例外情况的处理流程，包括明显的语法错误、已知的简单问题等例外情况</description>
<location>project</location>
</skill>

<skill>
<name>file-reading</name>
<description>大文件读取策略，对于大文件的读取应采用阶段性读取策略</description>
<location>project</location>
</skill>

<skill>
<name>modular-output</name>
<description>完整方案模块化输出策略，适用于复杂内容的输出</description>
<location>project</location>
</skill>

<skill>
<name>open-question-confirmation</name>
<description>开放性问题确认规范，针对开放性问题必须通过询问方式与用户的理解达成一致</description>
<location>project</location>
</skill>

<skill>
<name>phase-implementation</name>
<description>大型工程分阶段实施规则，大型工程必须分阶段实施，每个阶段完成后确认和测试再继续</description>
<location>project</location>
</skill>

<skill>
<name>problem-location</name>
<description>问题定位与调试规范，包括调试流程、调试代码规范等</description>
<location>project</location>
</skill>

<skill>
<name>project-clean-principle</name>
<description>项目清洁原则，避免将 AI 辅助开发工具和非业务相关的脚本混入项目核心代码</description>
<location>project</location>
</skill>

<skill>
<name>time-check</name>
<description>时间字段强制检查机制，创建包含时间字段的文档时，必须先通过工具获取当前时间</description>
<location>project</location>
</skill>

<skill>
<name>time-format</name>
<description>时间格式规范，强制要求所有时间字段都必须通过工具动态获取，严禁使用任何假设时间。当用户需要处理时间相关的内容时，自动应用此规范。</description>
<location>project</location>
</skill>

<skill>
<name>wiki-output</name>
<description>WIKI 文档输出规范，包括文档结构、格式要求、Mermaid 图表转换等</description>
<location>project</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>
