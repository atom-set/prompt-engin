# 使用示例

> **创建时间**: 2025-12-20（本地时间）  
> **适用对象**: 所有使用 Prompt Engine 的开发者

## 🎯 推荐说明

Prompt Engine 提供**两种使用方式**，**重点推荐方式2**：

- **⭐ 方式2**：精简版规则文件 + 技能系统（Token 优化，按需加载）✅ **重点推荐** - Token 占用减少约 60%，按需加载，灵活配置
- **方式1**：完整版规则文件（简单直接，复制即用）✅ **适用于小项目** - 简单直接，所有规则始终可用

> **重要**：两种方式都完全支持，**建议优先使用方式2**以获得更好的 Token 优化效果。

**选择建议**：
- **⭐ 所有项目（推荐）** → 使用方式2（精简版规则文件 + 技能系统）
- **小项目或不需要 token 优化** → 使用方式1（完整版规则文件）

## 📋 快速示例

### ⭐ 示例1：生成精简版规则文件（方式2）✅ **重点推荐**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成精简版规则文件（只包含核心规则）
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules

# 复制到你的项目
cp .cursorrules /path/to/your-project/

# 完成！Token 占用减少约 60%
```

**结果**：
- 文件大小：3427 行，约 124KB
- 只包含核心规则，Token 占用减少约 60%

---

### 示例2：生成完整版规则文件（方式1）✅ **适用于小项目**

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成完整版规则文件
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules

# 复制到你的项目
cp .cursorrules /path/to/your-project/

# 完成！直接使用即可
```

**结果**：
- 文件大小：8597 行，约 308KB
- 包含所有规则，始终可用

### 示例3：同时生成完整版和精简版

```bash
# 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 生成完整版
python3 scripts/prompt-engine merge --all --ide cursor --output .cursorrules.full

# 生成精简版
python3 scripts/prompt-engine merge --core-only --ide cursor --output .cursorrules.core

# 根据项目需求选择使用：
# - 小项目或不需要 token 优化：使用 .cursorrules.full
# - 大项目或需要 token 优化：使用 .cursorrules.core
```

## 📊 对比结果

| 指标 | 完整版 | 精简版 | 节省 |
|------|--------|--------|------|
| **行数** | 8597 行 | 3427 行 | **约 60%** |
| **文件大小** | ~308KB | ~124KB | **约 60%** |
| **Token 占用** | 大 | 小 | **约 60%** |
| **使用复杂度** | 简单（复制即用） | 简单（复制即用） | - |

## 🔍 验证生成结果

```bash
# 检查文件大小
wc -l .cursorrules
du -h .cursorrules

# 完整版应该约 8597 行
# 精简版应该约 3427 行
```

---

**最后更新**: 2025-12-20（本地时间）
