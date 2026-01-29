"""Skills 一键优化命令模块

根据分析报告自动优化 skills
"""
import re
from pathlib import Path
from typing import Dict, List, Optional

from ..utils.skills_analyzer import SkillsAnalyzer
from ..utils.file_utils import read_skill_content


def optimize_skills(
    dry_run: bool = True,
    output_file: Optional[str] = None,
    skill_name: Optional[str] = None,
    from_report: Optional[str] = None
):
    """
    一键优化 skills
    
    Args:
        dry_run: 是否为试运行（不实际修改文件）
        output_file: 输出优化报告文件路径
        skill_name: 指定要优化的 skill（可选）
        from_report: 从报告文件读取优化建议（可选）
    """
    if from_report:
        print(f"📄 从报告文件读取优化建议: {from_report}")
        print()
        
        # 从报告文件解析优化建议
        suggestions = _parse_suggestions_from_report(from_report)
        
        if not suggestions:
            print("❌ 报告文件中没有找到优化建议")
            return
        
        # 加载 skills
        analyzer = SkillsAnalyzer()
        analyzer.load_all_skills()
        
        # 生成优化计划
        optimization_plan = _generate_optimization_plan_from_suggestions(
            analyzer, suggestions, skill_name
        )
    else:
        print("🔧 开始分析 skills...")
        print()
        
        analyzer = SkillsAnalyzer()
        analyzer.load_all_skills()
        analyzer.validate_all()
        suggestions = analyzer.optimize_suggestions()
        
        if not suggestions:
            print("✅ 所有 skills 都符合优化标准，无需优化")
            return
        
        # 生成优化计划
        optimization_plan = _generate_optimization_plan(analyzer, suggestions, skill_name)
    
    if not optimization_plan:
        print("✅ 没有需要优化的内容")
        return
    
    # 显示优化计划
    print("=" * 60)
    print("📋 优化计划")
    print("=" * 60)
    print()
    
    for skill_name, plan in optimization_plan.items():
        print(f"📌 {skill_name}:")
        for action in plan['actions']:
            print(f"  - {action['description']}")
        print()
    
    # 执行优化
    if dry_run:
        print("=" * 60)
        print("ℹ️  试运行模式（不会实际修改文件）")
        print("=" * 60)
        print()
        print("💡 提示: 使用以下命令实际应用优化:")
        print("   ./skill-engine optimize --apply")
        print("   或: python3 -m skill_engine.cli optimize --apply")
        print()
    else:
        print("=" * 60)
        print("🚀 开始应用优化...")
        print("=" * 60)
        print()
        
        applied_count = 0
        for skill_name, plan in optimization_plan.items():
            try:
                if _apply_optimizations(analyzer.skills[skill_name], plan['actions']):
                    applied_count += 1
                    print(f"✅ {skill_name}: 优化完成")
                else:
                    print(f"⚠️  {skill_name}: 部分优化需要手动处理")
            except Exception as e:
                print(f"❌ {skill_name}: 优化失败 - {e}")
        
        print()
        print(f"✅ 完成: {applied_count}/{len(optimization_plan)} 个 skills 已优化")
        print()
    
    # 生成优化报告
    if output_file:
        _save_optimization_report(optimization_plan, analyzer, output_file, dry_run)
        print(f"📄 优化报告已保存到: {output_file}")


def _generate_optimization_plan(
    analyzer: SkillsAnalyzer,
    suggestions: Dict[str, List[str]],
    filter_skill: Optional[str] = None
) -> Dict[str, Dict]:
    """生成优化计划"""
    plan = {}
    
    skills_to_process = [filter_skill] if filter_skill else list(suggestions.keys())
    
    for skill_name in skills_to_process:
        if skill_name not in analyzer.skills:
            continue
        
        skill_info = analyzer.skills[skill_name]
        skill_suggestions = suggestions.get(skill_name, [])
        
        if not skill_suggestions:
            continue
        
        actions = []
        
        for suggestion in skill_suggestions:
            action = _parse_suggestion(suggestion, skill_info)
            if action:
                actions.append(action)
        
        if actions:
            plan[skill_name] = {
                'skill_info': skill_info,
                'actions': actions
            }
    
    return plan


def _parse_suggestion(suggestion: str, skill_info) -> Optional[Dict]:
    """解析优化建议，生成可执行的操作"""
    action = {
        'type': 'unknown',
        'description': suggestion,
        'auto_apply': False
    }
    
    # 添加示例
    if '添加代码示例' in suggestion or '添加使用场景示例' in suggestion:
        action['type'] = 'add_example'
        action['auto_apply'] = False  # 需要手动添加
        action['description'] = '添加代码示例或使用场景示例'
        action['suggestion'] = '在 skill 文件中添加 "### 示例" 章节，包含代码示例或使用场景'
        return action
    
    # 扩展描述
    if '扩展描述' in suggestion:
        action['type'] = 'expand_description'
        action['auto_apply'] = False  # 需要手动扩展
        action['description'] = '扩展 skill 描述，提供更详细的说明'
        action['suggestion'] = f'当前描述: {skill_info.metadata.get("description", "")[:50]}...'
        return action
    
    # 明确依赖关系
    if '明确依赖关系' in suggestion:
        action['type'] = 'add_dependencies'
        action['auto_apply'] = True  # 可以自动添加
        # 提取依赖的 skills
        deps_match = re.search(r'明确依赖关系: (.+)', suggestion)
        if deps_match:
            deps = [d.strip() for d in deps_match.group(1).split(',')]
            action['dependencies'] = deps
            action['description'] = f'添加依赖关系: {", ".join(deps)}'
        return action
    
    return action


def _apply_optimizations(skill_info, actions: List[Dict]) -> bool:
    """应用优化操作"""
    content = read_skill_content(skill_info.path)
    modified = False
    
    for action in actions:
        if not action.get('auto_apply', False):
            continue
        
        if action['type'] == 'add_dependencies':
            # 在"与其他规则的配合"章节添加依赖关系
            if '## 与其他规则的配合' in content:
                section_start = content.find('## 与其他规则的配合')
                section_end = content.find('##', section_start + 1)
                if section_end == -1:
                    section_end = len(content)
                
                section_content = content[section_start:section_end]
                deps = action.get('dependencies', [])
                
                # 检查是否已存在这些依赖（支持多种格式：error-handling, core/error-handling, error-handling-strategy 等）
                new_deps = []
                for dep in deps:
                    # 检查依赖是否已存在（支持完整路径和简单名称）
                    dep_exists = False
                    # 检查简单名称
                    if dep in section_content:
                        dep_exists = True
                    # 检查完整路径（如 core/error-handling）
                    elif '/' in dep and dep.split('/')[-1] in section_content:
                        dep_exists = True
                    # 检查反引号中的名称
                    elif f'`{dep}`' in section_content or f'`{dep.split("/")[-1]}`' in section_content:
                        dep_exists = True
                    
                    if not dep_exists:
                        new_deps.append(dep)
                
                if new_deps:
                    # 在章节末尾添加依赖关系（在章节结束标记之前）
                    # 找到章节内容的末尾（在下一个 ## 之前）
                    insert_pos = section_end
                    
                    # 如果章节末尾有分隔线，在分隔线之前插入
                    if content[insert_pos-3:insert_pos] == '\n---':
                        insert_pos -= 3
                    elif content[insert_pos-1:insert_pos] == '\n':
                        # 在最后一个换行符之前插入
                        pass
                    
                    new_lines = []
                    for dep in new_deps:
                        # 尝试查找完整的 skill 路径
                        full_dep_name = _find_skill_path(dep, skill_info.path.parent.parent)
                        if not full_dep_name:
                            # 如果找不到，使用原始名称
                            full_dep_name = dep
                        new_lines.append(f"- 与 `{full_dep_name}` 配合：相关功能")
                    
                    if new_lines:
                        # 确保在插入位置之前有换行
                        if insert_pos > 0 and content[insert_pos-1] != '\n':
                            insert_text = '\n' + '\n'.join(new_lines) + '\n'
                        else:
                            insert_text = '\n'.join(new_lines) + '\n'
                        content = content[:insert_pos] + insert_text + content[insert_pos:]
                        modified = True
    
    if modified:
        # 保存修改后的内容
        with open(skill_info.path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return modified


def _parse_suggestions_from_report(report_file: str) -> Dict[str, List[str]]:
    """从报告文件中解析优化建议"""
    suggestions = {}
    
    try:
        # 先读取整个文件，查找优化建议章节的位置
        with open(report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找优化建议章节
        section_start = content.find('## 4. 优化建议')
        if section_start == -1:
            # 尝试其他格式
            section_start = content.find('## 优化建议')
        
        if section_start == -1:
            return {}
        
        # 提取章节内容（找到下一个 ## 开头的行，或者到文件末尾）
        section_end = len(content)
        # 从章节开始位置之后查找下一个 ##（不在同一行）
        search_start = section_start + len('## 4. 优化建议')
        # 尝试查找下一个二级标题（## 开头，但不是 ###）
        next_section = content.find('\n## ', search_start)
        if next_section == -1:
            # 如果没有找到，说明这是最后一个章节，直接到文件末尾
            section_end = len(content)
        else:
            section_end = next_section
        
        section_content = content[section_start:section_end]
        lines = section_content.split('\n')
        
        # 解析章节内容
        current_skill = None
        
        for line in lines:
            line_stripped = line.rstrip()
            
            # 跳过章节标题（## 开头的二级标题）
            if line_stripped.startswith('##') and not line_stripped.startswith('###'):
                continue
            
            # 跳过空行
            if not line_stripped:
                continue
            
            # 匹配 skill 名称 (### skill-name)
            skill_match = re.match(r'^###\s+(.+)$', line_stripped)
            if skill_match:
                current_skill = skill_match.group(1).strip()
                if current_skill and current_skill not in suggestions:
                    suggestions[current_skill] = []
                continue
            
            # 匹配优化建议 (- 💡 建议内容)
            if current_skill:
                suggestion_match = re.match(r'^-\s+💡\s+(.+)$', line_stripped)
                if suggestion_match:
                    suggestion = suggestion_match.group(1).strip()
                    # 过滤掉空行和分隔线
                    if suggestion and not suggestion.startswith('---'):
                        suggestions[current_skill].append(suggestion)
        
        # 如果解析成功，显示统计信息
        if suggestions:
            total_suggestions = sum(len(sugs) for sugs in suggestions.values())
            print(f"✅ 从报告中解析到 {len(suggestions)} 个 skills，共 {total_suggestions} 条优化建议")
        
        return suggestions
    
    except FileNotFoundError:
        print(f"❌ 报告文件不存在: {report_file}")
        return {}
    except Exception as e:
        print(f"❌ 读取报告文件时出错: {e}")
        import traceback
        traceback.print_exc()
        return {}


def _generate_optimization_plan_from_suggestions(
    analyzer: SkillsAnalyzer,
    suggestions: Dict[str, List[str]],
    filter_skill: Optional[str] = None
) -> Dict[str, Dict]:
    """从建议生成优化计划"""
    plan = {}
    
    skills_to_process = [filter_skill] if filter_skill else list(suggestions.keys())
    
    for skill_name in skills_to_process:
        if skill_name not in analyzer.skills:
            # 尝试查找 skill（可能是相对路径）
            found = False
            for actual_name in analyzer.skills.keys():
                if actual_name.endswith(skill_name) or skill_name in actual_name:
                    skill_name = actual_name
                    found = True
                    break
            if not found:
                continue
        
        skill_info = analyzer.skills[skill_name]
        skill_suggestions = suggestions.get(skill_name, [])
        
        if not skill_suggestions:
            continue
        
        actions = []
        
        for suggestion in skill_suggestions:
            action = _parse_suggestion(suggestion, skill_info)
            if action:
                actions.append(action)
        
        if actions:
            plan[skill_name] = {
                'skill_info': skill_info,
                'actions': actions
            }
    
    return plan


def _find_skill_path(skill_name: str, skills_dir: Path) -> Optional[str]:
    """查找 skill 的完整路径"""
    # 尝试多种可能的路径
    possible_paths = [
        skills_dir / f"{skill_name}.md",
        skills_dir / skill_name / f"{skill_name.split('/')[-1]}.md",
    ]
    
    # 递归搜索
    for skill_file in skills_dir.rglob("*.md"):
        if skill_file.stem == skill_name.split('/')[-1] or skill_file.name == f"{skill_name.split('/')[-1]}.md":
            rel_path = skill_file.relative_to(skills_dir)
            return str(rel_path.with_suffix('')).replace('\\', '/')
    
    return skill_name


def _save_optimization_report(
    plan: Dict[str, Dict],
    analyzer: SkillsAnalyzer,
    output_file: str,
    dry_run: bool
):
    """保存优化报告"""
    from datetime import datetime
    
    report_parts = []
    report_parts.append("# Skills 优化报告")
    report_parts.append("")
    report_parts.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_parts.append(f"**模式**: {'试运行' if dry_run else '已应用'}")
    report_parts.append("")
    report_parts.append("---")
    report_parts.append("")
    
    report_parts.append("## 优化计划")
    report_parts.append("")
    report_parts.append(f"共 {len(plan)} 个 skills 需要优化")
    report_parts.append("")
    
    for skill_name, plan_data in plan.items():
        skill_info = plan_data['skill_info']
        actions = plan_data['actions']
        
        report_parts.append(f"### {skill_name}")
        report_parts.append("")
        report_parts.append(f"**文件路径**: `{skill_info.path}`")
        report_parts.append(f"**分类**: {skill_info.category}")
        report_parts.append("")
        report_parts.append("**优化操作**:")
        report_parts.append("")
        
        for i, action in enumerate(actions, 1):
            auto_apply = "✅ 可自动应用" if action.get('auto_apply') else "⚠️  需手动处理"
            report_parts.append(f"{i}. **{action['description']}** ({auto_apply})")
            
            if 'suggestion' in action:
                report_parts.append(f"   - {action['suggestion']}")
            
            report_parts.append("")
        
        report_parts.append("---")
        report_parts.append("")
    
    # 添加执行建议
    if dry_run:
        report_parts.append("## 执行优化")
        report_parts.append("")
        report_parts.append("要应用这些优化，请运行：")
        report_parts.append("")
        report_parts.append("```bash")
        report_parts.append("# 方式 1: 使用项目根目录的脚本（推荐）")
        report_parts.append("./skill-engine optimize --apply")
        report_parts.append("")
        report_parts.append("# 方式 2: 使用 python -m 方式")
        report_parts.append("python3 -m skill_engine.cli optimize --apply")
        report_parts.append("```")
        report_parts.append("")
    
    report = "\n".join(report_parts)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)
