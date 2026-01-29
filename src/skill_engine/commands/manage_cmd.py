"""Skills 管理命令模块

提供检验、优化、整合、优先级管理功能
"""
import json
from collections import defaultdict
from pathlib import Path
from typing import Optional

from ..utils.skills_analyzer import SkillsAnalyzer


def manage_skills(
    action: str,
    skill_name: Optional[str] = None,
    output_file: Optional[str] = None,
    format: str = 'text'
):
    """
    管理 skills：检验、优化、整合、优先级
    
    Args:
        action: 操作类型 (validate, optimize, integrate, priority, all)
        skill_name: 可选的 skill 名称（如果指定，只处理该 skill）
        output_file: 输出文件路径（可选）
        format: 输出格式 (text, json)
    """
    analyzer = SkillsAnalyzer()
    analyzer.load_all_skills()
    
    if action == 'validate' or action == 'all':
        _validate_skills(analyzer, skill_name, output_file, format)
    
    if action == 'optimize' or action == 'all':
        _optimize_skills(analyzer, skill_name, output_file, format)
    
    if action == 'integrate' or action == 'all':
        _integrate_skills(analyzer, skill_name, output_file, format)
    
    if action == 'priority' or action == 'all':
        _priority_skills(analyzer, skill_name, output_file, format)
    
    if action == 'all':
        _generate_full_report(analyzer, output_file, format)


def _validate_skills(
    analyzer: SkillsAnalyzer,
    skill_name: Optional[str],
    output_file: Optional[str],
    format: str
):
    """检验 skills"""
    print("=" * 60)
    print("🔍 Skills 检验报告")
    print("=" * 60)
    print()
    
    result = analyzer.validate_all()
    
    if skill_name:
        # 只显示指定 skill
        if skill_name in analyzer.skills:
            skill_info = analyzer.skills[skill_name]
            _print_skill_validation(skill_info)
        else:
            print(f"❌ Skill 不存在: {skill_name}")
        return
    
    # 显示所有 skills 的检验结果
    total_skills = len(result.skills)
    skills_with_issues = len(result.quality_issues)
    skills_missing_sections = len(result.missing_sections)
    duplicates_count = len(result.duplicates)
    
    print(f"📊 统计信息:")
    print(f"  - 总 skills 数: {total_skills}")
    print(f"  - 有问题的 skills: {skills_with_issues}")
    print(f"  - 缺少章节的 skills: {skills_missing_sections}")
    print(f"  - 重复内容对: {duplicates_count}")
    print()
    
    # 显示问题详情
    if result.quality_issues:
        print("⚠️  质量问题:")
        print("-" * 60)
        for skill_name, issues in result.quality_issues.items():
            print(f"  {skill_name}:")
            for issue in issues:
                print(f"    - {issue}")
        print()
    
    if result.missing_sections:
        print("📝 缺少章节:")
        print("-" * 60)
        for skill_name, sections in result.missing_sections.items():
            print(f"  {skill_name}:")
            for section in sections:
                print(f"    - {section}")
        print()
    
    if result.duplicates:
        print("🔄 重复内容:")
        print("-" * 60)
        for skill1, skill2, similarity in result.duplicates:
            print(f"  {skill1} ↔ {skill2} (相似度: {similarity:.1%})")
        print()
    
    # 输出到文件
    if output_file:
        _save_validation_report(result, output_file, format)


def _print_skill_validation(skill_info):
    """打印单个 skill 的检验结果"""
    print(f"Skill: {skill_info.name}")
    print(f"分类: {skill_info.category}")
    print(f"路径: {skill_info.path}")
    print(f"行数: {skill_info.line_count}")
    print()
    
    # 元数据
    print("📋 元数据:")
    metadata = skill_info.metadata
    print(f"  - 名称: {metadata.get('name', 'N/A')}")
    print(f"  - 描述: {metadata.get('description', 'N/A')}")
    print(f"  - 标签: {', '.join(metadata.get('tags', []))}")
    print()
    
    # 问题
    if skill_info.issues:
        print("⚠️  问题:")
        for issue in skill_info.issues:
            print(f"  - {issue}")
        print()
    else:
        print("✅ 未发现问题")
        print()


def _optimize_skills(
    analyzer: SkillsAnalyzer,
    skill_name: Optional[str],
    output_file: Optional[str],
    format: str
):
    """优化 skills"""
    print("=" * 60)
    print("✨ Skills 优化建议")
    print("=" * 60)
    print()
    
    if not analyzer.result:
        analyzer.validate_all()
    
    suggestions = analyzer.optimize_suggestions()
    
    if skill_name:
        # 只显示指定 skill
        if skill_name in suggestions:
            print(f"Skill: {skill_name}")
            print("-" * 60)
            for suggestion in suggestions[skill_name]:
                print(f"  💡 {suggestion}")
        elif skill_name in analyzer.skills:
            print(f"✅ {skill_name} 无需优化")
        else:
            print(f"❌ Skill 不存在: {skill_name}")
        return
    
    # 显示所有优化建议
    if not suggestions:
        print("✅ 所有 skills 都符合优化标准")
        return
    
    for skill_name, skill_suggestions in suggestions.items():
        print(f"📌 {skill_name}:")
        for suggestion in skill_suggestions:
            print(f"  💡 {suggestion}")
        print()
    
    # 输出到文件
    if output_file:
        _save_optimization_report(suggestions, output_file, format)


def _integrate_skills(
    analyzer: SkillsAnalyzer,
    skill_name: Optional[str],
    output_file: Optional[str],
    format: str
):
    """整合 skills"""
    print("=" * 60)
    print("🔗 Skills 整合分析")
    print("=" * 60)
    print()
    
    if not analyzer.result:
        analyzer.validate_all()
    
    report = analyzer.generate_integration_report()
    print(report)
    
    # 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)


def _priority_skills(
    analyzer: SkillsAnalyzer,
    skill_name: Optional[str],
    output_file: Optional[str],
    format: str
):
    """优先级管理"""
    print("=" * 60)
    print("🎯 Skills 优先级分析")
    print("=" * 60)
    print()
    
    if not analyzer.result:
        analyzer.validate_all()
    
    if skill_name:
        # 只显示指定 skill
        if skill_name in analyzer.skills:
            skill_info = analyzer.skills[skill_name]
            priority_info = analyzer.result.priority_analysis.get(skill_name, {})
            
            print(f"Skill: {skill_name}")
            print(f"当前优先级: {skill_info.priority or '未设置'}")
            print(f"分类: {skill_info.category}")
            print(f"基础优先级: {priority_info.get('base_priority', 'N/A')}")
            print(f"标签: {', '.join(priority_info.get('tags', []))}")
            print()
            
            # 优先级建议
            category = skill_info.category
            current_priority = skill_info.priority
            if category == 'core' and current_priority != 1:
                print("💡 建议: core 分类的 skill 应该设置优先级为 1")
            elif category in ['code', 'documentation', 'workflow'] and current_priority < 3:
                print(f"💡 建议: {category} 分类的 skill 通常优先级为 3-4")
        else:
            print(f"❌ Skill 不存在: {skill_name}")
        return
    
    # 显示优先级报告
    report = analyzer.generate_priority_report()
    print(report)
    
    # 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)


def _generate_full_report(
    analyzer: SkillsAnalyzer,
    output_file: Optional[str],
    format: str
):
    """生成完整报告"""
    print("📊 正在生成完整分析报告...")
    print()
    
    if not analyzer.result:
        analyzer.validate_all()
    
    analyzer.optimize_suggestions()
    
    if format == 'json':
        if output_file:
            _save_json_report(analyzer, output_file)
        return
    
    # 生成 Markdown 格式报告
    result = analyzer.result
    report_parts = []
    
    # 报告标题
    from datetime import datetime
    report_parts.append("# Skills 分析报告")
    report_parts.append("")
    report_parts.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    # 1. 检验报告
    report_parts.append("## 1. 检验报告")
    report_parts.append("")
    report_parts.append("### 统计信息")
    report_parts.append("")
    report_parts.append("| 项目 | 数量 |")
    report_parts.append("|------|------|")
    report_parts.append(f"| 总 skills 数 | {len(result.skills)} |")
    report_parts.append(f"| 有问题的 skills | {len(result.quality_issues)} |")
    report_parts.append(f"| 缺少章节的 skills | {len(result.missing_sections)} |")
    report_parts.append(f"| 重复内容对 | {len(result.duplicates)} |")
    report_parts.append("")
    
    # 质量问题详情
    if result.quality_issues:
        report_parts.append("### ⚠️ 质量问题")
        report_parts.append("")
        for skill_name, issues in result.quality_issues.items():
            report_parts.append(f"#### {skill_name}")
            report_parts.append("")
            for issue in issues:
                report_parts.append(f"- {issue}")
            report_parts.append("")
    
    # 缺少章节
    if result.missing_sections:
        report_parts.append("### 📝 缺少章节")
        report_parts.append("")
        for skill_name, sections in result.missing_sections.items():
            report_parts.append(f"#### {skill_name}")
            report_parts.append("")
            for section in sections:
                report_parts.append(f"- {section}")
            report_parts.append("")
    
    # 重复内容
    if result.duplicates:
        report_parts.append("### 🔄 重复内容")
        report_parts.append("")
        report_parts.append("| Skill 1 | Skill 2 | 相似度 |")
        report_parts.append("|---------|---------|--------|")
        for skill1, skill2, similarity in result.duplicates:
            report_parts.append(f"| {skill1} | {skill2} | {similarity:.1%} |")
        report_parts.append("")
    
    report_parts.append("---")
    report_parts.append("")
    
    # 2. 优先级分析
    report_parts.append("## 2. 优先级分析")
    report_parts.append("")
    
    priority_groups = defaultdict(list)
    for skill_name, skill_info in analyzer.skills.items():
        priority = skill_info.priority or 5
        priority_groups[priority].append((skill_name, skill_info))
    
    for priority in sorted(priority_groups.keys()):
        skills = priority_groups[priority]
        report_parts.append(f"### 优先级 {priority} ({len(skills)} 个 skills)")
        report_parts.append("")
        report_parts.append("| Skill | 分类 | 描述 |")
        report_parts.append("|-------|------|------|")
        
        for skill_name, skill_info in sorted(skills, key=lambda x: x[0]):
            category = skill_info.category
            description = skill_info.metadata.get('description', '')[:60]
            if len(description) > 60:
                description += "..."
            report_parts.append(f"| `{skill_name}` | {category} | {description} |")
        
        report_parts.append("")
    
    report_parts.append("---")
    report_parts.append("")
    
    # 3. 整合建议
    report_parts.append("## 3. 整合建议")
    report_parts.append("")
    
    if not result.integration_opportunities:
        report_parts.append("✅ 未发现明显的整合机会")
        report_parts.append("")
    else:
        # 合并建议
        merge_ops = [op for op in result.integration_opportunities if op['type'] == 'merge']
        if merge_ops:
            report_parts.append("### 🔄 合并建议")
            report_parts.append("")
            report_parts.append("| Skill 1 | Skill 2 | 相似度 | 建议 |")
            report_parts.append("|---------|---------|--------|------|")
            for op in merge_ops:
                skills = op['skills']
                similarity = op['similarity']
                suggestion = op['suggestion']
                report_parts.append(f"| {skills[0]} | {skills[1]} | {similarity:.1%} | {suggestion} |")
            report_parts.append("")
        
        # 分组建议
        group_ops = [op for op in result.integration_opportunities if op['type'] == 'group']
        if group_ops:
            report_parts.append("### 📁 分组建议")
            report_parts.append("")
            for op in group_ops:
                report_parts.append(f"#### 标签 `{op['tag']}` ({len(op['skills'])} 个 skills)")
                report_parts.append("")
                skills_list = ", ".join([f"`{s}`" for s in op['skills'][:10]])
                if len(op['skills']) > 10:
                    skills_list += f", ... (共 {len(op['skills'])} 个)"
                report_parts.append(f"{skills_list}")
                report_parts.append("")
    
    report_parts.append("---")
    report_parts.append("")
    
    # 4. 优化建议
    report_parts.append("## 4. 优化建议")
    report_parts.append("")
    
    suggestions = analyzer.result.optimization_suggestions
    if suggestions:
        for skill_name, skill_suggestions in sorted(suggestions.items()):
            report_parts.append(f"### {skill_name}")
            report_parts.append("")
            for suggestion in skill_suggestions:
                report_parts.append(f"- 💡 {suggestion}")
            report_parts.append("")
    else:
        report_parts.append("✅ 所有 skills 都符合优化标准")
        report_parts.append("")
    
    full_report = "\n".join(report_parts)
    
    # 在终端显示简化版本
    print("=" * 60)
    print("📊 完整分析报告")
    print("=" * 60)
    print()
    print(f"总 skills 数: {len(result.skills)}")
    print(f"有问题的 skills: {len(result.quality_issues)}")
    print(f"优化建议数: {len(suggestions)}")
    print()
    
    # 输出到文件
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_report)
        print(f"✅ 报告已保存到: {output_file}")
        print(f"📄 文件大小: {len(full_report.encode('utf-8'))} 字节")
        print(f"💡 提示: 使用 Markdown 编辑器打开查看完整报告")


def _save_validation_report(result, output_file: str, format: str):
    """保存检验报告"""
    if format == 'json':
        data = {
            'total_skills': len(result.skills),
            'skills_with_issues': len(result.quality_issues),
            'skills_missing_sections': len(result.missing_sections),
            'duplicates': [
                {'skill1': s1, 'skill2': s2, 'similarity': sim}
                for s1, s2, sim in result.duplicates
            ],
            'quality_issues': result.quality_issues,
            'missing_sections': result.missing_sections
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        # 文本格式已在上面打印
        pass


def _save_optimization_report(suggestions: dict, output_file: str, format: str):
    """保存优化报告"""
    if format == 'json':
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(suggestions, f, ensure_ascii=False, indent=2)
    else:
        # 文本格式已在上面打印
        pass


def _save_json_report(analyzer: SkillsAnalyzer, output_file: str):
    """保存 JSON 格式的完整报告"""
    result = analyzer.result
    
    data = {
        'summary': {
            'total_skills': len(result.skills),
            'skills_with_issues': len(result.quality_issues),
            'skills_missing_sections': len(result.missing_sections),
            'duplicates_count': len(result.duplicates),
            'integration_opportunities': len(result.integration_opportunities)
        },
        'skills': {
            name: {
                'name': info.name,
                'category': info.category,
                'priority': info.priority,
                'line_count': info.line_count,
                'issues': info.issues,
                'suggestions': info.suggestions,
                'dependencies': list(info.dependencies),
                'metadata': info.metadata
            }
            for name, info in analyzer.skills.items()
        },
        'duplicates': [
            {'skill1': s1, 'skill2': s2, 'similarity': sim}
            for s1, s2, sim in result.duplicates
        ],
        'quality_issues': result.quality_issues,
        'missing_sections': result.missing_sections,
        'optimization_suggestions': result.optimization_suggestions,
        'priority_analysis': result.priority_analysis,
        'integration_opportunities': result.integration_opportunities
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ JSON 报告已保存到: {output_file}")
