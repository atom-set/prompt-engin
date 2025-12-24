## 项目清洁原则

## 概述

本文件定义了项目清洁原则，确保 AI 辅助开发工具和非业务相关的脚本不会混入项目核心代码，保持项目结构的纯净性。适用于所有 AI 辅助开发过程中创建的工具、脚本、配置文件。

---

### 强制要求
- **核心原则**：避免将 AI 辅助开发工具和非业务相关的脚本混入项目核心代码，保持项目结构的纯净性
- **适用范围**：所有 AI 辅助开发过程中创建的工具、脚本、配置文件

### 项目污染的定义

**项目污染**是指将与项目核心业务无关的工具、脚本、配置文件等混入项目代码库，导致项目结构混乱、职责不清。

#### 常见的项目污染行为

❌ **禁止的行为**：
1. **将 AI 辅助工具放入项目核心目录**：
   - 将文档生成工具（如 Mermaid 转换脚本）放入 `scripts/` 目录
   - 将 AI 调试工具混入项目工具脚本
   - 将个人使用的辅助脚本提交到项目代码库
   - 将规则库的脚本复制到项目的 `.cursor-rules/` 目录

2. **混淆工具职责**：
   - 项目的 `scripts/` 目录应只包含项目核心的构建、部署、版本管理等脚本
   - AI 辅助开发工具应与项目业务代码分离

3. **将工具生成产物放入项目核心目录**：
   - 将 Mermaid 生成的图片放入项目根目录的 `assets/` 目录
   - 将文档工具生成的临时文件放入项目 `docs/` 目录
   - 将工具生成的任何产物混入项目业务资源目录

4. **不必要的依赖**：
   - 为了使用 AI 辅助工具而在项目中添加额外的依赖
   - 增加项目的环境配置复杂度

### AI 辅助工具的正确管理

#### 工具存放位置

✅ **推荐做法**：将 AI 辅助开发工具放在 `.cursor-rules` 目录下

**目录结构**：
```
.cursor-rules/
├── README.md                    # 说明文档
├── .cursorrules                 # 规则文件
├── assets/                      # 工具生成的产物目录
│   ├── batch-logger/           # Mermaid 转换生成的图片
│   └── project-name/           # 其他项目的图片资源
└── utils/                       # AI 辅助工具目录
    ├── mermaid_to_png.sh       # Mermaid 转 PNG 工具
    ├── extract_mermaid.py      # 提取 Mermaid 代码工具
    └── README.md                # 工具说明文档
```

**为什么使用 `.cursor-rules` 目录？**

1. **职责分离**：
   - 项目的 `scripts/` 目录只包含项目核心脚本
   - AI 辅助工具与项目业务代码分离
   - 目录命名清晰，明确标识为 AI 辅助工具

2. **Git 管理灵活**：
   - 可以选择性地提交或忽略整个目录
   - 不影响项目的核心代码库
   - 团队成员可以根据需要选择是否使用

3. **易于维护**：
   - 工具集中管理，便于更新和维护
   - 不会与项目代码产生冲突
   - 便于添加新的 AI 辅助工具

#### 工具生成产物的存放位置

✅ **推荐做法**：将 AI 辅助工具生成的产物（如图片、文档等）统一放在 `.cursor-rules/assets/` 目录下

**为什么使用 `.cursor-rules/assets/` 目录？**

1. **与工具同目录管理**：
   - 工具和工具生成的产物在同一个父目录下，便于统一管理
   - 清晰区分项目核心资源和 AI 辅助工具产物
   - 避免污染项目根目录的 `assets/` 目录

2. **便于文档引用**：
   - 文档可以使用相对路径引用图片
   - 例如：`![架构图](../.cursor-rules/assets/batch-logger/架构图.png)`
   - 路径清晰，便于维护

3. **统一的 Git 管理**：
   - 可以统一决定是否提交 `.cursor-rules/` 目录
   - 如果提交，工具和产物一起提交；如果不提交，则一起忽略
   - 避免在 `.gitignore` 中添加多个规则

**产物类型和存放位置**：

1. **Mermaid 生成的图片**：
   - ✅ 推荐：`.cursor-rules/assets/project-name/` 或 `.cursor-rules/assets/batch-logger/`
   - ❌ 禁止：项目根目录的 `assets/` 目录
   - 原因：避免与项目业务资源混淆

2. **文档工具生成的文件**：
   - ✅ 推荐：`.cursor-rules/assets/docs/`
   - ❌ 禁止：项目 `docs/` 目录下混入工具生成的临时文件

3. **其他辅助工具产物**：
   - ✅ 推荐：`.cursor-rules/assets/tool-name/`
   - 按工具名称分目录存放

**注意事项**：

1. **脚本文件不应复制到项目**：
   - 规则库的脚本（如 `push_cursor_rules.sh`、`sync_rules.sh`）应保留在规则库
   - 不应该复制到项目的 `.cursor-rules/` 目录
   - 如需使用，通过绝对路径调用规则库中的脚本

2. **产物与项目资源的区分**：
   - 项目根目录的 `assets/` 应只包含项目业务资源
   - AI 辅助工具生成的产物应放在 `.cursor-rules/assets/`

3. **文档引用路径**：
   - 在项目文档中引用图片时，使用相对路径
   - 例如：在 `docs/architecture.md` 中引用 `../.cursor-rules/assets/batch-logger/架构图.png`

#### Git 管理策略

根据团队情况选择合适的策略：

##### 策略1：个人工具（不提交到项目）

**适用场景**：
- 工具仅个人使用
- 其他团队成员有自己的工具习惯
- 避免增加项目依赖

**操作方式**：
在项目的 `.gitignore` 中添加：
```
.cursor-rules/
```

##### 策略2：团队共享（提交到项目）

**适用场景**：
- 团队成员都使用 Cursor AI
- 工具对团队协作有帮助
- 团队愿意统一工具集

**操作方式**：
提交 `.cursor-rules` 目录到项目：
```bash
git add .cursor-rules/utils/
git commit -m "feat: 添加 Cursor AI 辅助开发工具"
```

**注意事项**：
- 在 `.cursor-rules/utils/README.md` 中详细说明工具的用途和依赖
- 说明工具的安装和使用方法
- 标注工具是可选的，不影响项目核心功能

##### 策略3：独立工具仓库

**适用场景**：
- 工具需要在多个项目中使用
- 工具较为复杂，需要独立维护
- 团队有多个项目使用相同的工具

**操作方式**：
- 创建独立的工具仓库
- 在各个项目中通过 git submodule 或其他方式引用
- 集中管理和更新工具

### 项目目录职责划分

#### 核心项目目录

以下目录应**只包含项目核心业务相关的内容**：

1. **`src/`**：源代码目录
   - 只包含业务逻辑代码
   - 不包含 AI 辅助工具或个人脚本

2. **`scripts/`**：项目核心脚本目录
   - 构建脚本（build、compile、bundle）
   - 部署脚本（deploy、publish）
   - 版本管理脚本（version、release）
   - 数据库迁移脚本（migration）
   - 项目维护脚本（cleanup、backup）
   - **禁止**：AI 辅助工具、个人脚本、文档生成工具

3. **`docs/`**：项目文档目录
   - 项目文档、API 文档、使用说明
   - 不包含 AI 生成的临时文档或草稿

4. **`tests/` 或 `test/`**：测试代码目录
   - 单元测试、集成测试、E2E 测试
   - 不包含 AI 辅助的调试脚本

#### AI 辅助开发目录

以下目录用于存放 AI 辅助开发相关的内容：

1. **`.cursor-rules/`**：Cursor AI 配置和工具目录
   - `.cursorrules` 规则文件
   - `utils/` AI 辅助工具目录
   - 工具说明文档

2. **可选的其他 AI 辅助目录**：
   - `.ai-prompts/`：AI 提示词和模板
   - `.ai-tools/`：其他 AI 辅助工具

### 实施指南

#### 在创建新工具时

**必须遵循的流程**：

1. **判断工具性质**：
   - 是项目核心业务需要的工具？ → 放入 `scripts/`
   - 是 AI 辅助开发工具？ → 放入 `.cursor-rules/utils/`
   - 是个人临时脚本？ → 放在项目外或临时目录

2. **创建工具文件**：
   ```bash
   # AI 辅助工具
   mkdir -p .cursor-rules/utils
   touch .cursor-rules/utils/new_tool.sh
   ```

3. **添加工具说明**：
   在 `.cursor-rules/utils/README.md` 中添加工具说明

4. **决定 Git 管理策略**：
   - 个人使用：添加到 `.gitignore`
   - 团队共享：提交到代码库

#### 清理现有污染

**如果发现项目已存在污染**：

1. **识别污染内容**：
   - 检查 `scripts/` 目录中的非核心脚本
   - 检查项目根目录的 `assets/` 目录中的工具生成产物
   - 检查 `.cursor-rules/` 目录中的脚本文件（应该在规则库，不应在项目）
   - 识别 AI 辅助工具或个人脚本

2. **移动到正确位置**：
   ```bash
   # 创建 AI 辅助工具目录和产物目录
   mkdir -p .cursor-rules/utils
   mkdir -p .cursor-rules/assets
   
   # 移动工具文件
   mv scripts/utils/ai_tool.sh .cursor-rules/utils/
   
   # 移动工具生成的产物（如 Mermaid 图片）
   mv assets/batch-logger .cursor-rules/assets/
   mv assets/tool-name .cursor-rules/assets/
   
   # 清理空目录
   rmdir scripts/utils
   # 如果 assets 目录为空，删除它
   rmdir assets 2>/dev/null || true
   ```

3. **清理脚本文件**：
   ```bash
   # 删除复制到项目的规则库脚本
   cd .cursor-rules
   rm -f .push_cursor_rules.sh .push_cursor_rules.sh.backup.*
   rm -f .rest_cursor_rules.sh .rest_cursor_rules.sh.backup.*
   rm -f *.backup.*
   ```

4. **更新文档引用**：
   - 在 `.cursor-rules/utils/README.md` 中添加工具说明
   - 更新项目 README，说明 AI 辅助工具的位置
   - 更新文档中的图片引用路径（从 `assets/` 改为 `../.cursor-rules/assets/`）

5. **更新 .gitignore**（如果不提交）：
   ```bash
   echo ".cursor-rules/" >> .gitignore
   ```

### 检查清单

在提交代码前，使用以下检查清单确保没有项目污染：

- [ ] `scripts/` 目录只包含项目核心脚本（构建、部署、版本管理等）
- [ ] AI 辅助工具已移动到 `.cursor-rules/utils/` 目录
- [ ] 工具生成的产物已移动到 `.cursor-rules/assets/` 目录
- [ ] 项目根目录的 `assets/` 目录只包含项目业务资源
- [ ] 规则库的脚本文件没有复制到项目的 `.cursor-rules/` 目录
- [ ] 临时调试脚本已删除或移出项目
- [ ] `.cursor-rules/utils/README.md` 包含工具说明
- [ ] `.gitignore` 配置正确（如果不提交 AI 辅助工具）
- [ ] 项目依赖中没有为 AI 辅助工具添加的不必要依赖

### 常见问题

#### Q1：什么样的工具应该放在 `scripts/` 目录？

**A1**：只有项目核心业务需要的脚本才应该放在 `scripts/` 目录，包括：
- 构建脚本（build.sh、compile.js）
- 部署脚本（deploy.sh、publish.js）
- 版本管理脚本（version.js、release.sh）
- 数据库迁移脚本（migration.sql、migrate.js）
- 项目维护脚本（cleanup.sh、backup.sh）

这些脚本是项目功能的一部分，应该版本控制并团队共享。

#### Q2：什么样的工具应该放在 `.cursor-rules/utils/` 目录？

**A2**：AI 辅助开发过程中使用的工具，包括：
- 文档生成工具（Mermaid 转换、文档格式化）
- AI 调试工具（日志分析、代码分析）
- 开发辅助工具（代码模板生成、重复代码检查）
- 个人使用的开发工具

这些工具不是项目核心功能，可以选择性地使用和提交。

#### Q3：如果团队都使用 Cursor AI，是否应该提交 `.cursor-rules` 目录？

**A3**：可以提交，但需要注意：
- 在 README 中说明这是 AI 辅助工具，不影响项目核心功能
- 说明工具的依赖和安装方法
- 标注工具是可选的，团队成员可以选择使用或不使用
- 定期更新工具说明文档

#### Q4：如果工具需要在多个项目中使用，如何管理？

**A4**：建议创建独立的工具仓库：
- 创建一个专门的 AI 辅助工具仓库
- 在各个项目中通过 git submodule 或其他方式引用
- 集中管理和更新工具，避免在多个项目中重复维护

### 重要原则

1. **职责分离**：项目核心代码与 AI 辅助工具必须分离
2. **保持纯净**：项目目录结构应保持纯净，不包含非业务相关的内容
3. **灵活管理**：AI 辅助工具应支持灵活的 Git 管理策略
4. **清晰标识**：AI 辅助工具应有清晰的目录标识和说明
5. **易于维护**：工具应集中管理，便于更新和维护

### 注意事项

1. **强制要求**：所有 AI 辅助工具必须放在 `.cursor-rules/utils/` 目录
2. **禁止混入**：禁止将 AI 辅助工具混入项目 `scripts/` 目录
3. **及时清理**：发现项目污染时，应立即清理
4. **文档说明**：AI 辅助工具必须有完整的说明文档
5. **团队沟通**：提交 AI 辅助工具前，应与团队成员沟通并达成共识