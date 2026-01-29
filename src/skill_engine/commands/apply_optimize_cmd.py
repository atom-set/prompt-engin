"""Skills 优化应用命令模块

根据分析报告对需要优化的 skills 进行优化
"""
from pathlib import Path
from typing import Optional

from .optimize_cmd import optimize_skills


def apply_optimize(
    from_report: Optional[str] = None,
    skill_name: Optional[str] = None,
    dry_run: bool = False,
    output_file: Optional[str] = None
):
    """
    根据报告对需要优化的 skills 进行优化
    
    Args:
        from_report: 报告文件路径（默认: skills_report.md）
        skill_name: 指定要优化的 skill（可选）
        dry_run: 是否为试运行模式（默认: False，实际应用优化）
        output_file: 输出优化报告文件路径（可选）
    """
    print("=" * 60)
    print("🔧 Skills 优化应用工具")
    print("=" * 60)
    print()
    
    # 确定报告文件
    if not from_report:
        # 尝试查找默认报告文件
        default_reports = ['skills_report.md', 'skills_report.txt']
        for report_file in default_reports:
            if Path(report_file).exists():
                from_report = report_file
                print(f"📄 使用默认报告文件: {from_report}")
                break
        
        if not from_report:
            print("❌ 未找到报告文件")
            print()
            print("💡 请先运行分析命令生成报告:")
            print("   ./skill-engine analyze")
            print("   或: python3 -m skill_engine.cli analyze")
            print()
            print("   或者指定报告文件:")
            print("   ./skill-engine apply-optimize --from-report <报告文件路径>")
            print("   或: python3 -m skill_engine.cli apply-optimize --from-report <报告文件路径>")
            return
    
    # 检查报告文件是否存在
    report_path = Path(from_report)
    if not report_path.exists():
        print(f"❌ 报告文件不存在: {from_report}")
        return
    
    print(f"📄 读取报告文件: {from_report}")
    print()
    
    # 调用 optimize_skills 函数，它已经可以处理从报告文件读取的情况
    # dry_run 参数：如果用户指定了 --dry-run，则为 True（试运行），否则为 False（实际应用）
    optimize_skills(
        dry_run=dry_run,
        output_file=output_file,
        skill_name=skill_name,
        from_report=from_report
    )
