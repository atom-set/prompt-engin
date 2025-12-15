# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- 添加 `docs/examples/todo-cli-vaildation/` 提示词规则验证项目，包含完整的验证方案和工具
  - 添加 `quick-start.md` 快速开始指南，5 分钟快速上手验证
  - 添加 `rule-validation-guide.md` 完整验证指南，包含所有验证场景和预期行为
  - 添加 `prompts-collection.md` 提问词集合，可直接复制使用
  - 添加 `README.md` 项目说明文档
- 添加 `.cursorrules` 合并后的规则文件，方便在测试项目中使用
- 添加 `PROMPTS_OVERVIEW.md` 提示词概述文档，包含所有提示词的详细描述和应用场景
- 在 README.md 中添加提示词概述文档的链接，方便用户快速访问

### Changed
- 增强 `prompts/stages/common/mode/plan/tool-check.md` 工具调用检查机制，添加方案输出前置检查
- 增强 `prompts/stages/common/mode/plan/solution-output.md` 方案输出机制，添加修改需求判断标准
- 增强 `prompts/stages/common/mode/act/long-text-check.md` 长文本写入检查机制，明确执行时机
- 增强 `prompts/stages/common/mode/security/security-permissions.md` 安全权限规则，完善规则优先级说明
- 更新 README.md，添加验证项目说明和使用指南
- 更新 `pyproject.toml`，完善项目配置
- 增强 `PROMPTS_OVERVIEW.md` 提示词概述文档，为部分重要提示词规则添加"如何提问"部分，指导用户如何提问才能有效命中相应的提示词规则

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

## [0.1.0] - 2025-01-XX

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

