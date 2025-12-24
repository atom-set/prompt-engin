# 环境安装和测试指南

> **创建时间**：2025-12-24（本地时间）  
> **最后更新**：2025-12-24（本地时间）

---

## 概述

本指南提供 Prompt Engine 项目的环境安装和测试步骤，帮助开发者快速配置开发环境并验证环境是否正确。

---

## 一、系统要求

### 基本要求

- **Python**：3.8 或更高版本
- **操作系统**：macOS、Linux、Windows
- **Shell**：Bash（macOS/Linux）或 Git Bash（Windows）

### 推荐配置

- **Python**：3.9 或更高版本
- **内存**：至少 512MB 可用内存
- **磁盘空间**：至少 100MB 可用空间

---

## 二、安装步骤

### 步骤1：克隆仓库

```bash
git clone https://github.com/your-username/prompt-engin.git
cd prompt-engin
```

### 步骤2：检查 Python 版本

```bash
python3 --version
```

**要求**：Python 版本必须是 3.8 或更高版本。

如果版本不符合要求，请访问 [Python 官网](https://www.python.org/downloads/) 下载并安装最新版本。

### 步骤3：安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装开发依赖（可选）
pip install -r requirements-dev.txt
```

### 步骤4：安装到系统（可选）

如果需要全局使用 `prompt-engine` 命令，可以安装到系统：

```bash
pip install -e .
```

安装后，可以在任何目录使用 `prompt-engine` 命令。

---

## 三、环境测试

### 方法1：使用 Shell 脚本（推荐）

运行环境测试脚本，自动检查环境配置：

```bash
bash scripts/utils/test_environment.sh
```

**测试内容**：
- ✅ Python 版本检查（需要 3.8+）
- ✅ 依赖包检查（检查 requirements.txt 中的包）
- ✅ CLI 工具可用性检查（测试 prompt-engine 命令）
- ✅ 基本功能测试（list、validate 等命令）
- ✅ 项目文件检查（prompts、scripts、dist 目录）
- ✅ 脚本权限检查

**测试结果**：
- ✅ **通过**：所有必需测试通过，环境配置正确
- ⚠️ **警告**：所有必需测试通过，但有可选功能未配置（不影响基本使用）
- ❌ **失败**：有必需测试失败，需要修复环境配置

### 方法2：使用 Python 脚本（可选）

如果提供了 Python 版本的环境测试脚本：

```bash
python3 scripts/utils/test_environment.py
```

### 方法3：手动测试

如果自动测试脚本不可用，可以手动测试：

#### 3.1 测试 Python 版本

```bash
python3 --version
# 应该显示 Python 3.8.x 或更高版本
```

#### 3.2 测试依赖包

```bash
python3 -c "import yaml; import click; print('依赖包检查通过')"
```

#### 3.3 测试 CLI 工具

```bash
# 测试 prompt-engine 命令
python3 scripts/prompt-engine --help

# 测试 list 命令
python3 scripts/prompt-engine list

# 测试 validate 命令
python3 scripts/prompt-engine validate prompts/
```

---

## 四、常见问题

### Q1：Python 版本不符合要求

**问题**：`Python 版本 >= 3.8` 测试失败

**解决方案**：
1. 访问 [Python 官网](https://www.python.org/downloads/) 下载最新版本
2. 安装后，使用 `python3 --version` 验证版本
3. 如果系统有多个 Python 版本，确保使用正确的版本

### Q2：依赖包安装失败

**问题**：`依赖包检查` 测试失败

**解决方案**：
1. 检查网络连接
2. 尝试使用国内镜像源：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```
3. 如果使用虚拟环境，确保已激活虚拟环境

### Q3：CLI 工具不可用

**问题**：`prompt-engine CLI 工具可用` 测试失败

**解决方案**：
1. 确保已安装依赖：`pip install -r requirements.txt`
2. 确保脚本有执行权限：`chmod +x scripts/prompt-engine`
3. 尝试使用完整路径：`python3 /path/to/prompt-engin/scripts/prompt-engine --help`

### Q4：产物文件不存在

**问题**：`产物文件存在` 测试显示警告

**解决方案**：
1. 这是可选功能，不影响基本使用
2. 如果需要使用产物，运行：
   ```bash
   bash scripts/utils/generate_dist.sh --all
   ```

### Q5：openskills 工具不可用

**问题**：`openskills 工具可用` 测试显示警告

**解决方案**：
1. 这是可选功能，不影响基本使用
2. 如果需要使用技能系统，安装 openskills：
   ```bash
   npm install -g @openskills/cli
   ```

---

## 五、验证安装

安装完成后，运行以下命令验证安装：

```bash
# 1. 运行环境测试
bash scripts/utils/test_environment.sh

# 2. 测试 CLI 工具
python3 scripts/prompt-engine list

# 3. 测试验证功能
python3 scripts/prompt-engine validate prompts/
```

如果所有测试通过，说明环境配置正确，可以开始使用 Prompt Engine。

---

## 六、下一步

环境配置完成后，可以：

1. **查看使用手册**：阅读 [使用手册](./USAGE_MANUAL.md) 了解如何使用 Prompt Engine
2. **查看快速参考**：阅读 [快速参考](./QUICK_REFERENCE.md) 快速查找常用命令
3. **开始使用**：根据项目需求选择合适的使用方式（单文件完整版、单文件精简版+技能、多文件目录）

---

## 相关文档

- [使用手册](./USAGE_MANUAL.md) - 详细的使用指南
- [快速参考](./QUICK_REFERENCE.md) - 常用命令速查
- [README.md](../../README.md) - 项目主文档

---

**最后更新**：2025-12-24（本地时间）

