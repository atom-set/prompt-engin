# Context Engine - 简单介绍

> **创建时间**: 2025-12-31（本地时间）

---

## 概述

**Context Engine** 是系统化上下文工程实践的开源工程，帮助开发者从传统的提示词工程（Prompt Engineering）升级到系统化的上下文工程（Context Engineering）。

**核心价值**：Context Engine 通过工程化实践，将分散的上下文规则集中管理，实现模块化复用、版本统一、批量同步，维护效率显著提升。

## 什么是上下文工程

**上下文工程**是系统化管理和组织 AI 上下文规则的方法论，通过集中管理、结构化组织、版本控制等工程化手段，实现上下文规则的可复用、可维护、可扩展。

**核心升级路径**：
- **从分散的提示词** → **系统化的上下文规则**
- **从手动维护** → **工程化管理和自动化同步**
- **从单一配置** → **个性化适配和按需加载**

## 核心价值

### 系统化管理
集中管理上下文规则，一次修复，全项目同步，维护成本从 **O(n) 降至 O(1)**。

### Token 优化
精简版 + 技能系统，Token 占用减少 **60.1%**，提升 AI 响应速度。

### 个性化适配
按角色、阶段选择技能，精准适配不同需求（新手开发者、资深开发者、不同开发阶段）。

### 多平台支持
支持 Cursor IDE、TRAE IDE、Antigravity IDE，自动格式转换（Markdown、YAML）。

## 工程化方法论

Context Engine 的核心方法论：

- **模块化**：上下文规则按功能模块拆分，支持独立维护和复用
- **版本控制**：使用 Git 进行版本管理，支持版本回退和协作
- **批量同步**：提供工具脚本，实现一键同步到多个项目
- **标准化**：建立统一的规范体系，提升团队协作效率
- **持续改进**：集中修复漏洞，自动同步到所有项目

## 快速开始

### 方式1：完整版规则（适合小项目）

```bash
python3 scripts/prompt-engine merge --ide cursor --output .cursorrules
cp .cursorrules /path/to/your-project/
```

### 方式2：精简版 + 技能系统（推荐）

```bash
# 生成精简版规则
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 复制到项目
cp .cursorrules /path/to/your-project/

# 按需安装技能（可选）
# 参考 docs/milestones/V1_SKILL/ 目录下的技能系统指南
```

### 方式3：多文件目录（精细控制）

```bash
python3 scripts/prompt-engine merge --ide cursor --output-dir .cursor/rules/
```

## 适用场景

- ✅ **团队协作**：统一上下文规则，提升团队协作效率
- ✅ **新项目初始化**：快速建立标准化的上下文规则体系
- ✅ **大项目 Token 优化**：通过精简版和技能系统减少 Token 占用
- ✅ **多项目维护**：集中管理，批量同步，降低维护成本

## 相关资源

- **项目仓库**：https://gitlab.rd.chanjet.com/cc_web/prompt-engin
- **快速开始指南**：`QUICK_START.md`
- **技能系统指南**：`docs/milestones/V1_SKILL/`
- **完整文档**：项目 `docs/` 目录

