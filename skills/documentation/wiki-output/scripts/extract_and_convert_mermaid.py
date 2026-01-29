#!/usr/bin/env python3
"""
批量提取并转换 Mermaid 图表工具

自动提取 Markdown 文档中的所有 Mermaid 图表，根据章节标题自动命名并批量转换为 PNG 图片。

使用方法：
    python3 extract_and_convert_mermaid.py <markdown_file> [output_dir]

参数说明：
    - markdown_file: 包含 Mermaid 图表的 Markdown 文件路径
    - output_dir: 输出目录，默认为 ./assets/batch-logger

功能特性：
    1. 自动识别并提取文档中所有 Mermaid 代码块
    2. 根据图表前的章节标题（H3、H4）自动生成有意义的文件名
    3. 调用 mermaid_to_png.sh 批量转换为 PNG 图片（白色背景）
    4. 生成 image_list.txt 文件，记录所有图片文件名和对应标题
"""

import re
import sys
import os
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional


def extract_mermaid_blocks(content: str) -> List[Tuple[str, Optional[str], int]]:
    """
    提取 Markdown 文档中的所有 Mermaid 代码块
    
    Returns:
        [(mermaid_code, section_title, line_number), ...]
    """
    mermaid_blocks = []
    
    # 匹配 Mermaid 代码块
    pattern = r'```mermaid\s*\n(.*?)```'
    
    lines = content.split('\n')
    current_section = None
    section_number = None
    
    for i, line in enumerate(lines):
        # 检查是否是章节标题（H3 或 H4）
        h3_match = re.match(r'^###\s+(.+)$', line)
        h4_match = re.match(r'^####\s+(.+)$', line)
        
        if h3_match:
            # H3 标题：提取编号和标题
            title = h3_match.group(1).strip()
            # 尝试提取编号（如 "1.1.1 标题"）
            num_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', title)
            if num_match:
                section_number = num_match.group(1)
                current_section = num_match.group(2)
            else:
                current_section = title
        elif h4_match:
            # H4 标题：提取编号和标题
            title = h4_match.group(1).strip()
            num_match = re.match(r'^(\d+(?:\.\d+)*)\s+(.+)$', title)
            if num_match:
                section_number = num_match.group(1)
                current_section = num_match.group(2)
            else:
                current_section = title
        
        # 检查是否是 Mermaid 代码块开始
        if line.strip() == '```mermaid':
            # 查找代码块结束
            mermaid_lines = []
            j = i + 1
            while j < len(lines):
                if lines[j].strip() == '```':
                    break
                mermaid_lines.append(lines[j])
                j += 1
            
            if mermaid_lines:
                mermaid_code = '\n'.join(mermaid_lines)
                mermaid_blocks.append((mermaid_code, current_section, section_number, i + 1))
    
    return mermaid_blocks


def generate_filename(section_number: Optional[str], section_title: Optional[str], index: int) -> str:
    """
    根据章节信息生成文件名
    
    Args:
        section_number: 章节编号（如 "1.1.1"）
        section_title: 章节标题
        index: 索引（如果同一章节有多个图表）
    
    Returns:
        文件名（不含扩展名）
    """
    parts = []
    
    if section_number:
        # 将章节编号转换为文件名格式（1.1.1 -> 1-1-1）
        number_part = section_number.replace('.', '-')
        parts.append(number_part)
    
    if section_title:
        # 清理标题，移除特殊字符
        clean_title = re.sub(r'[^\w\s-]', '', section_title)
        clean_title = re.sub(r'\s+', '-', clean_title)
        parts.append(clean_title)
    
    if not parts:
        parts.append(f"mermaid-{index}")
    
    filename = '-'.join(parts)
    
    # 如果同一章节有多个图表，添加索引
    if index > 0:
        filename = f"{filename}-{index}"
    
    return filename


def convert_mermaid_to_png(mermaid_code: str, output_path: Path, script_path: Path) -> bool:
    """
    调用 mermaid_to_png.sh 转换 Mermaid 代码为 PNG
    
    Args:
        mermaid_code: Mermaid 代码
        output_path: 输出 PNG 文件路径
        script_path: mermaid_to_png.sh 脚本路径
    
    Returns:
        是否成功
    """
    try:
        # 从标准输入传递 Mermaid 代码
        # 根据 mermaid_to_png.sh 的实现，从标准输入转换时：
        # echo "graph TD; A-->B" | bash mermaid_to_png.sh [output_dir] [output_name]
        output_dir = str(output_path.parent)
        output_name = output_path.name
        
        process = subprocess.Popen(
            ['bash', str(script_path), output_dir, output_name],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(script_path.parent)  # 在脚本目录执行
        )
        
        stdout, stderr = process.communicate(input=mermaid_code)
        
        if process.returncode != 0:
            print(f"错误: 转换失败: {stderr}", file=sys.stderr)
            return False
        
        # 检查输出文件是否生成
        if not output_path.exists():
            print(f"警告: 输出文件未生成: {output_path}", file=sys.stderr)
            return False
        
        return True
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        return False


def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("错误: 请指定 Markdown 文件路径")
        print("")
        print("使用方法:")
        print("  python3 extract_and_convert_mermaid.py <markdown_file> [output_dir]")
        print("")
        sys.exit(1)
    
    markdown_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("./assets/batch-logger")
    
    if not markdown_file.exists():
        print(f"错误: 文件不存在: {markdown_file}")
        sys.exit(1)
    
    # 读取 Markdown 文件
    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取 Mermaid 代码块
    mermaid_blocks = extract_mermaid_blocks(content)
    
    if not mermaid_blocks:
        print("未找到 Mermaid 代码块")
        sys.exit(0)
    
    print(f"找到 {len(mermaid_blocks)} 个 Mermaid 代码块")
    print("")
    
    # 创建输出目录
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 获取脚本目录（当前脚本所在目录）
    script_dir = Path(__file__).parent
    mermaid_script = script_dir / "mermaid_to_png.sh"
    
    if not mermaid_script.exists():
        print(f"错误: 找不到 mermaid_to_png.sh: {mermaid_script}")
        sys.exit(1)
    
    # 转换每个 Mermaid 代码块
    image_list = []
    section_counts = {}  # 用于跟踪同一章节的图表数量
    
    for i, (mermaid_code, section_title, section_number, line_num) in enumerate(mermaid_blocks, 1):
        # 生成唯一键
        section_key = f"{section_number}-{section_title}"
        if section_key not in section_counts:
            section_counts[section_key] = 0
        section_counts[section_key] += 1
        index = section_counts[section_key] - 1
        
        # 生成文件名
        filename = generate_filename(section_number, section_title, index)
        output_path = output_dir / f"{filename}.png"
        
        print(f"[{i}/{len(mermaid_blocks)}] 转换: {filename}.png")
        if section_title:
            print(f"  章节: {section_title}")
        
        # 转换
        if convert_mermaid_to_png(mermaid_code, output_path, mermaid_script):
            # 记录到清单
            display_title = f"{section_number} {section_title}" if section_number and section_title else (section_title or f"图表 {i}")
            image_list.append((output_path.name, display_title))
            print(f"  ✓ 成功: {output_path}")
        else:
            print(f"  ✗ 失败")
        print("")
    
    # 生成 image_list.txt
    list_file = output_dir / "image_list.txt"
    with open(list_file, 'w', encoding='utf-8') as f:
        for filename, title in image_list:
            f.write(f"{filename}\t{title}\n")
    
    print(f"✓ 转换完成: {len(image_list)}/{len(mermaid_blocks)} 个图表")
    print(f"✓ 清单文件: {list_file}")
    print("")
    print("下一步:")
    print(f"  1. 查看图片清单: cat {list_file}")
    print(f"  2. 在 WIKI 文档中使用相对路径引用图片")
    print(f"  3. 为每个图片添加说明文字")


if __name__ == "__main__":
    main()
