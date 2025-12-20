# 批量安装技能指南

> **创建时间**: 2025-12-20（本地时间）  
> **适用场景**: 需要一次性安装所有技能，然后选择使用哪些

## 📋 概述

批量安装脚本可以安装 prompt-engin 项目中的技能到你的项目，支持两种方式：
1. **全选安装**：一次性安装所有技能
2. **选择性安装**：交互式选择要安装的技能

安装后，你可以通过 `openskills sync -y` 选择要使用的技能。

**优势**：
- ✅ 支持全选或选择性安装，灵活配置
- ✅ 交互式选择，用户友好
- ✅ 安装后可以选择使用哪些技能
- ✅ 简单快捷，适合首次使用

---

## 🚀 使用方法

### 方法1：从 prompt-engin 项目运行

```bash
# 1. 进入 prompt-engin 项目目录
cd /path/to/prompt-engin

# 2. 运行批量安装脚本，指定目标项目目录
bash scripts/utils/install_all_skills.sh /path/to/your-project
```

### 方法2：从目标项目运行

```bash
# 1. 进入你的项目目录
cd /path/to/your-project

# 2. 运行批量安装脚本（使用相对路径）
bash ../prompt-engin/scripts/utils/install_all_skills.sh
```

### 方法3：使用绝对路径

```bash
# 在任何目录运行
bash /path/to/prompt-engin/scripts/utils/install_all_skills.sh /path/to/your-project
```

---

## 📝 使用示例

### 示例1：全选安装所有技能

```bash
# 1. 进入 prompt-engin 项目
cd /Users/gengxiao/workspace/D-codeup/prompt-engin

# 2. 运行批量安装脚本
bash scripts/utils/install_all_skills.sh /Users/gengxiao/workspace/D-codeup/my-project

# 输出示例：
# ========================================
# 批量安装 prompt-engin 技能
# ========================================
# 
# 技能源目录: /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills
# 目标项目目录: /Users/gengxiao/workspace/D-codeup/my-project
# 
# 找到 16 个技能
# 
# 可用技能列表:
#  1. architecture-diagram-template
#  2. code-organization
#  3. compatibility-check
#  ...
# 
# 请选择安装方式:
#  1. 安装所有技能（全选）
#  2. 选择要安装的技能（交互式选择）
#  3. 取消安装
# 
# 请输入选项 [1-3]: 1
# 
# 已选择：安装所有 16 个技能
# 
# 将要安装的技能:
#  1. architecture-diagram-template
#  2. code-organization
#  ...
# 
# 确认安装到项目: /Users/gengxiao/workspace/D-codeup/my-project? [y/N]: y
# 
# 正在安装: architecture-diagram-template
# ✓ architecture-diagram-template (安装成功)
# 
# 正在安装: code-organization
# ✓ code-organization (安装成功)
# ...
# 
# ========================================
# 安装完成
# ========================================
# 
# 成功安装: 16 个技能
```

### 示例2：选择性安装技能

```bash
# 1. 进入 prompt-engin 项目
cd /Users/gengxiao/workspace/D-codeup/prompt-engin

# 2. 运行批量安装脚本
bash scripts/utils/install_all_skills.sh /Users/gengxiao/workspace/D-codeup/my-project

# 输出示例：
# ========================================
# 批量安装 prompt-engin 技能
# ========================================
# 
# 可用技能列表:
#  1. architecture-diagram-template
#  2. code-organization
#  3. compatibility-check
#  4. design-principles
#  5. document-format
#  ...
# 
# 请选择安装方式:
#  1. 安装所有技能（全选）
#  2. 选择要安装的技能（交互式选择）
#  3. 取消安装
# 
# 请输入选项 [1-3]: 2
# 
# 请选择要安装的技能（输入技能编号，多个用逗号分隔，如: 1,3,5）:
# 提示: 输入 'all' 选择全部，输入 'skip' 跳过某个技能
# 
# 请输入技能编号: 1,3,5,7
# 
# 已选择：安装 4 个技能
# 
# 将要安装的技能:
#  1. architecture-diagram-template
#  2. compatibility-check
#  3. design-principles
#  4. document-format
# 
# 确认安装到项目: /Users/gengxiao/workspace/D-codeup/my-project? [y/N]: y
# 
# 正在安装: architecture-diagram-template
# ✓ architecture-diagram-template (安装成功)
# ...
# 
# ========================================
# 安装完成
# ========================================
# 
# 成功安装: 4 个技能
```

### 示例3：选择要使用的技能

安装完成后，使用 `openskills sync -y` 选择要使用的技能：

```bash
# 进入目标项目目录
cd /path/to/your-project

# 同步技能到 AGENTS.md（交互式选择）
openskills sync -y

# 或者：查看已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format
```

---

## 🎯 安装方式说明

### 方式1：全选安装（选项 1）

**适用场景**：
- 首次使用，想安装所有技能
- 不确定需要哪些技能，先全部安装

**操作**：
1. 选择选项 `1`（安装所有技能）
2. 确认安装
3. 等待安装完成

### 方式2：选择性安装（选项 2）

**适用场景**：
- 明确知道需要哪些技能
- 只想安装部分技能，节省时间

**操作**：
1. 选择选项 `2`（选择要安装的技能）
2. 输入技能编号（多个用逗号分隔，如：`1,3,5`）
   - 输入 `all` 选择全部
   - 可以跳过某些技能（不输入其编号）
3. 确认安装
4. 等待安装完成

**输入格式示例**：
- `1` - 只安装第 1 个技能
- `1,3,5` - 安装第 1、3、5 个技能（用逗号分隔）
- `1,2,3,4,5` - 安装第 1-5 个技能（不支持 `1-5` 范围语法，需要逐个输入）
- `all` 或 `ALL` - 选择全部技能（等同于选项 1）
- 输入无效编号会被自动跳过，并显示警告

**注意事项**：
- 技能编号从 1 开始
- 多个编号用逗号分隔，不要有空格（如：`1,3,5`，不是 `1, 3, 5`）
- 输入 `all` 等同于选择选项 1（安装所有技能）
- 如果未选择任何有效技能，脚本会退出

---

## 🔍 脚本功能说明

### 脚本位置

**路径**: `scripts/utils/install_all_skills.sh`

### 功能特性

1. **自动检测技能目录**：自动查找 `.claude/skills/` 目录中的所有技能
2. **批量安装**：一次性安装所有技能
3. **安装统计**：显示安装成功、失败、跳过的技能数量
4. **错误处理**：自动跳过无效的技能目录
5. **下一步提示**：安装完成后提示下一步操作

### 脚本参数

```bash
bash scripts/utils/install_all_skills.sh [目标项目目录]
```

**参数说明**：
- `目标项目目录`（可选）：要安装技能的目标项目目录路径
  - 如果未提供，使用当前工作目录
  - 如果提供，使用指定的目录

---

## ⚠️ 注意事项

### 1. 路径要求

- **技能源路径**：脚本会自动使用 prompt-engin 项目的 `.claude/skills/` 目录
- **目标项目路径**：可以是绝对路径或相对路径
- **openskills install**：需要绝对路径，且**必须指向单个技能目录**，不能指向整个技能目录
- **重要**：`openskills install /path/to/.claude/skills` ❌ 错误（不能安装整个目录）
- **正确**：`openskills install /path/to/.claude/skills/document-format` ✅ 正确（安装单个技能）

### 2. 前置条件

- ✅ 已安装 OpenSkills：`npm install -g openskills`
- ✅ 目标项目目录存在
- ✅ prompt-engin 项目的技能目录存在

### 3. 安装后的操作

安装完成后，**必须**运行 `openskills sync -y` 来选择要使用的技能：

```bash
cd /path/to/your-project
openskills sync -y
```

**重要**：`openskills sync -y` 不会安装新技能，只会同步已安装的技能到 `AGENTS.md`。

---

## 🔧 故障排查

### 问题1：脚本找不到技能目录

**错误信息**：
```
错误: 技能目录不存在: /path/to/.claude/skills
```

**解决方法**：
- 确保在 prompt-engin 项目根目录下运行脚本
- 检查 `.claude/skills/` 目录是否存在

### 问题2：openskills 命令未找到

**错误信息**：
```
错误: 未找到 openskills 命令，请先安装 OpenSkills
```

**解决方法**：
```bash
npm install -g openskills
```

### 问题3：技能安装失败

**可能原因**：
- 技能目录结构不正确
- `SKILL.md` 文件不存在
- 路径问题
- **尝试安装整个技能目录**（这是错误的）

**解决方法**：
- **重要**：`openskills install` 只能安装单个技能目录，不能安装整个 `.claude/skills/` 目录
- 检查技能目录结构：`ls -la .claude/skills/<skill-name>/`
- 确保 `SKILL.md` 文件存在
- 使用绝对路径安装单个技能进行测试：
  ```bash
  # 测试安装单个技能
  openskills install /path/to/prompt-engin/.claude/skills/document-format
  ```
- 如果单个技能安装成功，但批量安装失败，检查脚本是否正确处理路径

---

## 📚 相关文档

- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [技能使用指南](./skills-usage-guide.md) - 完整的使用指南
- [技能创建指南](./SKILLS_CREATION.md) - 如何创建新技能
- [快速开始指南](./QUICK_START_SKILLS.md) - 快速上手

---

**最后更新**: 2025-12-20（本地时间）
