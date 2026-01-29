# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-01-29

### ✨ 新增功能

#### 优先级机制
- ✅ 为所有 skills 添加 `priority` 字段（1-4 级）
- ✅ 更新 YAML 工具支持 priority 字段解析和验证
- ✅ 更新 skills_analyzer 优先从 frontmatter 读取 priority
- ✅ 优先级分类：
  - Priority 1: 核心规则（3 个）- 必须首先应用
  - Priority 2: 模式规则（4 个）- 按模式条件应用
  - Priority 3: 代码标准（8 个）- 编写代码时自动应用
  - Priority 4: 领域技能（16 个）- 按需加载

#### AGENTS.md 自动生成
- ✅ 新增 `skill-engine generate` 命令，自动生成 AGENTS.md
- ✅ 支持 Cursor IDE 和 Claude Desktop 两个平台
- ✅ 自动包含所有 skills 的优先级信息
- ✅ 按优先级分组组织 skills 列表

#### 核心规则领域（core/）
- ✅ 新增 `skills/core/` 目录，包含 15 个核心规则
- ✅ 核心规则包括：
  - 工具权限系统（tool-permission-system）
  - 模式通用规则（mode-common）
  - 安全权限规则（security-permissions）
  - 模式规则（plan-mode, act-mode, solution-output, file-write）
  - 代码标准（code-format, naming, function-design, comments, error-handling-*）

### 🔧 改进

#### Skills 系统
- ✅ 更新所有 31 个 skills 添加 priority 字段
- ✅ 更新 SKILL_TEMPLATE.md 包含 priority 字段说明
- ✅ 更新 skills/README.md 添加优先级机制说明
- ✅ 验证命令现在显示 priority 字段

#### CLI 工具
- ✅ 新增 `generate` 命令用于生成 AGENTS.md
- ✅ 优化验证命令显示 priority 信息
- ✅ 更新帮助文档

#### 文档
- ✅ 更新 README.md 反映新功能
- ✅ 更新技能数量统计（16 → 31 个）
- ✅ 添加优先级机制说明
- ✅ 添加 AGENTS.md 生成说明
- ✅ 添加平台兼容性说明（Cursor + Claude Desktop）

### 🧹 清理

- ✅ 删除 `skills-old/` 旧版本备份目录（396KB）
- ✅ 删除临时报告文件（6 个）
- ✅ 清理未使用的代码导入（Dict, List）

### 📊 统计数据更新

- **Skills**: 从 16 个增加到 31 个（新增 15 个核心规则）
- **领域**: 从 5 个增加到 6 个（新增 core 领域）
- **平台支持**: Cursor IDE + Claude Desktop

## [2.0.0] - 2026-01-27

### 🚀 重大变更（Breaking Changes）

#### 架构重构
- **完全移除 Prompts 系统** - 不再支持 prompts 目录和相关功能
- **统一为 Skills 系统** - 所有规则以 skill 格式组织，共 16 个 skills
- **不向下兼容** - v1.x 用户需要迁移到 v2.0

#### Skills 转换与领域分层
- ✅ 已将所有 prompts 规则转换为 skills 格式（16 个）
- ✅ 采用**领域驱动**的组织方式，按功能领域分类：
  - `code/` - 代码开发领域（3 个 skills）
  - `documentation/` - 文档领域（5 个 skills）
  - `workflow/` - 工作流程领域（5 个 skills）
  - `interaction/` - 交互领域（2 个 skills）
  - `project/` - 项目管理领域（1 个 skill）
- ✅ 更加扁平化的目录结构，只有两层，易于浏览和管理
- ✅ 每个领域都有独立的 README.md，说明该领域的所有 skills
- ✅ 所有 skills 都可通过 `openskills` 命令或 `skill-engine` CLI 使用

#### Skills 格式升级
- ✅ 所有 16 个 skills 已升级为标准格式
- ✅ 每个 skill 包含：
  - YAML frontmatter（name、description、tags）
  - 使用场景说明
  - 触发条件说明
  - 与其他规则的配合说明
  - 完整的规则内容
- ✅ 创建标准 skill 模板（`skills/SKILL_TEMPLATE.md`）

#### 目录结构重构
- ✅ 删除 prompts 相关的遗留文件和目录
- ✅ 简化项目结构，只保留 skills 相关内容
- ✅ 删除过时的文档和示例
- ✅ 创建 `backup/` 目录，归档无用和不相关的文件（共 508KB）：
  - `test-artifacts/` - 测试覆盖率报告（372KB，可重新生成）
  - `deprecated-scripts/` - 已废弃的脚本（36KB: skills_sync, install_all_skills.sh）
  - `docs-old/` - 旧版本文档（96KB: docs/, CONTRIBUTING.md）
  - 添加到 `.gitignore`，不提交到版本控制
- ✅ 清理过时的 Markdown 文档：
  - 移除 `docs/` 目录（11 个文件，与 v2.0 不符）
  - 移除 `CONTRIBUTING.md`（提到旧的命名）
  - 只保留核心文档：README.md, QUICK_START.md, CHANGELOG.md, AGENTS.md
- ✅ 将 `.claude/` 目录添加到 `.gitignore`（Cursor IDE 个人配置，不应纳入版本控制）
- ✅ 将 `.specstory/` 目录添加到 `.gitignore`（AI 聊天历史，7.5MB，不应纳入版本控制）
- ✅ 清理构建产物：`htmlcov/`、`src/prompt_engin.egg-info/`
- ✅ 重新生成包信息：`src/skill_engine.egg-info/`（名称已更新）

#### 构建工具重构
- ✅ 重构 skill-engine CLI 工具
- ✅ 新增功能：
  - `skill-engine create` - 创建新 skill
  - `skill-engine validate` - 验证 skill 格式
  - `skill-engine search` - 搜索 skills（按关键词或标签）
  - `skill-engine stats` - 显示统计信息
- ✅ 模块化代码结构：
  - `commands/` - 命令模块
  - `utils/` - 工具函数
- ✅ 完善依赖配置：
  - `setup.py` 添加 `click>=8.0.0` 和 `pyyaml>=6.0` 依赖
  - 与 `requirements.txt` 保持一致

#### 测试覆盖提升
- ✅ 补全单元测试，测试用例从 6 个增加到 76 个
- ✅ 代码覆盖率从 17% 提升到 75%
- ✅ 新增测试文件：
  - `tests/test_cli.py` - CLI 和工具函数测试（22 个测试）
  - `tests/test_commands.py` - 命令模块测试（16 个测试）
  - `tests/test_utils.py` - 工具模块测试（38 个测试）
- ✅ 测试覆盖率详情：
  - `file_utils.py`: 97% 覆盖率
  - `yaml_utils.py`: 97% 覆盖率
  - `list_cmd.py`: 86% 覆盖率
  - `search_cmd.py`: 92% 覆盖率
  - `stats_cmd.py`: 95% 覆盖率
  - `read_cmd.py`: 100% 覆盖率
  - `cli.py`: 66% 覆盖率

#### 删除的功能
- ❌ Prompts 提示词系统（整个 `prompts/` 目录）
- ❌ Prompts 合并功能（`merge_prompts.sh`）
- ❌ `.cursorrules` 文件生成功能
- ❌ Prompts 验证功能（`validate_prompts.sh`）
- ❌ 旧的 CLI 工具（已改为 `skill-engine`）
- ❌ 规则转换工具（`convert_rule_to_skill.py`）

#### 新增的功能
- ✅ 重构的 Skills 系统（更清晰、更易用）
- ✅ 新的 `skill-engine` CLI 工具
- ✅ 完整的 Skills 文档体系
- ✅ 简化的项目结构

### 📚 文档更新
- ✅ 完全重写 README.md（以 Skills 为中心）
  - 精简冗余内容（384 行 → 197 行）
  - 补充详细的使用说明和实际场景（302 行）
  - 补充项目集成和部署说明（462 行 → 437 行）
  - 采用 **clone + sync** 部署模式（统一管理，按需同步）
  - 提供完整的团队协作流程和多项目使用方案
  - 添加典型使用流程和组合使用示例
- ✅ 完全重写 QUICK_START.md（5 分钟快速开始）
- ✅ 新增 `scripts/sync.sh` - 自动同步脚本
  - 复制 `skills/` 目录到目标项目
  - 复制 `AGENTS.md` 配置文件
  - 智能检测冲突并提示确认
  - 显示同步统计信息和后续操作提示
- 新增 Skills 使用最佳实践

### 🔧 代码重构
- 重命名 `prompt_engine` → `skill_engine`
- 简化 CLI 工具，只保留 skills 相关功能
- 移除所有 prompts 相关代码
- 删除 `merger.py`、`generator.py`、`parser.py`、`validator.py`

### 📦 配置更新
- 更新版本号为 2.0.0
- 更新项目描述为 "Skills-based AI Skill Engine Framework"
- 简化依赖关系

### 📖 迁移指南

**v1.x 用户请注意**：

1. **不向下兼容** - v2.0 是完全重构的版本
2. **使用方式变更**：
   - ❌ 不再使用 `.cursorrules` 文件
   - ✅ 改用 `openskills` 命令或 `skill-engine` CLI
3. **规则格式变更** - 所有规则需要以 skill 格式重新组织

**v1.x 用户建议**：
- 继续使用 v1.x 分支（保持可用）
- 或者迁移到 v2.0（需要重新学习）

**v2.0 快速开始**：
```bash
# 克隆仓库
git clone https://github.com/your-org/skill-engine.git
cd skill-engine

# 安装依赖
pip install -r requirements.txt
pip install -e .

# 使用 skills
Bash("openskills read <skill-name>")
```

详见 [QUICK_START.md](QUICK_START.md)

---

## [Unreleased]

### Added
- **创建自定义技能命令说明**（2026-01-20）：
  - 在 README.md 中添加"创建自定义技能"小节
  - 提供规则转技能工具的基本命令格式和使用示例
  - 包含 3 个具体使用示例（文档格式、时间格式、代码组织规范）
  - 添加参数说明和批量转换方法
  - 提供验证生成技能的方法
- **快速使用提示词支持**（2025-12-23）：
  - 在 README.md 中添加 `.cursorrules.all` 和 `.cursorrules.core` 快速使用说明
  - 提供两种版本的对比表格（行数、大小、Token 占用、功能完整性等）
  - 说明两种版本的使用方法和适用场景
  - 支持直接复制使用或在 Cursor IDE 中通过 `@文件名` 引用
  - **版本说明**：
    - `.cursorrules.all`：完整版规则（8597 行，约 328KB），推荐用于新项目
    - `.cursorrules.core`：核心版规则（3427 行，约 131KB），推荐用于已有项目，Token 占用减少约 60%
- **技能系统（Skills）支持**（2025-12-20）：
  - 添加技能系统支持，实现 Token 优化和按需加载
  - 创建 `AGENTS.md` 文件：技能列表定义文件
  - 创建 `scripts/skills_sync/sync_skill.py`：技能同步脚本
  - 创建 `scripts/utils/convert_rule_to_skill.py`：规则转技能工具
  - 创建 `docs/guides/token-optimization-guide.md`：Token 优化指南
  - 创建 `docs/guides/skills-usage-guide.md`：技能使用指南
  - 创建 `docs/guides/skill-capability-sync-plan-2025-12-20.md`：完整的实施方案
  - 创建 `docs/guides/SKILLS_CREATION.md`：技能创建指南
  - 创建 `docs/guides/SKILLS_QUICK_REFERENCE.md`：技能系统快速参考
  - 创建 `docs/guides/SKILLS_LIST.md`：技能列表文档
  - 更新 `README.md`：添加技能系统说明和使用指南
  - 实现 `--core-only` 选项：支持生成精简版规则文件
  - **Token 优化效果**：
    - 初始上下文 token 减少约 60%（从 8597 行减少到 3427 行）
    - 支持按需加载可选规则（转换为技能）
    - 同时支持完整版和精简版规则文件两种方式
  - **规则分类**：
    - 核心规则（~3427 行）：保留在 `.cursorrules` 中，必须全局生效
    - 可选规则（~3770 行）：转换为技能，按需加载
  - **技能创建**：
    - 已创建 16 个技能（第一批 7 个 + 第二批 9 个）
    - 第一批（P0-P1）：`document-format`、`time-format`、`code-organization`、`problem-location`、`design-principles`、`wiki-output`、`document-generation`
    - 第二批（P2）：`project-clean-principle`、`architecture-diagram-template`、`open-question-confirmation`、`modular-output`、`exception-handling`、`compatibility-check`、`file-reading`、`phase-implementation`、`time-check`
  - **批量安装脚本**：
    - 创建 `scripts/utils/install_all_skills.sh`：支持批量安装技能
    - 创建 `docs/guides/BATCH_INSTALL_GUIDE.md`：批量安装指南
    - 创建 `docs/guides/TROUBLESHOOTING.md`：故障排查指南
    - **功能特性**：
      - 支持全选安装（选项 1）：一次性安装所有技能
      - 支持选择性安装（选项 2）：交互式选择要安装的技能（输入技能编号，如：`1,3,5`）
      - 显示安装进度和结果统计
      - 详细的错误提示和故障排查链接
    - 支持批量安装技能，然后通过 `openskills sync -y` 选择使用哪些技能
  - **使用方式**：
    - 方式1：完整版规则文件（简单直接，复制即用）
    - 方式2：精简版规则文件 + 技能系统（Token 优化，按需加载）
- **规则架构顶层重构**（2025-12-19）：
  - 创建 `prompts/stages/common/mode/tool-permission-system.md`：工具权限系统顶层规则文件
    - 定义工具分类体系（只读工具 vs 修改工具）
    - 定义统一检查流程（3步简化版）
    - 定义强制触发机制（在响应生成流程中强制插入检查步骤）
  - 重构 `prompts/stages/common/mode/plan/tool-check.md`：简化检查流程
    - 从 5 步简化为 3 步（工具分类判断 → 权限检查 → 方案完整性检查）
    - 添加命令内容检查机制（`run_terminal_cmd` 必须检查命令内容）
    - 引用工具权限系统顶层规则
  - 重构 `prompts/stages/common/mode/common/mode-common.md`：移除 Debug 模式，添加强制触发机制
    - 移除所有 Debug 模式相关流程和检查
    - 在响应生成流程中强制插入"意图识别和方案输出检查"步骤
    - 简化响应生成流程（从 5 步简化为 4 步）
  - 更新 `prompts/stages/common/mode/plan/solution-output.md`：整合到新架构
    - 添加对工具权限系统和强制触发机制的引用
  - 更新 `prompts/stages/common/mode/security/security-permissions.md`：移除 Debug 模式
    - 移除所有 Debug 模式相关权限说明
    - 更新工具权限分类，引用工具权限系统
  - 更新 `prompts/stages/common/mode/index.md`：移除 Debug 模式规则索引
    - 添加工具权限系统模块说明
    - 更新依赖关系

### Removed
- **移除 Debug 模式**（2025-12-19）：
  - 删除 `prompts/stages/common/mode/debug/debug-mode.md`
  - 删除 `prompts/stages/common/mode/debug/index.md`
  - 移除所有规则文件中的 Debug 模式相关内容和引用
- **简化架构，移除重复文件**（2025-12-19）：
  - 删除 `prompts/stages/common/mode/plan/tool-check.md`（已整合到 `tool-permission-system.md`）
  - 删除 `prompts/stages/common/mode/plan/forbidden-behaviors.md`（已整合到 `tool-permission-system.md`）
  - 删除 `prompts/stages/common/mode/plan/solution-completeness.md`（已整合到 `solution-output.md`）

### Changed
- **修复规则漏洞：禁止在同一响应中输出方案后立即调用修改工具**（2025-12-24）：
  - 修复 `prompts/stages/common/mode/tool-permission-system.md` 中的规则漏洞：
    - 禁止在同一响应中输出方案后立即调用修改工具
    - 强化跨响应检查机制，明确要求输出方案后必须等待用户输入 "Act" 指令
    - 在方案完整性检查中添加强制检查：方案输出和工具调用必须在不同响应中
  - 修复 `prompts/stages/common/mode/common/mode-common.md` 中的模式切换规则：
    - 明确默认模式原则：系统默认以Plan模式开始，无Act指令时统一按Plan模式处理
    - 简化模式判断规则，禁止复杂判断，只需检查是否有"Act"指令
    - 明确禁止的行为：不能假设用户意图，不能使用其他指令作为切换条件
  - 更新 `.cursorrules` 文件，同步规则修复
- **修复分阶段实施规则漏洞**（2025-12-23）：
  - 修复 `prompts/stages/common/mode/act/phase-implementation.md` 中的 4 个漏洞：
    - 漏洞1：用户说"继续X阶段"的歧义处理 - 明确必须先询问测试
    - 漏洞2：阶段完成的标准不明确 - 明确阶段完成的判断标准
    - 漏洞3：子任务和阶段的区别不明确 - 明确"阶段"和"子任务"的定义
    - 漏洞4：测试询问的时机不够明确 - 明确测试询问的时机和处理方式
  - 新增 `prompts/stages/common/mode/act/phase-implementation-验证报告.md` 验证报告文档
  - 完善阶段完成后的检查清单，添加强制要求说明
  - 更新重要原则，禁止跳过测试确认环节（除非用户明确表示）
- **完善意图识别机制**（2025-12-19）：
  - 重构 `prompts/stages/common/mode/tool-permission-system.md`：完善意图识别失败时的安全机制
    - 将意图识别整合为检查流程第零步（在工具分类判断之前）
    - 检查流程从 3 步扩展为 4 步（第零步：意图识别检查）
    - 量化触发条件的判断标准（明确何时触发安全机制）
    - 明确误判检测机制（基于用户反馈检测误判）
    - 明确询问机制的执行时机和方式（在响应生成时询问）
    - 明确模式切换时机（检测到失败时立即切换）
    - 明确与方案输出的关系（失败时作废方案）
    - **添加强制确认机制**（2025-12-19）：
      - 意图识别失败时，必须与用户确认（不能跳过）
      - 定义标准确认格式（提供明确选项，至少 3 个选项）
      - 明确确认时机、确认方式、确认内容
      - 明确回复判断逻辑（根据用户选择执行对应流程）
      - 明确确认后的处理流程（重新识别 → 从第零步重新开始）
      - 添加重新识别次数限制（最多 2 次，避免无限循环）
    - **优化询问机制和确认机制**（2025-12-19）：
      - 统一询问机制格式（与确认机制保持一致，可使用简化版本）
      - 为询问机制添加推荐格式（与确认机制保持一致）
      - 明确确认后的完整流程（重新识别成功/失败的处理方式）
      - 完善检查结果说明（明确确认后的处理流程）
      - 优化询问机制和确认机制的关系说明（明确两者的区别和联系）
      - 在错误处理部分添加确认后的处理流程说明
- **规则架构顶层重构**（2025-12-19）：
  - 重构 `prompts/stages/common/mode/tool-permission-system.md`：整合所有检查机制
    - 整合工具调用检查机制（从 `tool-check.md`）
    - 整合禁止行为清单（从 `forbidden-behaviors.md`）
    - 整合意图识别和方案输出机制
    - 成为工具调用检查的唯一入口
  - 重构 `prompts/stages/common/mode/common/mode-common.md`：简化响应生成流程
    - 移除意图识别和方案输出检查步骤（在工具调用时执行）
    - 简化响应生成流程（从 4 步简化为 3 步）
  - 重构 `prompts/stages/common/mode/plan/solution-output.md`：聚焦方案输出内容
    - 移除意图识别机制（已整合到 `tool-permission-system.md`）
    - 整合方案完整性判断标准（从 `solution-completeness.md`）
    - 聚焦方案输出的内容要求（5个部分的具体格式）
  - 重构 `prompts/stages/common/mode/security/security-permissions.md`：移除重复检查流程
    - 移除详细的检查流程定义（只保留快速参考）
    - 引用 `tool-permission-system.md` 作为详细说明
    - 同步检查清单，与 `tool-permission-system.md` 保持一致
    - 更新文件头部的更新时间说明
- **规则架构简化重构**（2025-12-19）：
- 添加 IDE 适配支持功能，支持生成适用于不同 AI 辅助 IDE 的规则文件
  - 支持生成 Cursor IDE 规则文件（`.cursorrules`）
  - 支持生成 TRAE IDE 规则文件（`.traerules`）
  - 支持生成 Antigravity IDE 规则文件（`.antigravityrules`）
  - CLI 工具新增 `--ide` 选项，支持指定 IDE 格式（cursor/trae/antigravity/both/all）
  - 支持同时生成多个 IDE 规则文件（`both` 选项生成 Cursor 和 TRAE，`all` 选项生成所有三个 IDE）
- 添加 `docs/examples/todo-cli-vaildation/` 提示词规则验证项目，包含完整的验证方案和工具
  - 添加 `quick-start.md` 快速开始指南，5 分钟快速上手验证
  - 添加 `rule-validation-guide.md` 完整验证指南，包含所有验证场景和预期行为
  - 添加 `prompts-collection.md` 提问词集合，可直接复制使用
  - 添加 `README.md` 项目说明文档
- 添加 `.cursorrules`、`.traerules`、`.antigravityrules` 合并后的规则文件，方便在不同 IDE 中使用
- 添加 `PROMPTS_OVERVIEW.md` 提示词概述文档，包含所有提示词的详细描述和应用场景
- 在 README.md 中添加提示词概述文档的链接，方便用户快速访问
- 添加 `prompts/OPTIMIZATION_PLAN.md` 和 `prompts/OPTIMIZATION_SUMMARY.md` 优化方案和总结文档
- 添加 `rules.antigravityrules`、`rules.cursorrules`、`rules.traerules` 规则文件到版本控制

### Changed
- 增强 `PromptMerger` 类，添加 `ide_format` 参数，支持生成不同 IDE 格式的文件头
- 增强 `PromptMerger` 类，在合并时根据 IDE 类型动态替换文件引用（如 `.cursorrules` → `.traerules` 或 `.antigravityrules`）
- 增强 CLI `merge` 命令，添加 `--ide` 选项，支持生成多种 IDE 规则文件
- 更新 README.md，添加 IDE 适配支持章节，详细说明 Cursor、TRAE 和 Antigravity IDE 的使用方法
- 增强 `prompts/stages/common/mode/common/mode-common.md`，添加"语言要求"章节，强制要求所有响应使用中文
- 增强 `prompts/stages/common/code/problem-location/problem-location.md` 问题定位规范，添加"问题分析阶段的约束"：
  - 明确要求：在问题分析阶段，只添加日志，不要修改代码逻辑，也不要添加防御性代码
  - 明确允许的操作：添加日志输出、临时变量、注释、断点
  - 明确禁止的操作：禁止修改代码逻辑、禁止添加防御性代码、禁止修改业务逻辑、禁止添加修复代码
- 增强 `prompts/stages/common/mode/plan/solution-output.md` 方案输出机制：
  - 在修改方案部分添加"设计原则"强制要求，必须优先考虑最简单的设计方案
  - 要求复杂方案必须明确说明使用场景和理由
  - 要求必须对比简单方案和复杂方案，说明选择理由
  - 禁止因为"未来可能需要"而采用复杂方案
- 增强 `prompts/stages/common/mode/plan/tool-check.md` 工具调用检查机制，添加方案输出前置检查
- 整合 `prompts/stages/common/mode/act/long-text-check.md` 到 `file-write.md`，文件大小检查作为写入前的第一步
- 增强 `prompts/stages/common/mode/security/security-permissions.md` 安全权限规则，完善规则优先级说明
- 更新 README.md，添加验证项目说明和使用指南
- 更新 `pyproject.toml`，完善项目配置
- 增强 `PROMPTS_OVERVIEW.md` 提示词概述文档，为部分重要提示词规则添加"如何提问"部分，指导用户如何提问才能有效命中相应的提示词规则
- **优化和整合提示词规则**（2025-12-19）：
  - 整合文件写入规则：将 `long-text-check.md` 整合到 `file-write.md`，文件大小检查作为写入前的第一步，提供完整的文件写入流程（检查大小 → 选择策略 → 写入框架 → 填充内容 → 验证）
  - 优化时间相关规则：在 `time-check.md` 中引用 `time-format.md`，减少重复内容，明确职责边界（通用规范 vs 检查流程）
  - 明确文档阶段规范主次关系：`document-generation.md` 作为整合版推荐优先使用（⭐⭐⭐），`architecture-diagram-template.md` 和 `wiki-output.md` 作为快速参考（⭐⭐）
  - 重组 `PROMPTS_OVERVIEW.md` 模式规则分类方式：从按 Plan/Act/Debug 模式分类改为按功能/使用场景分类（方案输出和计划、代码执行和文件操作、模式切换和响应格式、工具调用和安全检查），使文档更直观
  - 更新 `PROMPTS_OVERVIEW.md` 反映最新架构变更（2025-12-19）：
    - 替换 `tool-check.md` 和 `forbidden-behaviors.md` 的描述为 `tool-permission-system.md`（工具权限系统）
    - 删除 `solution-completeness.md` 的独立描述（已整合到 `solution-output.md`）
    - 删除 `long-text-check.md` 的独立描述（已整合到 `file-write.md`）
    - 删除 Debug 模式的描述（已移除）
    - 添加 `tool-permission-system.md` 的详细描述，包括工具分类体系、4 步检查流程、意图识别机制、强制确认机制等
    - 更新统计信息：总文件数从 63 更新为 60，模式规则文件数从 16 更新为 13
    - 更新更新日志，添加规则架构顶层重构和意图识别机制完善的详细说明
  - 更新 `prompts/README.md`：添加详细的目录结构说明和文档生成规范章节
  - 更新相关索引文件：`mode/act/index.md`、`documentation/README.md` 等
  - 添加技术方案文档模板：`templates/technical-solution-template.md`，包含完整模板和 AI 使用提示词
  - 添加文档生成规范整合版：`stages/documentation/document-generation.md`，整合所有文档类型的规范

### Removed
- 删除 `prompts/stages/common/mode/act/long-text-check.md`（已整合到 `file-write.md`）

### Fixed
- 修复 `scripts/sync.sh` 脚本大小写兼容性问题（2026-01-29）：
  - 修复用户输入 "Y"（大写）时无法正确识别为确认的问题
  - 使用 `tr` 命令替代 `${response,,}` 语法，提升 macOS bash 兼容性
  - 现在支持 "y" 和 "Y" 两种输入方式
- 修复 `prompts/stages/common/mode/common/mode-common.md` 缺少概述部分的验证问题
- 添加概述部分，使文件符合提示词格式规范

### Added (Previous)
- 添加 `TEST_AND_SANITIZATION_REPORT.md` 自测和脱敏检查报告

## [0.2.0] - 2025-12-15

### Added
- 添加隐藏的同步工具 `.sync_from_cursor_rules.py`，支持从 cursor-rules 仓库同步提示词
- CLI 工具新增 `--all` 选项，支持合并所有提示词文件
- 创建包装脚本 `scripts/skill-engine`，无需安装即可使用 CLI 工具
- 添加 `QUICK_START.md` 快速开始指南
- 添加 `AI_GENERATED.md` AI 生成说明文档
- 添加 `PROJECT_SETUP.md` 项目初始化总结文档

### Fixed
- 修复 `generator.py` 中缺少 `List` 类型导入的问题
- 修复 CLI 工具在没有参数时的错误提示，提供更友好的帮助信息
- 修复 `pyproject.toml` 中的包路径配置问题

### Changed
- 改进 merge 命令的错误提示，显示所有可用选项和示例
- 更新 README.md，添加两种使用方式说明（包装脚本和安装后使用）
- 优化 CLI 工具的用户体验

### Documentation
- 更新 README.md 使用示例
- 创建 QUICK_START.md 快速开始指南
- 添加 AI 生成说明到多个文档
- 更新 prompts/README.md 说明所有提示词由 AI 生成

## [0.1.0] - 2025-12-01

### Added
- 项目初始化
- 初始项目结构
- 提示词模板目录结构（按阶段和类型组织）
- 核心代码框架（解析器、合并器、验证器、生成器）
- CLI 工具基础框架
- 基础文档和示例
- README 和 LICENSE
- 基础配置文件（pyproject.toml, requirements.txt, .gitignore 等）
- 测试框架和 CI/CD 配置

