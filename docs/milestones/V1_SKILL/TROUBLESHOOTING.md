# 技能系统故障排查指南

> **创建时间**: 2025-12-20（本地时间）  
> **适用场景**: 技能安装和使用过程中遇到的问题

## 📋 常见问题

### Q1：为什么不能直接安装整个技能目录？

**问题描述**：

```bash
# ❌ 错误：尝试安装整个技能目录
openskills install /path/to/prompt-engin/.claude/skills

# 错误信息：
# Error: Command failed: git clone --depth 1 --quiet "https://github.com//Users" ...
```

**原因**：

`openskills install` **只能安装单个技能目录**，不能安装整个 `.claude/skills/` 目录。

当提供整个技能目录路径时，`openskills` 工具会误认为这是一个 GitHub 仓库路径，尝试执行 `git clone`，导致失败。

**解决方法**：

**方式1：使用批量安装脚本（推荐）**

```bash
# 从 prompt-engin 项目运行
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 或从目标项目运行
cd /path/to/your-project
bash ../prompt-engin/scripts/utils/install_all_skills.sh
```

**方式2：安装单个技能**

```bash
# ✅ 正确：安装单个技能目录
openskills install /path/to/prompt-engin/.claude/skills/document-format
openskills install /path/to/prompt-engin/.claude/skills/time-format
# ... 逐个安装其他技能
```

**方式3：批量安装（使用循环）**

```bash
# 批量安装所有技能
for skill in document-format time-format code-organization; do
  openskills install /path/to/prompt-engin/.claude/skills/$skill
done
```

---

### Q2：批量安装脚本执行失败

**问题描述**：

运行批量安装脚本时，某些技能安装失败。

**可能原因**：

1. **openskills 未安装或未正确配置**
2. **技能目录结构不正确**
3. **路径问题（相对路径 vs 绝对路径）**
4. **权限问题**

**解决方法**：

**步骤1：检查 openskills 安装**

```bash
# 检查 openskills 是否已安装
which openskills

# 如果未安装，安装 OpenSkills
npm install -g openskills

# 验证安装
openskills --version
```

**步骤2：检查技能目录结构**

```bash
# 检查技能目录是否存在
ls -la /path/to/prompt-engin/.claude/skills/

# 检查单个技能目录结构
ls -la /path/to/prompt-engin/.claude/skills/document-format/

# 确保 SKILL.md 文件存在
test -f /path/to/prompt-engin/.claude/skills/document-format/SKILL.md && echo "✓ SKILL.md 存在" || echo "✗ SKILL.md 不存在"
```

**步骤3：测试单个技能安装**

```bash
# 测试安装单个技能
cd /path/to/your-project
openskills install /path/to/prompt-engin/.claude/skills/document-format

# 如果单个技能安装成功，说明 openskills 配置正确
# 如果失败，检查错误信息
```

**步骤4：检查批量安装脚本**

```bash
# 查看脚本帮助
bash /path/to/prompt-engin/scripts/utils/install_all_skills.sh --help

# 使用详细模式运行（查看详细错误信息）
bash /path/to/prompt-engin/scripts/utils/install_all_skills.sh /path/to/your-project
```

---

### Q3：openskills install 提示路径错误

**问题描述**：

```bash
openskills install /path/to/prompt-engin/.claude/skills/document-format
# 错误：路径不存在或无效
```

**解决方法**：

**步骤1：验证路径**

```bash
# 检查路径是否存在
ls -la /path/to/prompt-engin/.claude/skills/document-format

# 使用绝对路径（推荐）
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format
```

**步骤2：使用相对路径（如果在同一工作区）**

```bash
# 如果 prompt-engin 和你的项目在同一工作区
cd /path/to/your-project
openskills install ../prompt-engin/.claude/skills/document-format
```

**步骤3：检查路径格式**

```bash
# ✅ 正确：指向单个技能目录
openskills install /path/to/prompt-engin/.claude/skills/document-format

# ❌ 错误：指向整个技能目录
openskills install /path/to/prompt-engin/.claude/skills

# ❌ 错误：路径中包含空格（需要引号）
openskills install "/path/to/prompt-engin/.claude/skills/document-format"
```

---

### Q4：openskills sync -y 没有同步技能

**问题描述**：

运行 `openskills sync -y` 后，`AGENTS.md` 中没有技能列表。

**可能原因**：

1. **技能未正确安装**
2. **技能目录位置不正确**
3. **AGENTS.md 文件权限问题**

**解决方法**：

**步骤1：检查已安装的技能**

```bash
# 列出已安装的技能
openskills list

# 检查技能目录
ls -la .claude/skills/
```

**步骤2：验证技能安装**

```bash
# 检查技能目录是否存在
test -d .claude/skills/document-format && echo "✓ 技能目录存在" || echo "✗ 技能目录不存在"

# 检查 SKILL.md 文件
test -f .claude/skills/document-format/SKILL.md && echo "✓ SKILL.md 存在" || echo "✗ SKILL.md 不存在"
```

**步骤3：手动同步**

```bash
# 确保在项目根目录
cd /path/to/your-project

# 运行同步命令
openskills sync -y

# 检查 AGENTS.md 是否已创建/更新
cat AGENTS.md
```

---

### Q5：技能安装后无法使用

**问题描述**：

技能已安装，但 AI 无法识别或使用。

**可能原因**：

1. **AGENTS.md 未正确同步**
2. **技能格式不正确**
3. **AI 未读取 AGENTS.md**

**解决方法**：

**步骤1：检查 AGENTS.md**

```bash
# 查看 AGENTS.md 内容
cat AGENTS.md

# 确保技能列表在 <available_skills> 标签中
grep -A 20 "<available_skills>" AGENTS.md
```

**步骤2：验证技能格式**

```bash
# 检查技能文件格式
cat .claude/skills/document-format/SKILL.md | head -20

# 确保包含正确的元数据
# ---
# name: document-format
# description: ...
# tags: ...
# ---
```

**步骤3：重新同步**

```bash
# 重新同步技能到 AGENTS.md
openskills sync -y

# 验证同步结果
cat AGENTS.md
```

---

## 🔧 调试技巧

### 1. 启用详细输出

```bash
# 批量安装脚本会显示详细输出
bash scripts/utils/install_all_skills.sh /path/to/your-project

# openskills 命令的详细输出
openskills install /path/to/skill --verbose  # 如果支持
```

### 2. 检查日志

```bash
# 检查 openskills 临时目录
ls -la ~/.openskills-temp-*/

# 检查项目中的技能目录
ls -la .claude/skills/
ls -la .agent/skills/  # 如果使用 universal 模式
```

### 3. 验证安装

```bash
# 列出已安装的技能
openskills list

# 查看特定技能内容
openskills read document-format

# 检查技能目录结构
tree .claude/skills/  # 如果安装了 tree 命令
# 或
find .claude/skills/ -type f -name "*.md"
```

---

## 📚 相关文档

- [批量安装指南](./BATCH_INSTALL_GUIDE.md) - 批量安装所有技能的方法
- [技能系统快速参考](./SKILLS_QUICK_REFERENCE.md) - 技能目录位置和使用方法
- [技能使用指南](./skills-usage-guide.md) - 完整的使用指南
- [技能创建指南](./SKILLS_CREATION.md) - 如何创建新技能

---

## 💡 最佳实践

### 1. 使用批量安装脚本

**推荐**：使用批量安装脚本，而不是手动逐个安装。

```bash
# ✅ 推荐
bash scripts/utils/install_all_skills.sh /path/to/your-project

# ❌ 不推荐（容易出错）
openskills install /path/to/.claude/skills  # 错误：不能安装整个目录
```

### 2. 使用绝对路径

**推荐**：使用绝对路径，避免路径解析问题。

```bash
# ✅ 推荐：绝对路径
openskills install /Users/gengxiao/workspace/D-codeup/prompt-engin/.claude/skills/document-format

# ⚠️ 谨慎：相对路径（需要确保工作目录正确）
openskills install ../prompt-engin/.claude/skills/document-format
```

### 3. 验证安装结果

**推荐**：安装后验证技能是否正确安装。

```bash
# 安装后验证
openskills list
openskills read document-format
openskills sync -y
cat AGENTS.md
```

---

**最后更新**: 2025-12-20（本地时间）
