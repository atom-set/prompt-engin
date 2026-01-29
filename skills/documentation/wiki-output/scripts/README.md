# Scripts 目录

本目录包含 `wiki-output` skill 相关的工具脚本。

## 路径说明

**同步到目标项目后**（使用 `sync.sh` 脚本）：
- `.claude/skills/documentation/wiki-output/scripts/`

**推荐使用方式**（定义变量，避免重复输入长路径）：

```bash
# 在项目根目录定义变量（一次性设置）
MERMAID_SCRIPT=".claude/skills/documentation/wiki-output/scripts/mermaid_to_png.sh"
MERMAID_BATCH=".claude/skills/documentation/wiki-output/scripts/extract_and_convert_mermaid.py"

# 然后使用变量（简洁）
bash "$MERMAID_SCRIPT" input.mmd assets/
python3 "$MERMAID_BATCH" docs/架构图.md assets/
```

## 脚本列表

### mermaid_to_png.sh

将 Mermaid 流程图代码转换为 PNG 图片文件（自动使用白色背景）。

**依赖要求**：
- Node.js
- npm
- @mermaid-js/mermaid-cli (mmdc)

**安装依赖**：
```bash
npm install -g @mermaid-js/mermaid-cli
```

**使用方法**（使用上面定义的变量）：

```bash
# 从文件转换
bash "$MERMAID_SCRIPT" input.mmd assets/

# 从标准输入转换
echo "graph TD; A-->B" | bash "$MERMAID_SCRIPT" assets/
```

### extract_and_convert_mermaid.py

自动提取 Markdown 文档中的所有 Mermaid 图表，根据章节标题自动命名并批量转换为 PNG 图片。

**使用方法**（使用上面定义的变量）：

```bash
# 批量转换
python3 "$MERMAID_BATCH" docs/架构图.md assets/
```

**功能特性**：
1. 自动识别并提取文档中所有 Mermaid 代码块
2. 根据图表前的章节标题（H3、H4）自动生成有意义的文件名
3. 调用 `mermaid_to_png.sh` 批量转换为 PNG 图片（白色背景）
4. 生成 `image_list.txt` 文件，记录所有图片文件名和对应标题

## 说明

根据 **Agent Skills 开放标准**（官方规范），每个 skill 目录可以包含可选的 `scripts/` 目录，用于存放该 skill 相关的工具脚本。

这些脚本是 `wiki-output` skill 的组成部分，用于支持 WIKI 文档生成过程中的 Mermaid 图表转换功能。

**提示**：
- 当使用 `sync.sh` 脚本同步到目标项目时，这些脚本会被复制到 `.claude/skills/documentation/wiki-output/scripts/` 目录
- **强烈建议**：在项目根目录定义变量，避免重复输入长路径
