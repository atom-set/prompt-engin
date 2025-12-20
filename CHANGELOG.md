# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- **重点推荐方式2（精简版规则文件 + 技能系统）**（2025-12-20）：
  - 调整所有文档顺序，将方式2（精简版规则文件 + 技能系统）放在方式1之前
  - 更新推荐说明，重点推荐方式2，添加星号（⭐）和"重点推荐"标识
  - 更新选择建议：所有项目（推荐）→ 使用方式2
  - 更新的文档：
    - `README.md`：技能系统部分重点推荐方式2
    - `QUICK_START.md`：调整推荐顺序
    - `docs/guides/skills-usage-guide.md`：调整推荐说明和顺序
    - `docs/guides/token-optimization-guide.md`：调整推荐说明和顺序
    - `docs/guides/QUICK_START_SKILLS.md`：调整推荐说明和顺序
    - `docs/guides/USAGE_EXAMPLE.md`：调整示例顺序
  - **推荐理由**：
    - Token 占用减少约 60%（从 8597 行减少到 3427 行）
    - 按需加载，灵活配置
    - 推荐用于所有项目，特别是大项目

### Removed
- **删除无用文档**（2025-12-20）：
  - 删除 `docs/guides/user-guide.md`：与 README.md 和 QUICK_START.md 内容重复
  - 删除 `prompts/OPTIMIZATION_PLAN.md` 和 `prompts/OPTIMIZATION_SUMMARY.md`：优化方案文档已整合
  - 删除 `TEST_AND_SANITIZATION_REPORT.md`：测试报告文档
  - 删除临时文件：`combined.md`、`common.md`

### Fixed
- **修复文档引用**（2025-12-20）：
  - 修复不存在的文档引用：`skill-capability-sync-plan-2025-12-20.md`
  - 更新所有对 `user-guide.md` 的引用，指向 `QUICK_START.md`
  - 更新的文件：
    - `README.md`：更新文档引用
    - `PROMPTS_OVERVIEW.md`：更新文档引用
    - `prompts/README.md`：更新文档引用
    - `docs/examples/todo-cli-vaildation/README.md`：更新文档引用
    - `PROJECT_SETUP.md`：更新文档引用
    - `CHANGELOG.md`：更新技能系统实施方案说明
    - `docs/guides/skills-usage-guide.md`：更新相关文档链接
    - `docs/guides/QUICK_START_SKILLS.md`：更新相关文档链接
    - `docs/guides/token-optimization-guide.md`：更新相关文档链接
    - `docs/guides/SKILLS_CREATION.md`：更新相关文档链接

### Added
- **技能系统（Skills）支持**（2025-12-20）：
  - 添加技能系统支持，实现 Token 优化和按需加载
  - 创建 `AGENTS.md` 文件：技能列表定义文件
  - 创建 `scripts/skills_sync/sync_skill.py`：技能同步脚本
  - 创建 `scripts/utils/convert_rule_to_skill.py`：规则转技能工具
  - 创建 `docs/guides/token-optimization-guide.md`：Token 优化指南
  - 创建 `docs/guides/skills-usage-guide.md`：技能使用指南
  - 技能系统实施方案：完整的实施方案已整合到相关指南文档中
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
- 修复 `prompts/stages/common/mode/common/mode-common.md` 缺少概述部分的验证问题
- 添加概述部分，使文件符合提示词格式规范

### Added (Previous)
- 添加 `TEST_AND_SANITIZATION_REPORT.md` 自测和脱敏检查报告

## [0.2.0] - 2025-12-15

### Added
- 添加隐藏的同步工具 `.sync_from_cursor_rules.py`，支持从 cursor-rules 仓库同步提示词
- CLI 工具新增 `--all` 选项，支持合并所有提示词文件
- 创建包装脚本 `scripts/prompt-engine`，无需安装即可使用 CLI 工具
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

