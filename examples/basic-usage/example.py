#!/usr/bin/env python3
"""
基础使用示例

演示如何使用 Prompt Engine 的核心功能。
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

from prompt_engine import PromptParser, PromptMerger, PromptValidator, PromptGenerator


def main():
    """主函数"""
    base_path = str(project_root)

    print("=" * 60)
    print("Prompt Engine 基础使用示例")
    print("=" * 60)
    print()

    # 1. 解析提示词文件
    print("1. 解析提示词文件")
    print("-" * 60)
    parser = PromptParser(base_path)
    try:
        prompt = parser.parse_file("prompts/stages/common/mode/common/mode-common.md")
        print(f"✓ 成功解析: {prompt['path']}")
        print(f"  标题: {prompt['metadata'].get('title', 'N/A')}")
        print(f"  概述: {prompt['metadata'].get('overview', 'N/A')[:50]}...")
    except Exception as e:
        print(f"✗ 解析失败: {e}")
    print()

    # 2. 验证提示词
    print("2. 验证提示词文件")
    print("-" * 60)
    validator = PromptValidator(base_path)
    try:
        is_valid, errors = validator.validate_file("prompts/stages/common/mode/common/mode-common.md")
        if is_valid:
            print("✓ 验证通过")
        else:
            print("✗ 验证失败:")
            for error in errors:
                print(f"  - {error}")
    except Exception as e:
        print(f"✗ 验证失败: {e}")
    print()

    # 3. 合并提示词
    print("3. 合并提示词文件")
    print("-" * 60)
    merger = PromptMerger(base_path)
    try:
        output_file = merger.merge_by_stage("common", "examples/basic-usage/merged_common.md")
        print(f"✓ 合并完成: {output_file}")
    except Exception as e:
        print(f"✗ 合并失败: {e}")
    print()

    # 4. 列出模板
    print("4. 列出可用模板")
    print("-" * 60)
    generator = PromptGenerator(base_path)
    templates = generator.list_templates()
    if templates:
        print(f"✓ 找到 {len(templates)} 个模板:")
        for template in templates:
            print(f"  - {template}")
    else:
        print("⚠ 未找到模板")
    print()

    print("=" * 60)
    print("示例完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()

