#!/usr/bin/env python3
"""
将 .core 文件转换为顶层 skills

用法:
    python scripts/core-to-skills.py [--output-dir skills/core]
"""

import re
import os
import sys
from datetime import datetime


# 模块到 skill 的映射配置
MODULE_TO_SKILL_CONFIG = {
    'tool-permission-system.md': {
        'name': 'tool-permission-system',
        'description': '工具权限系统，定义工具分类体系和统一检查流程',
        'tags': ['core', 'mode', 'permission', 'security'],
        'title': '工具权限系统',
        'scenarios': [
            '调用任何工具前',
            '需要判断工具权限时',
            '需要执行安全检查时'
        ],
        'triggers': [
            '每次工具调用前自动应用',
            '所有模式（Plan、Act）下都应用'
        ]
    },
    'mode-common.md': {
        'name': 'mode-common',
        'description': '模式通用规则，包括模式切换、响应格式等',
        'tags': ['core', 'mode', 'common'],
        'title': '模式通用规则',
        'scenarios': [
            '模式切换时',
            '生成响应时',
            '需要格式化输出时'
        ],
        'triggers': [
            '每次响应生成时自动应用',
            '模式切换时自动应用'
        ]
    },
    'security-permissions.md': {
        'name': 'security-permissions',
        'description': '安全规则和权限规则，系统化整理权限矩阵',
        'tags': ['core', 'mode', 'security', 'permission'],
        'title': '安全规则和权限规则',
        'scenarios': [
            '需要查看权限矩阵时',
            '需要确认操作权限时',
            '需要安全检查时'
        ],
        'triggers': [
            '工具调用前自动应用',
            '模式切换时自动应用'
        ]
    },
    'code-format.md': {
        'name': 'code-format',
        'description': '代码格式规范，包括缩进、行长度、空行等',
        'tags': ['core', 'code', 'format'],
        'title': '代码格式规范',
        'scenarios': [
            '编写代码时',
            '格式化代码时',
            '代码审查时'
        ],
        'triggers': [
            '编写代码时自动应用',
            '格式化代码时自动应用'
        ]
    },
    'naming.md': {
        'name': 'naming',
        'description': '命名规范，包括变量、函数、类、常量等命名规则',
        'tags': ['core', 'code', 'naming'],
        'title': '命名规范',
        'scenarios': [
            '命名变量、函数、类时',
            '创建新文件时',
            '代码审查时'
        ],
        'triggers': [
            '命名时自动应用',
            '创建文件时自动应用'
        ]
    },
    'function-design.md': {
        'name': 'function-design',
        'description': '函数设计规范，包括函数命名、参数处理、代码嵌套等',
        'tags': ['core', 'code', 'function', 'design'],
        'title': '函数设计规范',
        'scenarios': [
            '设计函数时',
            '重构函数时',
            '代码审查时'
        ],
        'triggers': [
            '设计函数时自动应用',
            '重构函数时自动应用'
        ]
    },
    'comments.md': {
        'name': 'comments',
        'description': '注释规范，包括单行注释、多行注释、文档注释等',
        'tags': ['core', 'code', 'comments'],
        'title': '注释规范',
        'scenarios': [
            '编写注释时',
            '文档化代码时',
            '代码审查时'
        ],
        'triggers': [
            '编写注释时自动应用',
            '文档化代码时自动应用'
        ]
    },
    'strategy.md': {
        'name': 'error-handling-strategy',
        'description': '错误处理策略，包括异常捕获、错误处理模式等',
        'tags': ['core', 'code', 'error-handling', 'strategy'],
        'title': '错误处理策略',
        'scenarios': [
            '处理错误时',
            '设计错误处理机制时',
            '代码审查时'
        ],
        'triggers': [
            '处理错误时自动应用',
            '设计错误处理机制时自动应用'
        ]
    },
    'logging.md': {
        'name': 'error-logging',
        'description': '错误日志记录，包括日志级别、日志内容、结构化日志等',
        'tags': ['core', 'code', 'error-handling', 'logging'],
        'title': '错误日志记录',
        'scenarios': [
            '记录日志时',
            '设计日志系统时',
            '调试问题时'
        ],
        'triggers': [
            '记录日志时自动应用',
            '设计日志系统时自动应用'
        ]
    },
    'message-format.md': {
        'name': 'error-message-format',
        'description': '错误信息格式，包括用户可见错误、错误码规范等',
        'tags': ['core', 'code', 'error-handling', 'message'],
        'title': '错误信息格式',
        'scenarios': [
            '设计错误信息时',
            '返回错误给用户时',
            '定义错误码时'
        ],
        'triggers': [
            '设计错误信息时自动应用',
            '返回错误时自动应用'
        ]
    },
    'return-values.md': {
        'name': 'return-values',
        'description': '返回值规范，包括返回值模式、错误处理等',
        'tags': ['core', 'code', 'error-handling', 'return'],
        'title': '返回值规范',
        'scenarios': [
            '设计函数返回值时',
            '处理函数返回值时',
            '代码审查时'
        ],
        'triggers': [
            '设计函数返回值时自动应用',
            '处理返回值时自动应用'
        ]
    },
    'plan/behavior.md': {
        'name': 'plan-mode',
        'description': 'Plan 模式行为规范，定义 Plan 模式下的允许和禁止操作',
        'tags': ['core', 'mode', 'plan'],
        'title': 'Plan 模式行为规范',
        'scenarios': [
            'Plan 模式下操作时',
            '需要分析需求时',
            '需要输出方案时'
        ],
        'triggers': [
            'Plan 模式下自动应用',
            '分析需求时自动应用'
        ]
    },
    'act/behavior.md': {
        'name': 'act-mode',
        'description': 'Act 模式行为规范，定义 Act 模式下的执行规范',
        'tags': ['core', 'mode', 'act'],
        'title': 'Act 模式行为规范',
        'scenarios': [
            'Act 模式下执行时',
            '执行代码修改时',
            '需要确认计划时'
        ],
        'triggers': [
            'Act 模式下自动应用',
            '执行修改时自动应用'
        ]
    },
    'plan/solution-output.md': {
        'name': 'solution-output',
        'description': '代码修改前的方案输出机制，定义方案输出的内容和格式',
        'tags': ['core', 'mode', 'plan', 'solution'],
        'title': '代码修改前的方案输出机制',
        'scenarios': [
            '需要输出修改方案时',
            '代码修改前',
            '需要用户确认时'
        ],
        'triggers': [
            '代码修改前自动应用',
            '输出方案时自动应用'
        ]
    },
    'act/file-write.md': {
        'name': 'file-write',
        'description': '文件写入规则，包括文件大小检查和写入策略',
        'tags': ['core', 'mode', 'act', 'file'],
        'title': '文件写入规则',
        'scenarios': [
            '写入文件时',
            '创建新文件时',
            '修改文件时'
        ],
        'triggers': [
            '写入文件前自动应用',
            '创建文件时自动应用'
        ]
    }
}


def parse_core_file(core_file_path):
    """解析 .core 文件，提取各个模块"""
    with open(core_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式分割模块
    pattern = r'# ===========================================================================\n# 来源: ([^\n]+)\n# ===========================================================================\n\n(.*?)(?=\n# ===========================================================================|$)'
    
    modules = []
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        source_path = match.group(1)
        module_content = match.group(2).strip()
        
        # 提取模块标题（第一个 # 开头的行）
        title_match = re.search(r'^# ([^\n]+)', module_content, re.MULTILINE)
        title = title_match.group(1) if title_match else 'Untitled'
        
        # 提取文件名（用于匹配配置）
        filename = source_path.split('/')[-1]
        if 'plan/' in source_path:
            filename = f'plan/{filename}'
        elif 'act/' in source_path:
            filename = f'act/{filename}'
        elif 'error-handling/' in source_path:
            filename = source_path.split('error-handling/')[-1]
        
        modules.append({
            'source': source_path,
            'filename': filename,
            'title': title,
            'content': module_content
        })
    
    return modules


def get_skill_config(filename):
    """获取 skill 配置"""
    # 直接匹配
    if filename in MODULE_TO_SKILL_CONFIG:
        return MODULE_TO_SKILL_CONFIG[filename]
    
    # 尝试匹配文件名（不含路径）
    basename = os.path.basename(filename)
    if basename in MODULE_TO_SKILL_CONFIG:
        return MODULE_TO_SKILL_CONFIG[basename]
    
    # 默认配置
    name = basename.replace('.md', '').replace('/', '-')
    return {
        'name': name,
        'description': f'{name} 规范',
        'tags': ['core'],
        'title': name.replace('-', ' ').title(),
        'scenarios': ['相关场景'],
        'triggers': ['自动应用']
    }


def convert_to_skill(module, config):
    """将模块内容转换为 skill 格式"""
    # 提取正文内容（移除标题和文件说明）
    content = module['content']
    
    # 移除文件说明块（> **文件说明**...）
    content = re.sub(r'> \*\*文件说明\*\*.*?\n\n', '', content, flags=re.DOTALL)
    
    # 移除创建时间等元信息
    content = re.sub(r'> \*\*创建时间\*\*.*?\n', '', content)
    content = re.sub(r'> \*\*重构时间\*\*.*?\n', '', content)
    content = re.sub(r'> \*\*更新时间\*\*.*?\n', '', content)
    content = re.sub(r'> \*\*规则来源\*\*.*?\n', '', content)
    content = re.sub(r'> \*\*相关文件\*\*.*?\n', '', content)
    
    # 清理多余的空行
    content = re.sub(r'\n{3,}', '\n\n', content)
    content = content.strip()
    
    # 构建 skill 内容
    skill_content = f"""---
name: {config['name']}
description: {config['description']}
tags: {config['tags']}
---

# {config['title']}

## 使用场景

当用户需要：
"""
    
    for scenario in config['scenarios']:
        skill_content += f"- {scenario}\n"
    
    skill_content += "\n## 触发条件\n\n"
    skill_content += "以下情况自动应用此规范：\n"
    
    for trigger in config['triggers']:
        skill_content += f"- {trigger}\n"
    
    skill_content += "\n## 与其他规则的配合\n\n"
    skill_content += "- 与核心规则配合使用\n"
    
    # 添加与其他 skills 的配合说明
    if 'tool-permission-system' in config['name']:
        skill_content += "- 与 `mode-common` 配合：模式切换和响应格式\n"
        skill_content += "- 与 `security-permissions` 配合：权限检查\n"
    elif 'mode-common' in config['name']:
        skill_content += "- 与 `tool-permission-system` 配合：工具调用检查\n"
        skill_content += "- 与 `plan-mode` 和 `act-mode` 配合：模式行为规范\n"
    elif 'plan-mode' in config['name']:
        skill_content += "- 与 `mode-common` 配合：模式切换规则\n"
        skill_content += "- 与 `solution-output` 配合：方案输出机制\n"
    elif 'act-mode' in config['name']:
        skill_content += "- 与 `mode-common` 配合：模式切换规则\n"
        skill_content += "- 与 `file-write` 配合：文件写入规则\n"
    elif 'solution-output' in config['name']:
        skill_content += "- 与 `plan-mode` 配合：Plan 模式行为规范\n"
        skill_content += "- 与 `tool-permission-system` 配合：工具调用检查\n"
    elif 'file-write' in config['name']:
        skill_content += "- 与 `act-mode` 配合：Act 模式行为规范\n"
    elif 'error-handling' in config['name']:
        skill_content += "- 与其他错误处理 skills 配合：完整的错误处理体系\n"
    
    skill_content += "\n---\n\n"
    skill_content += content
    
    return skill_content


def convert_core_to_skills(core_file_path='.core', output_dir='skills/core'):
    """将 .core 文件转换为 skills"""
    print(f"📖 读取文件: {core_file_path}")
    
    if not os.path.exists(core_file_path):
        print(f"❌ 错误: 文件不存在: {core_file_path}")
        return False
    
    # 解析文件
    modules = parse_core_file(core_file_path)
    print(f"✅ 找到 {len(modules)} 个模块")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换并保存
    saved_files = []
    for i, module in enumerate(modules, 1):
        config = get_skill_config(module['filename'])
        skill_content = convert_to_skill(module, config)
        
        # 确定输出路径
        output_path = os.path.join(output_dir, f"{config['name']}.md")
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(skill_content)
        
        saved_files.append(output_path)
        print(f"  [{i}/{len(modules)}] ✅ {output_path} ({config['name']})")
    
    # 创建索引文件
    create_index_file(output_dir, modules)
    
    print(f"\n✅ 转换完成!")
    print(f"📁 输出目录: {output_dir}")
    print(f"📄 共生成 {len(saved_files)} 个 skills")
    
    return True


def create_index_file(output_dir, modules):
    """创建索引文件"""
    index_path = os.path.join(output_dir, 'README.md')
    
    # 按类别分组
    mode_skills = []
    code_skills = []
    
    for module in modules:
        config = get_skill_config(module['filename'])
        if 'mode' in config['tags']:
            mode_skills.append(config)
        elif 'code' in config['tags']:
            code_skills.append(config)
    
    # 生成索引内容
    content = f"""# 核心规则 Skills

> **说明**：本目录包含所有核心规则 skills，这些规则在每次对话中都会自动应用
> **自动生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📚 Skills 列表

### 模式相关 Skills（必须应用）

"""
    
    for i, config in enumerate(mode_skills, 1):
        content += f"{i}. **{config['title']}** - `{config['name']}.md`\n"
        content += f"   - 描述：{config['description']}\n"
        content += f"   - 标签：{', '.join(config['tags'])}\n\n"
    
    content += "### 代码规范 Skills（自动应用）\n\n"
    
    for i, config in enumerate(code_skills, 1):
        content += f"{i}. **{config['title']}** - `{config['name']}.md`\n"
        content += f"   - 描述：{config['description']}\n"
        content += f"   - 标签：{', '.join(config['tags'])}\n\n"
    
    content += """## 🔄 使用方式

### 方式一：通过 openskills 命令

```bash
# 读取单个 skill
openskills read core/tool-permission-system

# 读取所有核心 skills
openskills read core
```

### 方式二：在 Cursor 配置中引用

在 `.cursorrules` 或项目配置中：

```markdown
# 核心规则（必须应用）

@skills/core/tool-permission-system.md
@skills/core/mode-common.md
@skills/core/security-permissions.md
```

## 📝 维护说明

这些 skills 是从 `.core` 文件自动转换生成的。如果需要修改：

1. 直接编辑对应的 skill 文件
2. 或者修改 `.core` 文件后重新运行转换脚本

## 🔗 相关文档

- [skills/README.md](../skills/README.md) - Skills 主文档
- [README.md](../README.md) - 项目主文档
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  📄 创建索引文件: {index_path}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='将 .core 文件转换为顶层 skills')
    parser.add_argument('--core-file', default='.core', help='.core 文件路径')
    parser.add_argument('--output-dir', default='skills/core', help='输出目录')
    
    args = parser.parse_args()
    
    success = convert_core_to_skills(args.core_file, args.output_dir)
    sys.exit(0 if success else 1)
