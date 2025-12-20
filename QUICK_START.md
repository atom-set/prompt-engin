# 快速开始指南

## 🎯 推荐说明

Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：

- **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
- **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用

> **重要**：两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

**选择建议**：
- **⭐ 所有项目（推荐）** → 使用方式2（精简版规则文件 + 技能系统）
- **小项目或不需要 token 优化** → 使用方式1（完整版规则文件）

**快速开始**：
- ⭐ **方式2（推荐）**：`python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules`
- 方式1：`python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules`

详细说明请查看 [README.md](./README.md) 中的"技能系统（Skills）支持"章节。

## 使用 CLI 工具

### 方式1：使用包装脚本（推荐，无需安装）

直接使用项目中的包装脚本，无需安装：

```bash
# 查看帮助
python3 scripts/prompt-engine --help

# 列出所有可用的提示词模板
python3 scripts/prompt-engine list

# 合并所有提示词文件
python3 scripts/prompt-engine merge --all --output combined.md

# 按阶段合并
python3 scripts/prompt-engine merge --stage common --output common.md

# 按类型合并
python3 scripts/prompt-engine merge --type frontend --output frontend.md

# 验证提示词格式
python3 scripts/prompt-engine validate prompts/stages/common/

# 根据模板生成提示词
python3 scripts/prompt-engine generate --template prompts/templates/common.md --output output.md
```

### 方式2：安装后使用

如果需要全局使用 `prompt-engine` 命令，可以安装项目：

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 安装项目
pip install -e .

# 现在可以直接使用命令
prompt-engine list
prompt-engine merge --output combined.md
```

## 常见问题

### Q: 提示 `command not found: prompt-engine`

**A:** 项目未安装，请使用方式1（包装脚本）：
```bash
python3 scripts/prompt-engine merge --output combined.md
```

或者按照方式2安装项目。

### Q: 如何添加 PATH 以便直接使用？

**A:** 可以将包装脚本添加到 PATH，或创建符号链接：

```bash
# 创建符号链接（需要安装）
ln -s $(pwd)/scripts/prompt-engine /usr/local/bin/prompt-engine

# 或添加到 PATH（在 ~/.zshrc 或 ~/.bashrc 中）
export PATH="$PATH:$(pwd)/scripts"
```

## 更多信息

- 详细使用指南：查看 [README.md](./README.md)
- API 文档：查看 [docs/api/README.md](./docs/api/README.md)

---

**最后更新**：2025-12-20

