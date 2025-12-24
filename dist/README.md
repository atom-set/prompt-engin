# 产物目录说明

> **文件说明**：产物目录说明文档
> **创建时间**：2025-12-24（本地时间）

---

## 📋 目录说明

`dist/` 目录包含为三个平台（Cursor、TRAE、Antigravity）生成的规则文件产物，支持三种组织方式。

## 📁 目录结构

```
dist/
├── skills/                       # 技能产物目录（方式2使用）
│   ├── README.md                 # 技能目录说明
│   ├── document-format/          # 文档格式技能
│   │   └── SKILL.md
│   ├── time-format/              # 时间格式技能
│   │   └── SKILL.md
│   └── ...                       # 其他技能（共16个）
├── cursor/                       # Cursor IDE 产物
│   ├── single-full/              # 方式1：单文件完整版
│   │   └── .cursorrules.all      # 完整版规则文件（8597 行）
│   ├── single-core/              # 方式2：单文件精简版
│   │   └── .cursorrules.core     # 精简版规则文件（3427 行）
│   └── multi-files/              # 方式3：多文件目录
│       └── rules/                # 多文件规则目录
│           ├── 001-common.mdc
│           ├── 002-code.mdc
│           └── ...
├── trae/                         # TRAE IDE 产物
│   ├── single-full/
│   │   └── .traerules.all        # 完整版规则文件
│   ├── single-core/
│   │   └── .traerules.core       # 精简版规则文件
│   └── multi-files/
│       └── .trae/                # 多文件目录（YAML 格式）
│           ├── ai-rules.yml
│           └── team-rules.yml
└── antigravity/                  # Antigravity IDE 产物
    ├── single-full/
    │   └── .antigravityrules.all  # 完整版规则文件
    ├── single-core/
    │   └── .antigravityrules.core # 精简版规则文件
    └── multi-files/
        └── *.agent               # Agent 配置文件（如果支持）
```

## 🚀 快速使用

### 方式1：单文件完整版（最简单）

**Cursor**：
```bash
cp dist/cursor/single-full/.cursorrules.all /path/to/your-project/.cursorrules
```

**TRAE**：
```bash
cp dist/trae/single-full/.traerules.all /path/to/your-project/.traerules
```

**Antigravity**：
```bash
cp dist/antigravity/single-full/.antigravityrules.all /path/to/your-project/.antigravityrules
```

### 方式2：单文件精简版 + 技能（推荐）⭐

**Cursor**：
```bash
# 1. 复制规则文件
cp dist/cursor/single-core/.cursorrules.core /path/to/your-project/.cursorrules

# 2. 复制技能（从 dist 目录，推荐）
cp -r dist/skills /path/to/your-project/.claude/

# 或使用安装脚本（从源代码目录）
cd /path/to/prompt-engin
bash scripts/utils/install_all_skills.sh /path/to/your-project

# 3. 同步技能
cd /path/to/your-project
openskills sync -y
```

### 方式3：多文件目录（精细控制）

**Cursor**：
```bash
# 使用同步脚本（推荐）
bash scripts/utils/sync_to_project.sh \
  --platform cursor \
  --mode multi-files \
  /path/to/your-project

# 或手动复制
cp -r dist/cursor/multi-files/rules /path/to/your-project/.cursor/
```

**TRAE**：
```bash
# 使用同步脚本（推荐）
bash scripts/utils/sync_to_project.sh \
  --platform trae \
  --mode multi-files \
  /path/to/your-project

# 或手动复制
cp -r dist/trae/multi-files/.trae /path/to/your-project/
```

## 📖 详细说明

- **方式选择**：查看 [使用手册](../docs/guides/USAGE_MANUAL.md)
- **平台支持**：查看 [多平台多方式规则使用指南](../docs/milestones/V2_multi-platform-rules/multi-platform-rules-guide.md)
- **完整文档**：查看 [V2 版本改进计划](../docs/milestones/V2_multi-platform-rules/V2_IMPROVEMENT_PLAN.md)

## ⚠️ 注意事项

1. **产物文件已提交到 Git**：可以直接使用，无需安装环境
2. **版本同步**：产物文件与代码版本同步，确保一致性
3. **更新方式**：运行 `bash scripts/utils/generate_dist.sh --all` 更新产物

---

**最后更新**：2025-12-24（本地时间）

