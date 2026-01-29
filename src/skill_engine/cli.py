#!/usr/bin/env python3
"""
Skill Engine CLI

提供 skills 管理的命令行工具
"""
import argparse
import sys
from pathlib import Path

from .commands import (
    list_skills,
    read_skill,
    create_skill,
    validate_skill,
    search_skills,
    show_stats,
    manage_skills,
    optimize_skills,
    analyze_skills,
    apply_optimize,
    generate_agents
)


def create_parser():
    """创建命令行解析器"""
    parser = argparse.ArgumentParser(
        description="Skill Engine - Skills 管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  skill-engine list                          # 列出所有 skills
  skill-engine list common                   # 列出 common 分类的 skills
  skill-engine read code-organization        # 读取 skill
  skill-engine create my-skill               # 创建新 skill
  skill-engine validate code-organization    # 验证 skill 格式
  skill-engine search keyword                # 搜索 skills
  skill-engine search --tag code             # 按标签搜索
  skill-engine stats                         # 显示统计信息
  skill-engine info                          # 显示项目信息
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # list 命令
    list_parser = subparsers.add_parser('list', help='列出 skills')
    list_parser.add_argument('category', nargs='?', help='可选的分类过滤')
    
    # read 命令
    read_parser = subparsers.add_parser('read', help='读取 skill')
    read_parser.add_argument('skill', help='skill 名称或路径')
    
    # create 命令
    create_parser = subparsers.add_parser('create', help='创建新 skill')
    create_parser.add_argument('name', help='skill 名称')
    create_parser.add_argument('--category', default='common', help='分类（默认: common）')
    create_parser.add_argument('--non-interactive', action='store_true', help='非交互模式')
    
    # validate 命令
    validate_parser = subparsers.add_parser('validate', help='验证 skill 格式')
    validate_parser.add_argument('skill', help='skill 名称或路径')
    
    # search 命令
    search_parser = subparsers.add_parser('search', help='搜索 skills')
    search_group = search_parser.add_mutually_exclusive_group(required=True)
    search_group.add_argument('keyword', nargs='?', help='搜索关键词')
    search_group.add_argument('--tag', help='按标签搜索')
    
    # stats 命令
    subparsers.add_parser('stats', help='显示统计信息')
    
    # info 命令
    subparsers.add_parser('info', help='显示项目信息')
    
    # manage 命令
    manage_parser = subparsers.add_parser('manage', help='管理 skills：检验、优化、整合、优先级')
    manage_parser.add_argument(
        'action',
        nargs='?',
        choices=['validate', 'optimize', 'integrate', 'priority', 'all'],
        default='all',
        help='操作类型：validate(检验), optimize(优化), integrate(整合), priority(优先级), all(全部，默认)'
    )
    manage_parser.add_argument('--skill', help='指定 skill 名称（可选）')
    manage_parser.add_argument('--output', '-o', help='输出文件路径（默认: skills_report.txt）')
    manage_parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式（默认: text）')
    
    # 添加简单的 report 命令
    report_parser = subparsers.add_parser('report', help='生成完整的 skills 分析报告（简化版）')
    report_parser.add_argument('--output', '-o', default='skills_report.md', help='输出文件路径（默认: skills_report.md）')
    report_parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式（默认: text，输出为 Markdown）')
    
    # 添加 optimize 命令
    optimize_parser = subparsers.add_parser('optimize', help='一键优化 skills（根据分析报告）')
    optimize_parser.add_argument('--apply', action='store_true', help='实际应用优化（默认只是试运行）')
    optimize_parser.add_argument('--skill', help='指定要优化的 skill（可选）')
    optimize_parser.add_argument('--from-report', '-f', help='从报告文件读取优化建议（默认: skills_report.md）')
    optimize_parser.add_argument('--output', '-o', default='optimization_report.md', help='输出优化报告文件路径（默认: optimization_report.md）')
    
    # 添加 analyze 命令（分析 skills 并生成报告）
    analyze_parser = subparsers.add_parser('analyze', help='分析当前 skills 并生成优化报告')
    analyze_parser.add_argument('--output', '-o', help='输出文件路径（默认: skills_report.md）')
    analyze_parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式（默认: text）')
    analyze_parser.add_argument('--skill', help='指定要分析的 skill（可选）')
    
    # 添加 apply-optimize 命令（根据报告应用优化）
    apply_optimize_parser = subparsers.add_parser('apply-optimize', help='根据分析报告对需要优化的 skills 进行优化')
    apply_optimize_parser.add_argument('--from-report', '-f', help='报告文件路径（默认: skills_report.md）')
    apply_optimize_parser.add_argument('--skill', help='指定要优化的 skill（可选）')
    apply_optimize_parser.add_argument('--dry-run', action='store_true', help='试运行模式（不实际修改文件）')
    apply_optimize_parser.add_argument('--output', '-o', help='输出优化报告文件路径（可选）')
    
    # 添加 generate 命令（生成 AGENTS.md）
    generate_parser = subparsers.add_parser('generate', help='生成 AGENTS.md 文件')
    generate_parser.add_argument('--output', '-o', help='输出文件路径（默认: AGENTS.md）')
    
    return parser


def show_info():
    """显示项目信息"""
    print("=" * 60)
    print("Skill Engine - Skills 管理工具")
    print("=" * 60)
    print()
    print("版本: 2.0.0")
    print("描述: 基于 Skills 的 AI 提示词工程框架")
    print()
    print("使用方法:")
    print("  skill-engine list                   # 列出所有 skills")
    print("  skill-engine read <skill-name>      # 读取 skill")
    print("  skill-engine create <skill-name>    # 创建新 skill")
    print("  skill-engine validate <skill-name>  # 验证 skill")
    print("  skill-engine search <keyword>       # 搜索 skills")
    print("  skill-engine stats                  # 统计信息")
    print("  skill-engine analyze                 # 分析 skills 并生成报告（推荐）")
    print("  skill-engine apply-optimize           # 根据报告应用优化（推荐）")
    print("  skill-engine report                  # 生成完整分析报告（简化版）")
    print("  skill-engine optimize                # 一键优化 skills")
    print("  skill-engine generate                # 生成 AGENTS.md 文件")
    print("  skill-engine manage <action>         # 管理 skills")
    print("  skill-engine info                    # 项目信息")
    print()
    print("示例:")
    print("  skill-engine list common")
    print("  skill-engine read common/code/code-organization")
    print("  skill-engine create my-skill --category common/code")
    print("  skill-engine search --tag code")
    print("  skill-engine analyze                  # 分析所有 skills 并生成报告")
    print("  skill-engine analyze --skill core/act-mode  # 分析单个 skill")
    print("  skill-engine apply-optimize           # 根据报告应用优化（实际修改）")
    print("  skill-engine apply-optimize --dry-run # 试运行模式（查看优化计划）")
    print("  skill-engine report                  # 生成完整报告（最简单）")
    print("  skill-engine optimize                # 查看优化计划（试运行）")
    print("  skill-engine optimize --apply        # 应用优化（实际修改）")
    print("  skill-engine generate                # 生成 AGENTS.md 文件")
    print("  skill-engine generate -o custom.md    # 生成到指定文件")
    print("  skill-engine manage validate          # 检验所有 skills")
    print()


def main():
    """主函数"""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'list':
            list_skills(args.category)
        
        elif args.command == 'read':
            read_skill(args.skill)
        
        elif args.command == 'create':
            create_skill(
                args.name,
                category=args.category,
                interactive=not args.non_interactive
            )
        
        elif args.command == 'validate':
            success = validate_skill(args.skill)
            sys.exit(0 if success else 1)
        
        elif args.command == 'search':
            if args.tag:
                search_skills(tag=args.tag)
            else:
                search_skills(keyword=args.keyword)
        
        elif args.command == 'stats':
            show_stats()
        
        elif args.command == 'info':
            show_info()
        
        elif args.command == 'manage':
            action = args.action if args.action else 'all'
            # 如果没有指定输出文件，根据格式设置默认文件名
            default_output = 'skills_report.md' if args.format == 'text' else 'skills_report.json'
            manage_skills(
                action=action,
                skill_name=args.skill,
                output_file=args.output or default_output,
                format=args.format
            )
        
        elif args.command == 'report':
            # 简化版：直接生成完整报告
            print("📊 正在生成 Skills 分析报告...")
            print()
            manage_skills(
                action='all',
                skill_name=None,
                output_file=args.output,
                format=args.format
            )
        
        elif args.command == 'optimize':
            # 一键优化
            from_report = args.from_report or ('skills_report.md' if Path('skills_report.md').exists() else None)
            optimize_skills(
                dry_run=not args.apply,
                output_file=args.output,
                skill_name=args.skill,
                from_report=from_report
            )
        
        elif args.command == 'analyze':
            # 分析 skills 并生成报告
            analyze_skills(
                output_file=args.output,
                format=args.format,
                skill_name=args.skill
            )
        
        elif args.command == 'apply-optimize':
            # 根据报告应用优化
            apply_optimize(
                from_report=args.from_report,
                skill_name=args.skill,
                dry_run=args.dry_run,
                output_file=args.output
            )
        
        elif args.command == 'generate':
            # 生成 AGENTS.md
            generate_agents(output_path=args.output)
    
    except KeyboardInterrupt:
        print("\n\n已取消")
        sys.exit(0)
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
