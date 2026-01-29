"""Skills 分析命令模块

分析当前 skills 并生成优化报告
"""
from pathlib import Path
from typing import Optional

from ..utils.skills_analyzer import SkillsAnalyzer
from .manage_cmd import manage_skills


def analyze_skills(
    output_file: Optional[str] = None,
    format: str = 'text',
    skill_name: Optional[str] = None
):
    """
    分析当前 skills 并生成报告
    
    Args:
        output_file: 输出文件路径（默认: skills_report.md）
        format: 输出格式（text 或 json，默认: text）
        skill_name: 指定要分析的 skill（可选）
    """
    print("=" * 60)
    print("📊 Skills 分析工具")
    print("=" * 60)
    print()
    print("正在分析 skills...")
    print()
    
    # 初始化分析器
    analyzer = SkillsAnalyzer()
    analyzer.load_all_skills()
    
    # 如果指定了单个 skill，只分析该 skill
    if skill_name:
        if skill_name not in analyzer.skills:
            print(f"❌ Skill 不存在: {skill_name}")
            return
        
        # 只分析指定的 skill
        skill_info = analyzer.skills[skill_name]
        print(f"📌 分析 Skill: {skill_name}")
        print(f"   分类: {skill_info.category}")
        print(f"   路径: {skill_info.path}")
        print()
        
        # 执行验证
        analyzer.validate_all()
        analyzer.optimize_suggestions()
        
        # 生成单个 skill 的报告
        _generate_single_skill_report(analyzer, skill_name, output_file, format)
    else:
        # 分析所有 skills - 使用 manage_skills 生成完整报告
        default_output = output_file or 'skills_report.md'
        # 临时保存 analyzer 到 manage_skills 可以访问的地方
        # 由于 manage_skills 内部会创建新的 analyzer，我们直接调用它
        manage_skills(
            action='all',
            skill_name=None,
            output_file=default_output,
            format=format
        )
    
    print()
    print("=" * 60)
    print("✅ 分析完成")
    print("=" * 60)
    print()
    
    # 显示报告文件信息和下一步提示
    if skill_name:
        # 单个 skill 分析
        report_file = output_file or f'{skill_name.replace("/", "_")}_report.md'
        print(f"📄 报告文件: {report_file}")
        print()
        print("💡 下一步:")
        print(f"   使用以下命令应用优化:")
        print(f"   ./skill-engine apply-optimize --skill {skill_name}")
        print(f"   或: python3 -m skill_engine.cli apply-optimize --skill {skill_name}")
        print()
    else:
        # 所有 skills 分析
        report_file = output_file or 'skills_report.md'
        print(f"📄 报告文件: {report_file}")
        print()
        print("💡 下一步:")
        print(f"   使用以下命令应用优化:")
        print(f"   ./skill-engine apply-optimize --from-report {report_file}")
        print(f"   或: python3 -m skill_engine.cli apply-optimize --from-report {report_file}")
        print()


def _generate_single_skill_report(
    analyzer: SkillsAnalyzer,
    skill_name: str,
    output_file: Optional[str],
    format: str
):
    """生成单个 skill 的分析报告"""
    skill_info = analyzer.skills[skill_name]
    result = analyzer.result
    
    if format == 'json':
        # JSON 格式
        import json
        data = {
            'skill': {
                'name': skill_info.name,
                'category': skill_info.category,
                'path': str(skill_info.path),
                'line_count': skill_info.line_count,
                'priority': skill_info.priority,
                'metadata': skill_info.metadata,
                'issues': skill_info.issues,
                'suggestions': skill_info.suggestions,
                'dependencies': list(skill_info.dependencies)
            },
            'quality_issues': result.quality_issues.get(skill_name, []),
            'missing_sections': result.missing_sections.get(skill_name, []),
            'optimization_suggestions': result.optimization_suggestions.get(skill_name, [])
        }
        
        output_path = output_file or f'{skill_name.replace("/", "_")}_report.json'
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ JSON 报告已保存到: {output_path}")
    else:
        # Markdown 格式
        from datetime import datetime
        report_parts = []
        
        report_parts.append(f"# Skill 分析报告: {skill_name}")
        report_parts.append("")
        report_parts.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_parts.append("")
        report_parts.append("---")
        report_parts.append("")
        
        # 基本信息
        report_parts.append("## 基本信息")
        report_parts.append("")
        report_parts.append(f"- **名称**: {skill_info.name}")
        report_parts.append(f"- **分类**: {skill_info.category}")
        report_parts.append(f"- **路径**: `{skill_info.path}`")
        report_parts.append(f"- **行数**: {skill_info.line_count}")
        report_parts.append(f"- **优先级**: {skill_info.priority or '未设置'}")
        report_parts.append("")
        
        # 元数据
        metadata = skill_info.metadata
        report_parts.append("### 元数据")
        report_parts.append("")
        report_parts.append(f"- **描述**: {metadata.get('description', 'N/A')}")
        report_parts.append(f"- **标签**: {', '.join(metadata.get('tags', []))}")
        report_parts.append("")
        
        # 问题
        if skill_info.issues:
            report_parts.append("## ⚠️ 质量问题")
            report_parts.append("")
            for issue in skill_info.issues:
                report_parts.append(f"- {issue}")
            report_parts.append("")
        
        # 缺少章节
        missing = result.missing_sections.get(skill_name, [])
        if missing:
            report_parts.append("## 📝 缺少章节")
            report_parts.append("")
            for section in missing:
                report_parts.append(f"- {section}")
            report_parts.append("")
        
        # 优化建议
        suggestions = result.optimization_suggestions.get(skill_name, [])
        if suggestions:
            report_parts.append("## 💡 优化建议")
            report_parts.append("")
            for suggestion in suggestions:
                report_parts.append(f"- {suggestion}")
            report_parts.append("")
        else:
            report_parts.append("## ✅ 优化建议")
            report_parts.append("")
            report_parts.append("该 skill 符合优化标准，无需优化")
            report_parts.append("")
        
        # 依赖关系
        if skill_info.dependencies:
            report_parts.append("## 🔗 依赖关系")
            report_parts.append("")
            for dep in skill_info.dependencies:
                report_parts.append(f"- `{dep}`")
            report_parts.append("")
        
        report_parts.append("---")
        report_parts.append("")
        report_parts.append("## 下一步")
        report_parts.append("")
        report_parts.append("要应用优化建议，请运行：")
        report_parts.append("")
        report_parts.append("```bash")
        report_parts.append(f"# 方式 1: 使用项目根目录的脚本（推荐）")
        report_parts.append(f"./skill-engine apply-optimize --skill {skill_name}")
        report_parts.append("")
        report_parts.append(f"# 方式 2: 使用 python -m 方式")
        report_parts.append(f"python3 -m skill_engine.cli apply-optimize --skill {skill_name}")
        report_parts.append("```")
        report_parts.append("")
        
        full_report = "\n".join(report_parts)
        
        output_path = output_file or f'{skill_name.replace("/", "_")}_report.md'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_report)
        
        print(f"✅ 报告已保存到: {output_path}")
        print()
        print("📋 报告摘要:")
        print(f"   - 问题数: {len(skill_info.issues)}")
        print(f"   - 优化建议数: {len(suggestions)}")
        print(f"   - 依赖关系数: {len(skill_info.dependencies)}")
