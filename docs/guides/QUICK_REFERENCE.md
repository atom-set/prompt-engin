# 快速参考

> **创建时间**：2025-12-24（本地时间）  
> **最后更新**：2025-12-24（本地时间）

---

## 概述

本文档提供 Prompt Engine 的快速参考卡片，包括常用命令、脚本使用、文件路径等，方便快速查找。

---

## 📋 常用命令速查

### CLI 工具命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `list` | 列出所有提示词文件 | `python3 scripts/prompt-engine list` |
| `merge` | 合并提示词文件 | `python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules` |
| `validate` | 验证提示词文件格式 | `python3 scripts/prompt-engine validate prompts/` |

### 脚本命令

| 脚本 | 说明 | 示例 |
|------|------|------|
| `test_environment.sh` | 环境测试 | `bash scripts/utils/test_environment.sh` |
| `generate_dist.sh` | 生成产物 | `bash scripts/utils/generate_dist.sh --all` |
| `sync_to_project.sh` | 同步到项目 | `bash scripts/utils/sync_to_project.sh --platform cursor --mode single-core /path/to/project` |
| `validate_prompts.sh` | 验证提示词格式 | `bash scripts/utils/validate_prompts.sh` |
| `test_sync_scripts.sh` | 测试同步脚本 | `bash scripts/utils/test_sync_scripts.sh` |

---

## 🚀 快速开始

### 方式1：单文件完整版（最简单）

```bash
# 从 dist 目录复制（推荐）
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules
```

### 方式2：单文件精简版 + 技能（推荐）⭐

```bash
# 1. 复制精简版规则
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 2. 安装技能
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 3. 同步技能
cd /path/to/your-project
openskills sync -y
```

### 方式3：多文件目录

```bash
# 1. 生成产物
bash scripts/utils/generate_dist.sh --platform cursor --mode multi-files

# 2. 同步到项目
bash scripts/utils/sync_to_project.sh --platform cursor --mode multi-files /path/to/your-project
```

---

## 📁 重要文件路径

### 项目文件

| 路径 | 说明 |
|------|------|
| `prompts/` | 提示词源文件目录 |
| `dist/` | 生成的产物目录 |
| `scripts/utils/` | 工具脚本目录 |
| `docs/guides/` | 文档指南目录 |

### 产物文件

| 路径 | 说明 |
|------|------|
| `dist/cursor/single-full/.cursorrules.all` | Cursor 完整版规则文件 |
| `dist/cursor/single-core/.cursorrules.core` | Cursor 精简版规则文件 |
| `dist/cursor/multi-files/rules/` | Cursor 多文件规则目录 |
| `dist/trae/single-full/.traerules.all` | TRAE 完整版规则文件 |
| `dist/antigravity/single-full/.antigravityrules.all` | Antigravity 完整版规则文件 |

---

## 🔧 常用操作

### 生成产物

```bash
# 生成所有平台的三种方式产物
bash scripts/utils/generate_dist.sh --all

# 生成特定平台的产物
bash scripts/utils/generate_dist.sh --platform cursor

# 生成特定方式的产物
bash scripts/utils/generate_dist.sh --mode single-core
```

### 同步到项目

```bash
# 交互式选择
bash scripts/utils/sync_to_project.sh /path/to/your-project

# 指定平台和方式
bash scripts/utils/sync_to_project.sh --platform cursor --mode single-core /path/to/your-project

# 预览模式（不实际同步）
bash scripts/utils/sync_to_project.sh --platform cursor --mode single-core --dry-run /path/to/your-project
```

### 环境测试

```bash
# 运行环境测试
bash scripts/utils/test_environment.sh

# 运行同步脚本测试
bash scripts/utils/test_sync_scripts.sh
```

---

## 📚 文档链接

| 文档 | 路径 |
|------|------|
| 环境安装和测试指南 | `docs/guides/INSTALLATION_AND_TESTING.md` |
| 使用手册 | `docs/guides/USAGE_MANUAL.md` |
| 快速参考 | `docs/guides/QUICK_REFERENCE.md`（本文件） |
| V2 版本改进计划 | `docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md` |
| 项目主文档 | `README.md` |

---

## 🆘 故障排除

### 问题：产物文件不存在

**解决方案**：
```bash
bash scripts/utils/generate_dist.sh --all
```

### 问题：同步失败

**解决方案**：
1. 检查目标目录是否存在
2. 检查产物是否已生成
3. 使用 `--dry-run` 预览操作

### 问题：环境测试失败

**解决方案**：
1. 检查 Python 版本：`python3 --version`
2. 安装依赖：`pip install -r requirements.txt`
3. 查看详细错误信息

---

## 相关文档

- [环境安装和测试指南](./INSTALLATION_AND_TESTING.md) - 环境配置指南
- [使用手册](./USAGE_MANUAL.md) - 详细使用指南
- [README.md](../../README.md) - 项目主文档

---

**最后更新**：2025-12-24（本地时间）

