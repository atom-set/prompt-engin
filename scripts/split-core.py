#!/usr/bin/env python3
"""
拆分 .core 文件为独立模块文件

用法:
    python scripts/split-core.py [--output-dir prompts/core]
"""

import re
import os
import sys


def parse_core_file(core_file_path):
    """解析 .core 文件，提取各个模块"""
    with open(core_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式分割模块
    # 匹配格式: # ===========================================================================\n# 来源: path/to/file.md\n# ===========================================================================
    pattern = r'# ===========================================================================\n# 来源: ([^\n]+)\n# ===========================================================================\n\n(.*?)(?=\n# ===========================================================================|$)'
    
    modules = []
    matches = re.finditer(pattern, content, re.DOTALL)
    
    for match in matches:
        source_path = match.group(1)
        module_content = match.group(2).strip()
        
        # 提取模块标题（第一个 # 开头的行）
        title_match = re.search(r'^# ([^\n]+)', module_content, re.MULTILINE)
        title = title_match.group(1) if title_match else 'Untitled'
        
        modules.append({
            'source': source_path,
            'title': title,
            'content': module_content
        })
    
    return modules


def determine_output_path(source_path, output_dir):
    """根据源路径确定输出路径"""
    # 提取相对路径部分
    # 例如: prompts/stages/common/mode/tool-permission-system.md
    # -> mode/tool-permission-system.md
    
    # 移除 prompts/stages/common/ 前缀
    if 'prompts/stages/common/' in source_path:
        relative_path = source_path.replace('prompts/stages/common/', '')
    elif 'prompts/' in source_path:
        relative_path = source_path.replace('prompts/', '')
    else:
        relative_path = source_path
    
    # 处理子目录
    if '/' in relative_path:
        # 例如: mode/tool-permission-system.md -> mode/tool-permission-system.md
        # 例如: code/error-handling/strategy.md -> code/error-handling/strategy.md
        output_path = os.path.join(output_dir, relative_path)
    else:
        # 直接放在输出目录
        output_path = os.path.join(output_dir, relative_path)
    
    return output_path


def split_core_file(core_file_path='.core', output_dir='prompts/core'):
    """拆分 .core 文件"""
    print(f"📖 读取文件: {core_file_path}")
    
    if not os.path.exists(core_file_path):
        print(f"❌ 错误: 文件不存在: {core_file_path}")
        return False
    
    # 解析文件
    modules = parse_core_file(core_file_path)
    print(f"✅ 找到 {len(modules)} 个模块")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 拆分并保存
    saved_files = []
    for i, module in enumerate(modules, 1):
        output_path = determine_output_path(module['source'], output_dir)
        
        # 创建目录
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(module['content'])
        
        saved_files.append(output_path)
        print(f"  [{i}/{len(modules)}] ✅ {output_path}")
    
    # 创建索引文件
    create_index_file(output_dir, modules)
    
    print(f"\n✅ 拆分完成!")
    print(f"📁 输出目录: {output_dir}")
    print(f"📄 共生成 {len(saved_files)} 个文件")
    
    return True


def create_index_file(output_dir, modules):
    """创建索引文件"""
    index_path = os.path.join(output_dir, 'README.md')
    
    # 按类别分组
    mode_modules = []
    code_modules = []
    other_modules = []
    
    for module in modules:
        source = module['source']
        if 'mode' in source:
            mode_modules.append(module)
        elif 'code' in source:
            code_modules.append(module)
        else:
            other_modules.append(module)
    
    # 生成索引内容
    content = f"""# 核心规则索引

> **说明**：本目录包含所有核心规则，这些规则在每次对话中都会自动应用
> **自动生成时间**：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📚 规则列表

### 模式相关规则（必须应用）

"""
    
    for i, module in enumerate(mode_modules, 1):
        relative_path = module['source'].replace('prompts/stages/common/', '')
        content += f"{i}. **{module['title']}** - `{relative_path}`\n"
    
    content += "\n### 代码规范（自动应用）\n\n"
    
    for i, module in enumerate(code_modules, 1):
        relative_path = module['source'].replace('prompts/stages/common/', '')
        content += f"- **{module['title']}** - `{relative_path}`\n"
    
    if other_modules:
        content += "\n### 其他规则\n\n"
        for module in other_modules:
            relative_path = module['source'].replace('prompts/stages/common/', '')
            content += f"- **{module['title']}** - `{relative_path}`\n"
    
    content += """
## 🔄 合并机制

使用 `scripts/merge-core.sh` 脚本自动合并所有规则到 `.core` 文件。

## 📝 使用说明

在 Cursor IDE 中，`.core` 文件会自动被应用。如果需要单独引用某个规则，可以直接引用对应的独立文件。
"""
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  📄 创建索引文件: {index_path}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='拆分 .core 文件为独立模块')
    parser.add_argument('--core-file', default='.core', help='.core 文件路径')
    parser.add_argument('--output-dir', default='prompts/core', help='输出目录')
    
    args = parser.parse_args()
    
    success = split_core_file(args.core_file, args.output_dir)
    sys.exit(0 if success else 1)
