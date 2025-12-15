# Debug 模式行为规范

> **文件说明**：本文件包含 Debug 模式的所有行为规范，从原 `plan-act-mode.md` 文件中拆分而来
> **拆分时间**：2025-12-12

---

- **模式性质**：Debug 模式是一个**辅助模式**，可以与 Plan/Act 模式并行使用
- **默认状态**：Debug 模式默认关闭，需要用户明确开启
- **模式标识**：
  - 当 Debug 模式开启时，在响应开头显示：`# 模式：Plan [Debug]` 或 `# 模式：执行 [Debug]`
  - 当 Debug 模式关闭时，正常显示：`# 模式：Plan` 或 `# 模式：执行`
- **状态管理**：
  - **开启条件**：用户消息包含 `【DEBUG START】` 时开启 Debug 模式
  - **持续执行**：开启后持续执行 Debug 模式功能，直到用户消息包含 `【DEBUG END】`
  - **结束条件**：用户消息包含 `【DEBUG END】` 时结束 Debug 模式
  - **状态标识**：Debug 模式开启时显示 `[Debug]` 标识，关闭时移除标识
- **不影响主流程**：Debug 模式不影响 Plan/Act 模式的正常工作流程

#### Debug模式触发机制

- **触发条件**：
  - **开启触发**：用户消息包含 `【DEBUG START】` 时，立即询问并开启 Debug 模式
  - **结束触发**：用户消息包含 `【DEBUG END】` 时，立即结束 Debug 模式
  - **持续执行**：开启后持续执行 Debug 模式功能，直到检测到 `【DEBUG END】`
- **询问时机**：
  - **检测到 `【DEBUG START】`**：
    - 立即询问 Debug 模式
    - 询问格式见下方
    - 用户确认后开启 Debug 模式
  - **检测到 `【DEBUG END】`**：
    - 立即结束 Debug 模式
    - 在响应中说明 Debug 模式已结束
    - 移除 `[Debug]` 标识
  - **Debug 模式已开启**：
    - 继续执行 Debug 模式功能
    - 在响应中显示 `[Debug]` 标识
- **询问格式**（当检测到 `【DEBUG START】` 时）：
  ```
  # 模式：Plan

  ## 🔍 Debug 模式询问

  检测到 `【DEBUG START】`，是否进入 Debug 模式？

  Debug 模式功能：
  1. 对话结束后检查提示词规则是否违背
  2. 每次回答后检查规则是否有漏洞
  3. 每次提问后询问是否提炼归档本次提示词
  4. 上下文变化时提供会话ID，方便回溯

  请输入：
  - "是" 或 "开启" 或 "debug"：开启 Debug 模式（将一直执行，直到检测到 `【DEBUG END】`）
  - "否" 或 "关闭" 或 "skip"：跳过 Debug 模式（默认）
  ```
- **用户响应处理**：
  - 用户输入"是"、"开启"、"debug"（不区分大小写）：开启 Debug 模式，持续执行直到检测到 `【DEBUG END】`
  - 用户输入"否"、"关闭"、"skip"（不区分大小写）或未回复：保持 Debug 模式关闭（默认）
  - 开启后，在后续响应中显示 `[Debug]` 标识，直到检测到 `【DEBUG END】`
- **结束处理**（当检测到 `【DEBUG END】` 时）：
  - 立即结束 Debug 模式
  - 在响应中说明："Debug 模式已结束（检测到 `【DEBUG END】`）"
  - 移除 `[Debug]` 标识
  - 停止执行 Debug 模式相关功能

#### 对话结束后的规则检查机制

- **检查时机**：
  - 每次对话结束后（用户明确结束对话或开始新话题时）
  - 仅在 Debug 模式开启时执行
- **对话结束的判断标准**（明确标准）：
  1. **用户明确结束对话**：
     - 用户消息中包含明确的结束关键词：
       - "结束"、"完成"、"谢谢"、"再见"、"好了"、"搞定"等
     - 用户明确表示任务完成或对话结束
  2. **开始新话题**：
     - 主题关键词变化超过 50%：
       - 从"代码开发"切换到"文档编写"
       - 从"问题定位"切换到"功能实现"
       - 从"设计"切换到"测试"等
     - 用户明确表示要处理新的、不相关的任务
  3. **时间间隔**：
     - 超过 5 分钟无交互（用户无回复）
     - 系统可以认为对话已结束
  4. **判断逻辑示例**：
     ```typescript
     // 伪代码
     function isConversationEnded(): boolean {
       const lastUserMessage = getLastUserMessage();
       const timeSinceLastMessage = getTimeSinceLastMessage();
       
       // 情况1：用户明确结束
       const endKeywords = ['结束', '完成', '谢谢', '再见', '好了', '搞定'];
       if (endKeywords.some(keyword => lastUserMessage.includes(keyword))) {
         return true;
       }
       
       // 情况2：开始新话题（主题关键词变化 > 50%）
       const topicChangeRatio = calculateTopicChangeRatio();
       if (topicChangeRatio > 0.5) {
         return true;
       }
       
       // 情况3：时间间隔超过 5 分钟
       if (timeSinceLastMessage > 5 * 60 * 1000) { // 5 分钟 = 300000 毫秒
         return true;
       }
       
       return false;
     }
     ```
- **检查内容**：
  1. **Plan/Act 模式切换规则**：是否遵循了模式切换规则
  2. **代码修改前方案输出**：是否遵循了代码修改前的方案输出机制
  3. **文件大小限制**：是否遵循了文件大小限制（500行）
  4. **时间格式规范**：是否遵循了时间格式规范（不使用假设日期）
  5. **文档格式规范**：是否遵循了文档格式规范
  6. **问题定位规范**：是否遵循了问题定位规范（先定位再修复）
  7. **其他关键规则**：其他关键规则遵循情况
- **检查结果输出格式**：
  ```
  ## 📋 规则检查结果

  | 规则项 | 状态 | 说明 |
  |--------|------|------|
  | Plan/Act 模式切换 | ✅ 通过 | 正确遵循了模式切换规则 |
  | 代码修改前方案输出 | ✅ 通过 | 已输出完整方案 |
  | 文件大小限制 | ⚠️ 警告 | 创建了1个超过500行的文件 |
  | 时间格式规范 | ✅ 通过 | 正确使用了动态时间 |
  | 文档格式规范 | ✅ 通过 | 遵循了文档格式要求 |
  | 问题定位规范 | ✅ 通过 | 先定位问题再修复 |
  | ... | ... | ... |

  **检查总结**：
  - ✅ 通过：X 项
  - ⚠️ 警告：Y 项
  - ❌ 失败：Z 项
  ```
- **状态标识说明**：
  - ✅ **通过**：完全遵循规则，无问题
  - ⚠️ **警告**：部分违背规则，但不影响功能（如文件略超500行）
  - ❌ **失败**：严重违背规则，可能影响功能或质量
- **检查执行原则**：
  - 必须客观、准确地检查规则遵循情况
  - 对于警告项，应说明具体问题和建议
  - 对于失败项，应说明违背的规则和修复建议

#### 规则漏洞检查机制

- **检查时机**（强制要求）：
  - 仅在 Debug 模式开启时执行
  - **执行场景**：
    1. **Act模式执行完成后**（主要场景）：
       - 仅在 Act 模式执行完代码修改后执行
       - **执行流程**：
         ```
         开始 → 执行代码修改 → 完成所有修改 → 执行规则漏洞检查 → 输出检查结果 → 检测上下文变化 → 提供会话ID（如果变化） → 询问提示词归档 → 返回 Plan 模式 → 结束
         ```
       - **重要说明**：
         - Act 模式执行完成后，除了执行规则漏洞检查，还应执行其他适用的 Debug 功能
         - 必须使用 Debug 功能执行检查清单确保所有功能都被执行
    2. **用户主动要求检查**（补充场景）：
       - 用户在 Plan 模式或 Act 模式下主动要求检查规则漏洞（如"检查规则有没有漏洞"）
       - **执行流程**：
         ```
         用户要求检查 → 分析规则文件 → 执行规则漏洞检查 → 输出检查结果 → 继续当前模式
         ```
       - **输出位置**：在响应中直接输出检查结果，使用分隔线区分
  - **触发条件**（明确标准）：
    1. **场景1：Act模式执行完成后**（必须条件）：
       - 当前处于 Act 模式
       - Debug 模式已开启
       - 已执行代码修改操作（search_replace、write、delete_file 等）
    2. **场景2：用户主动要求检查**（必须条件）：
       - Debug 模式已开启
       - 用户明确要求检查规则漏洞（如"检查规则有没有漏洞"、"检查规则漏洞"等）
    3. **不触发的情况**：
       - Debug 模式未开启时不执行检查
       - Act 模式下未执行代码修改且用户未主动要求时不执行检查
       - Plan 模式下用户未主动要求时不执行检查
    3. **判断逻辑**：
       ```typescript
       // 伪代码
       function shouldCheckRuleVulnerabilities(): boolean {
         // 必须条件1：当前处于 Act 模式
         if (currentMode !== 'Act') {
           return false;
         }
         
         // 必须条件2：Debug 模式已开启
         if (!isDebugModeEnabled()) {
           return false;
         }
         
         // 必须条件3：已执行代码修改操作
         if (!hasPerformedCodeModifications()) {
           return false;
         }
         
         return true;
       }
       ```
  - **重要原则**：
    - ✅ **Act模式执行完成后自动检查**：在 Act 模式执行完代码修改后自动执行检查
    - ✅ **用户主动要求时执行检查**：用户在 Plan 模式或 Act 模式下主动要求时执行检查
    - ✅ **Debug 模式必须开启**：所有规则漏洞检查都必须在 Debug 模式开启时执行
    - ✅ **执行所有适用的 Debug 功能**：Act 模式执行完成后，应执行所有适用的 Debug 功能（规则漏洞检查、上下文变化检测、提示词归档询问）
    - ✅ **使用检查清单验证**：使用 Debug 功能执行检查清单确保所有功能都被执行
    - ❌ **禁止在 Debug 模式未开启时执行检查**：避免不必要的检查
    - ❌ **禁止在未满足触发条件时执行检查**：避免无效检查
    - ❌ **禁止跳过任何 Debug 功能**：所有适用的 Debug 功能都必须执行
- **检查目的**：
  - 检查规则本身是否存在漏洞、冲突或不完善之处
  - 发现规则可能导致的潜在问题
  - 识别规则之间的冲突或不一致
- **检查内容**：
  1. **规则冲突检查**：
     - 检查不同规则之间是否存在冲突
     - 检查规则内部是否存在逻辑矛盾
     - 检查规则优先级是否清晰
  2. **规则覆盖检查**：
     - 检查是否有场景未被规则覆盖
     - 检查规则是否过于宽泛或过于严格
     - 检查规则边界情况是否处理
  3. **规则表述检查**：
     - 检查规则表述是否清晰明确
     - 检查规则是否存在歧义
     - 检查规则示例是否充分
  4. **规则执行检查**：
     - 检查规则执行时机是否合理
     - 检查规则触发条件是否明确
     - 检查规则执行流程是否完整
  5. **规则完整性检查**：
     - 检查规则是否包含必要的检查项
     - 检查规则是否缺少关键步骤
     - 检查规则是否形成闭环
  6. **问题定位规范检查**：
     - 检查是否遵循了问题定位规范
     - 检查是否先定位问题再修复
     - 检查是否添加了必要的调试代码
     - 检查是否清理了临时调试代码
     - 检查是否在未定位问题的情况下添加了防御性代码
- **检查结果输出位置**（强制要求）：
  - **场景1：Act模式执行完成后**：
    - **输出位置**：在 Act 模式执行完成总结之后
    - **输出时机**：所有代码修改完成后，返回 Plan 模式之前
    - **输出格式**：使用分隔线（`---`）区分检查结果和执行总结
    - **输出顺序**：
      ```
      Act 模式执行流程（Debug 模式开启时）：
      1. 执行代码修改
      2. 输出执行完成总结
      3. 执行规则漏洞检查
      4. 输出检查结果（在总结之后）
      5. 检测上下文变化（模式切换：Act → Plan）
      6. 如果检测到上下文变化，提供会话ID
      7. 询问是否提炼归档本次提示词（用户提问"act"后）
      8. 返回 Plan 模式
      ```
    - **Debug 功能执行检查清单**（Act 模式执行完成后，Debug 模式开启时）：
      - [ ] 执行规则漏洞检查
      - [ ] 检测上下文变化（模式切换：Act → Plan）
      - [ ] 如果检测到上下文变化，提供会话ID
      - [ ] 询问是否提炼归档本次提示词（用户提问"act"后）
      - [ ] 返回 Plan 模式
      - **重要原则**：
        - ✅ **必须执行所有适用的 Debug 功能**：确保所有 Debug 功能都被执行
        - ✅ **按照执行顺序执行**：严格按照执行流程顺序执行
        - ✅ **使用检查清单验证**：使用检查清单确保不遗漏任何功能
        - ❌ **禁止跳过任何 Debug 功能**：所有适用的 Debug 功能都必须执行
  - **场景2：用户主动要求检查**：
    - **输出位置**：在响应中直接输出检查结果
    - **输出时机**：完成规则分析后立即输出
    - **输出格式**：使用分隔线（`---`）区分检查结果和其他内容
    - **输出顺序**：
      ```
      用户要求检查流程：
      1. 识别用户要求
      2. 分析规则文件
      3. 执行规则漏洞检查
      4. 输出检查结果
      5. 继续当前模式
      ```
- **检查结果输出格式**：
  ```
  ---

  ## 🔍 规则漏洞检查结果（Debug 模式）

  | 检查项 | 状态 | 发现的问题 | 建议 |
  |--------|------|-----------|------|
  | 规则冲突检查 | ✅ 正常 | 无冲突 | - |
  | 规则覆盖检查 | ⚠️ 警告 | 场景X未被规则覆盖 | 建议添加规则覆盖场景X |
  | 规则表述检查 | ✅ 正常 | 表述清晰 | - |
  | 规则执行检查 | ❌ 发现问题 | 规则Y的执行时机不明确 | 建议明确规则Y的触发条件 |
  | 规则完整性检查 | ✅ 正常 | 规则完整 | - |

  **检查总结**：
  - ✅ 正常：X 项
  - ⚠️ 警告：Y 项（需要关注）
  - ❌ 发现问题：Z 项（需要修复）

  **发现的规则漏洞**（如果发现问题）：
  1. [漏洞描述1]：影响范围、严重程度、修复建议
  2. [漏洞描述2]：影响范围、严重程度、修复建议
  ```
- **状态标识说明**：
  - ✅ **正常**：未发现规则漏洞，规则设计合理
  - ⚠️ **警告**：发现潜在的规则问题，但不影响当前使用
  - ❌ **发现问题**：发现明确的规则漏洞，可能影响功能或质量
- **检查执行原则**：
  - 必须客观、深入地分析规则本身
  - 对于警告项，应说明潜在问题和改进建议
  - 对于发现的问题，应详细说明漏洞、影响范围和修复建议
  - 检查应基于实际执行情况，而非理论分析
- **漏洞修复建议**：
  - 对于发现的规则漏洞，应提供具体的修复建议
  - 修复建议应包括：修改位置、修改内容、修改原因
  - 修复建议应遵循规则文件的格式和结构要求

#### 每次提问后的提示词提炼归档机制

- **询问时机**：
  - 每次用户提问后，AI 响应完成时
  - 仅在 Debug 模式开启时执行
- **询问格式**：
  ```
  ## 📝 提示词提炼归档

  是否对本次提示词进行提炼归档？

  本次提示词要点：
  - [提取的关键信息1]
  - [提取的关键信息2]
  - [提取的关键信息3]
  - ...

  请输入：
  - "是" 或 "归档"：进行提炼归档
  - "否" 或 "跳过"：跳过归档
  ```
- **提示词要点提取原则**：
  1. **关键需求**：提取用户的核心需求或问题
  2. **技术要点**：提取涉及的技术点、工具、方法等
  3. **上下文信息**：提取重要的上下文信息（如文件路径、配置项等）
  4. **决策点**：提取需要做出决策的关键点
  5. **限制条件**：提取约束条件、要求等
- **归档格式建议**：
  - **存储位置**：`.cursor-rules/debug/prompts/` 目录（如果不存在，建议创建）
  - **文件命名**：`prompt-{YYYY-MM-DD}-{序号}.md`（使用实际日期，禁止假设）
  - **序号生成规则**（明确标准）：
    1. **生成方法**：自增序号（从 1 开始，每天重置）
    2. **生成逻辑**：
       - 检查当天已有归档文件（格式：`prompt-{YYYY-MM-DD}-{序号}.md`）
       - 提取当天所有归档文件的最大序号
       - 新序号 = 最大序号 + 1
       - 如果当天没有归档文件，序号从 1 开始
    3. **冲突处理**：
       - 如果生成的文件名已存在，序号 + 1，重新检查
       - 重复此过程直到找到不存在的文件名
    4. **生成逻辑示例**：
       ```typescript
       // 伪代码
       function generateArchiveSequenceNumber(date: string): number {
         const archiveDir = '.cursor-rules/debug/prompts/';
         const pattern = new RegExp(`^prompt-${date}-(\\d+)\\.md$`);
         
         // 获取当天所有归档文件
         const files = listFiles(archiveDir).filter(file => pattern.test(file));
         
         if (files.length === 0) {
           return 1; // 当天第一个归档文件
         }
         
         // 提取所有序号并找到最大值
         const sequenceNumbers = files.map(file => {
           const match = file.match(pattern);
           return match ? parseInt(match[1], 10) : 0;
         });
         
         const maxSequenceNumber = Math.max(...sequenceNumbers);
         return maxSequenceNumber + 1;
       }
       
       // 生成文件名（带冲突检测）
       function generateArchiveFileName(date: string): string {
         let sequenceNumber = generateArchiveSequenceNumber(date);
         let fileName = `prompt-${date}-${sequenceNumber}.md`;
         
         // 冲突检测：如果文件已存在，序号 + 1
         while (fileExists(fileName)) {
           sequenceNumber++;
           fileName = `prompt-${date}-${sequenceNumber}.md`;
         }
         
         return fileName;
       }
       ```
  - **内容格式**：
    ```markdown
    # 提示词归档 - {YYYY-MM-DD}

    > **归档时间**: {实际时间}（本地时间）
    > **会话ID**: {如果有会话ID}

    ## 原始提示词
    {用户的原始提示词}

    ## 提炼要点
    - 关键需求：{需求描述}
    - 技术要点：{技术点描述}
    - 上下文信息：{上下文描述}
    - 决策点：{决策点描述}
    - 限制条件：{限制条件描述}

    ## 使用场景
    {适用场景说明}

    ## 备注
    {其他备注信息}
    ```
- **归档执行**：
  - 如果用户选择"是"或"归档"，创建归档文件
  - 如果用户选择"否"或"跳过"，跳过归档，继续正常流程
  - 归档文件应遵循文件写入规则（先框架后内容）

#### 上下文变化时的会话ID管理机制

- **生成时机**：
  - 当检测到上下文语境发生重大变化时
  - 例如：从代码开发切换到文档编写、从问题定位切换到功能实现、从 Plan 模式切换到 Act 模式等
  - 仅在 Debug 模式开启时执行
- **执行时机**（强制要求）：
  - 必须在 Debug 模式处理之后、处理用户需求之前执行
  - 作为响应执行顺序的第三步（模式标识 → Debug模式处理 → **上下文变化检测** → 处理用户需求）
  - 不能跳过，不能延后
- **执行条件**（强制要求）：
  - 仅在 Debug 模式开启时执行
  - 如果 Debug 模式未开启，跳过此步骤
  - 必须在每次响应中检查 Debug 模式状态
- **上下文变化判断标准**（量化标准）：
  1. **场景切换**（量化标准）：
     - 场景关键词匹配度变化 > 50%
     - 场景关键词列表：
       - 开发场景：代码、开发、实现、编写、函数、类、模块等
       - 文档场景：文档、说明、指南、README、Markdown 等
       - 测试场景：测试、用例、验证、断言等
       - 设计场景：设计、架构、方案、流程图等
     - 判断逻辑：计算前后场景关键词匹配度，如果变化 > 50%，则认为是场景切换
  2. **模式切换**（明确检测）：
     - 从 Plan 模式切换到 Act 模式（明确检测到"Act"指令）
     - 从 Act 模式切换到 Plan 模式（执行完成后自动返回）
     - 判断逻辑：直接检测模式状态变化，无需量化
  3. **主题切换**（量化标准）：
     - 主题关键词变化 > 70%
     - 主题关键词提取：从用户消息中提取关键主题词（如"规则库"、"测试"、"修复"等）
     - 判断逻辑：计算前后主题关键词匹配度，如果变化 > 70%，则认为是主题切换
  4. **任务切换**（量化标准）：
     - 任务关键词变化 > 60%
     - 任务关键词提取：从用户消息中提取任务相关关键词（如"创建"、"修改"、"删除"、"分析"等）
     - 判断逻辑：计算前后任务关键词匹配度，如果变化 > 60%，则认为是任务切换
  5. **判断逻辑示例**：
     ```typescript
     // 伪代码
     function calculateKeywordChangeRatio(previousKeywords: string[], currentKeywords: string[]): number {
       const previousSet = new Set(previousKeywords);
       const currentSet = new Set(currentKeywords);
       
       // 计算交集和并集
       const intersection = [...previousSet].filter(x => currentSet.has(x));
       const union = new Set([...previousSet, ...currentSet]);
       
       // 计算变化比例（1 - 交集/并集）
       const changeRatio = 1 - (intersection.length / union.size);
       return changeRatio;
     }
     
     function isContextChanged(previousContext: Context, currentContext: Context): boolean {
       // 情况1：模式切换（明确检测）
       if (previousContext.mode !== currentContext.mode) {
         return true;
       }
       
       // 情况2：场景切换（关键词匹配度变化 > 50%）
       const sceneChangeRatio = calculateKeywordChangeRatio(
         previousContext.sceneKeywords,
         currentContext.sceneKeywords
       );
       if (sceneChangeRatio > 0.5) {
         return true;
       }
       
       // 情况3：主题切换（关键词匹配度变化 > 70%）
       const topicChangeRatio = calculateKeywordChangeRatio(
         previousContext.topicKeywords,
         currentContext.topicKeywords
       );
       if (topicChangeRatio > 0.7) {
         return true;
       }
       
       // 情况4：任务切换（关键词匹配度变化 > 60%）
       const taskChangeRatio = calculateKeywordChangeRatio(
         previousContext.taskKeywords,
         currentContext.taskKeywords
       );
       if (taskChangeRatio > 0.6) {
         return true;
       }
       
       return false;
     }
     ```
- **会话ID格式**：
  - 格式：`session-{YYYYMMDD}-{HHMMSS}-{random}`
  - 示例：`session-20251206-143022-abc123`
  - 生成规则：
    - `YYYYMMDD`：当前日期（使用 `date '+%Y%m%d'` 获取）
    - `HHMMSS`：当前时间（使用 `date '+%H%M%S'` 获取）
    - `random`：固定 6 位随机字符串（字母数字组合）
  - **随机字符串生成规则**（明确标准）：
    1. **生成方法**：使用系统随机数生成器
    2. **字符集**：`a-z`（小写字母）、`A-Z`（大写字母）、`0-9`（数字），共 62 个字符
    3. **长度**：固定 6 位（不再使用 3-6 位的可变长度）
    4. **生成逻辑**：
       - 从字符集中随机选择 6 个字符
       - 每个字符的选择概率相等（1/62）
       - 确保随机性，避免可预测性
    5. **生成逻辑示例**：
       ```typescript
       // 伪代码
       function generateRandomString(length: number = 6): string {
         const charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
         const charsetLength = charset.length;
         let randomString = '';
         
         // 使用系统随机数生成器
         for (let i = 0; i < length; i++) {
           const randomIndex = Math.floor(Math.random() * charsetLength);
           randomString += charset[randomIndex];
         }
         
         return randomString;
       }
       
       // 生成会话ID
       function generateSessionId(): string {
         const date = getCurrentDate('YYYYMMDD'); // 使用 date '+%Y%m%d' 获取
         const time = getCurrentTime('HHMMSS');   // 使用 date '+%H%M%S' 获取
         const random = generateRandomString(6);   // 固定 6 位随机字符串
         
         return `session-${date}-${time}-${random}`;
       }
       ```
       ```bash
       # Shell 实现示例
       generate_random_string() {
         local length=${1:-6}
         local charset="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
         local result=""
         
         for ((i=0; i<length; i++)); do
           local index=$((RANDOM % ${#charset}))
           result="${result}${charset:$index:1}"
         done
         
         echo "$result"
       }
       
       generate_session_id() {
         local date=$(date '+%Y%m%d')
         local time=$(date '+%H%M%S')
         local random=$(generate_random_string 6)
         
         echo "session-${date}-${time}-${random}"
       }
       ```
- **输出格式**：
  ```
  ## 🔄 上下文变化检测

  检测到上下文语境发生变化：
  - 之前：{之前的上下文描述}
  - 现在：{现在的上下文描述}

  **会话ID**: `session-{YYYYMMDD}-{HHMMSS}-{random}`

  如需回到之前的对话上下文，请使用此会话ID。
  ```
- **会话ID使用说明**：
  - 会话ID用于标识特定的对话上下文
  - 用户可以使用会话ID在后续对话中引用之前的上下文
  - 会话ID应记录在提示词归档中（如果进行了归档）
- **会话状态记录**（可选）：
  - 可以记录当前会话的关键信息：
    - 当前模式（Plan/Act）
    - 当前任务或主题
    - 关键文件或路径
    - 重要决策或配置
  - 这些信息可以帮助用户更好地理解上下文变化

#### Debug模式使用注意事项

- **性能影响**：
  - Debug 模式会增加一些交互步骤，可能影响响应速度
  - 建议在需要规则检查或提示词归档时开启
  - 日常开发可以关闭 Debug 模式
