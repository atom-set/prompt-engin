
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

Priority and application order:
1. **Core skills (Priority 1)** - Automatically applied first. These are the foundation rules that must be applied first:
   - mode-common (applied when generating responses)
   - security-permissions (applied before tool calls)
   - tool-permission-system (applied before every tool call)

2. **Mode skills (Priority 2)** - Applied conditionally based on current mode:
   - act-mode (when in Act mode)
   - file-write (when in File-Write mode)
   - plan-mode (when in Plan mode)
   - solution-output (when in Solution-Output mode)

3. **Code standards (Priority 3)** - Automatically applied when writing code:
   - code-format, comments, error-handling-strategy, error-logging, error-message-format, function-design, naming, return-values

4. **Domain skills (Priority 4)** - Load on-demand based on task type:
   - Check task requirements and load relevant domain skills
   - Code tasks → code-organization, design-principles, problem-location
   - Documentation tasks → document-format, document-generation, wiki-output
   - Workflow tasks → phase-implementation, compatibility-check, etc.

Application rules:
- Always apply core skills first (from skills/core/ directory)
- Apply mode skills based on current context
- Apply code standards when writing code
- Load domain skills only when needed for specific tasks
</usage>

<available_skills>

<!-- ============================================================================
     Core Skills (顶层核心规则，默认自动应用，优先级最高)
     ============================================================================ -->

<skill>
<name>mode-common</name>
<description>模式通用规则，包括模式切换、响应格式等。本规范定义了 Plan 和 Act 两种模式下的通用规则，包括模式切换条件、响应格式规范、执行顺序要求等核心机制，确保系统在不同模式下的行为一致性和可预测性。优先级：1（最高，必须首先应用）</description>
<location>mode-common</location>
</skill>

<skill>
<name>security-permissions</name>
<description>安全规则和权限规则，系统化整理权限矩阵。本规范提供了 Plan 和 Act 两种模式下的权限规则快速参考，包括工具权限分类、行为权限分类、安全检查机制等，确保所有操作都以安全为前提，权限明确、确认优先。优先级：1（最高，必须首先应用）</description>
<location>security-permissions</location>
</skill>

<skill>
<name>tool-permission-system</name>
<description>工具权限系统，定义工具分类体系和统一检查流程。优先级：1（最高，必须首先应用）</description>
<location>tool-permission-system</location>
</skill>

<!-- ============================================================================
     Mode Skills (模式规则，按模式条件应用)
     ============================================================================ -->

<skill>
<name>act-mode</name>
<description>Act 模式行为规范，定义 Act 模式下的执行规范。优先级：2（按模式条件应用）</description>
<location>act-mode</location>
</skill>

<skill>
<name>file-write</name>
<description>文件写入规则，包括文件大小检查和写入策略。优先级：2（按模式条件应用）</description>
<location>file-write</location>
</skill>

<skill>
<name>plan-mode</name>
<description>Plan 模式行为规范，定义 Plan 模式下的允许和禁止操作。优先级：2（按模式条件应用）</description>
<location>plan-mode</location>
</skill>

<skill>
<name>solution-output</name>
<description>代码修改前的方案输出机制，定义方案输出的内容和格式。优先级：2（按模式条件应用）</description>
<location>solution-output</location>
</skill>

<!-- ============================================================================
     Code Standards (代码标准，编写代码时自动应用)
     ============================================================================ -->

<skill>
<name>code-format</name>
<description>代码格式规范，包括缩进、行长度、空行等。本规范定义了代码编写时的格式要求，确保代码风格统一、可读性强，适用于所有编程语言的代码编写场景。优先级：3（编写代码时自动应用）</description>
<location>code-format</location>
</skill>

<skill>
<name>comments</name>
<description>注释规范，包括单行注释、多行注释、文档注释等。优先级：3（编写代码时自动应用）</description>
<location>comments</location>
</skill>

<skill>
<name>error-handling-strategy</name>
<description>错误处理策略，包括异常捕获、错误处理模式等。优先级：3（编写代码时自动应用）</description>
<location>error-handling-strategy</location>
</skill>

<skill>
<name>error-logging</name>
<description>错误日志记录，包括日志级别、日志内容、结构化日志等。优先级：3（编写代码时自动应用）</description>
<location>error-logging</location>
</skill>

<skill>
<name>error-message-format</name>
<description>错误信息格式，包括用户可见错误、错误码规范等。优先级：3（编写代码时自动应用）</description>
<location>error-message-format</location>
</skill>

<skill>
<name>function-design</name>
<description>函数设计规范，包括函数命名、参数处理、代码嵌套等。优先级：3（编写代码时自动应用）</description>
<location>function-design</location>
</skill>

<skill>
<name>naming</name>
<description>命名规范，包括变量、函数、类、常量等命名规则。优先级：3（编写代码时自动应用）</description>
<location>naming</location>
</skill>

<skill>
<name>return-values</name>
<description>返回值规范，包括返回值模式、错误处理等。本规范定义了函数返回值的设计原则和模式，确保返回值格式统一、类型明确，便于调用者处理和错误处理，适用于所有编程语言的函数设计场景。优先级：3（编写代码时自动应用）</description>
<location>return-values</location>
</skill>

<!-- ============================================================================
     Domain Skills (领域技能，按需加载)
     ============================================================================ -->

<skill>
<name>architecture-diagram-template</name>
<description>架构图文档模板规范，包括图表模块化、说明可折叠、便于导航等。优先级：4（按需加载，用于特定场景）</description>
<location>architecture-diagram</location>
</skill>

<skill>
<name>code-organization</name>
<description>代码组织规范，包括文件大小限制、拆分原则等。优先级：4（按需加载，用于特定场景）</description>
<location>organization</location>
</skill>

<skill>
<name>compatibility-check</name>
<description>技术方案调整的兼容性确认机制，涉及技术方案调整时必须明确询问用户是否需要向下兼容。优先级：4（按需加载，用于特定场景）</description>
<location>compatibility-check</location>
</skill>

<skill>
<name>design-principles</name>
<description>设计原则规范，强调简单设计优先，避免过度设计。优先级：4（按需加载，用于特定场景）</description>
<location>design-principles</location>
</skill>

<skill>
<name>document-format</name>
<description>文档格式规范，包括任务清单、测试用例、文章报告等格式要求。优先级：4（按需加载，用于特定场景）</description>
<location>format</location>
</skill>

<skill>
<name>document-generation</name>
<description>文档生成规范，整合技术方案、架构图、WIKI 等文档类型的规范。优先级：4（按需加载，用于特定场景）</description>
<location>generation</location>
</skill>

<skill>
<name>exception-handling</name>
<description>例外情况的处理流程，包括明显的语法错误、已知的简单问题等例外情况。优先级：4（按需加载，用于特定场景）</description>
<location>exception-handling</location>
</skill>

<skill>
<name>file-reading</name>
<description>大文件读取策略，对于大文件的读取应采用阶段性读取策略。优先级：4（按需加载，用于特定场景）</description>
<location>file-reading</location>
</skill>

<skill>
<name>modular-output</name>
<description>完整方案模块化输出策略，适用于复杂内容的输出。优先级：4（按需加载，用于特定场景）</description>
<location>modular-output</location>
</skill>

<skill>
<name>open-question-confirmation</name>
<description>开放性问题确认规范，针对开放性问题必须通过询问方式与用户的理解达成一致。优先级：4（按需加载，用于特定场景）</description>
<location>open-question-confirmation</location>
</skill>

<skill>
<name>phase-implementation</name>
<description>大型工程分阶段实施规则，大型工程必须分阶段实施，每个阶段完成后确认和测试再继续。优先级：4（按需加载，用于特定场景）</description>
<location>phase-implementation</location>
</skill>

<skill>
<name>problem-location</name>
<description>问题定位与调试规范，包括调试流程、调试代码规范等。优先级：4（按需加载，用于特定场景）</description>
<location>debugging</location>
</skill>

<skill>
<name>project-clean-principle</name>
<description>项目清洁原则，避免将 AI 辅助开发工具和非业务相关的脚本混入项目核心代码。优先级：4（按需加载，用于特定场景）</description>
<location>clean-principle</location>
</skill>

<skill>
<name>time-check</name>
<description>时间字段强制检查机制，创建包含时间字段的文档时，必须先通过工具获取当前时间。优先级：4（按需加载，用于特定场景）</description>
<location>time-check</location>
</skill>

<skill>
<name>time-format</name>
<description>时间格式规范，强制要求所有时间字段都必须通过工具动态获取，严禁使用任何假设时间。优先级：4（按需加载，用于特定场景）</description>
<location>time-format</location>
</skill>

<skill>
<name>wiki-output</name>
<description>WIKI 文档输出规范，包括文档结构、格式要求、Mermaid 图表转换等。优先级：4（按需加载，用于特定场景）</description>
<location>wiki-output</location>
</skill>

</available_skills>
<!-- SKILLS_TABLE_END -->

</skills_system>