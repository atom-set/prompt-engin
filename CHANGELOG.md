# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

