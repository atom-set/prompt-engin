"""Generate AGENTS.md command"""

from pathlib import Path
from collections import defaultdict
from typing import Tuple

from ..utils import (
    get_skills_dir,
    list_all_skills,
    read_skill_content,
    parse_frontmatter
)


def get_priority_description(priority: int) -> str:
    """获取优先级描述"""
    descriptions = {
        1: "（最高，必须首先应用）",
        2: "（按模式条件应用）",
        3: "（编写代码时自动应用）",
        4: "（按需加载，用于"
    }
    return descriptions.get(priority, "")


def get_priority_category_name(priority: int) -> Tuple[str, str]:
    """获取优先级分类名称（中文和英文）"""
    categories = {
        1: ("Core Skills (顶层核心规则，默认自动应用，优先级最高)", "Core skills (Priority 1)"),
        2: ("Mode Skills (模式规则，按模式条件应用)", "Mode skills (Priority 2)"),
        3: ("Code Standards (代码标准，编写代码时自动应用)", "Code standards (Priority 3)"),
        4: ("Domain Skills (领域技能，按需加载)", "Domain skills (Priority 4)")
    }
    return categories.get(priority, ("", ""))


def get_priority_usage_description(priority: int) -> str:
    """获取优先级的使用说明"""
    descriptions = {
        1: "Automatically applied first. These are the foundation rules that must be applied first:",
        2: "Applied conditionally based on current mode:",
        3: "Automatically applied when writing code:",
        4: "Load on-demand based on task type:"
    }
    return descriptions.get(priority, "")


def generate_agents_md(output_path: Path = None) -> str:
    """生成 AGENTS.md 内容"""
    skills_dir = get_skills_dir()
    
    if not skills_dir.exists():
        raise FileNotFoundError(f"Skills 目录不存在: {skills_dir}")
    
    # 加载所有 skills
    skills_list = list_all_skills()
    skills_by_priority = defaultdict(list)
    
    for skill_name, skill_path in skills_list:
        try:
            content = read_skill_content(skill_path)
            metadata, _ = parse_frontmatter(content)
            
            if not metadata:
                continue
            
            # 获取优先级
            priority = metadata.get('priority')
            if priority is None:
                # 如果没有 priority，根据分类推断
                category = skill_path.parent.name
                if category == 'core':
                    # 进一步判断
                    tags = metadata.get('tags', [])
                    if 'mode' in tags and 'permission' in tags or 'security' in tags:
                        priority = 1
                    elif 'mode' in tags:
                        priority = 2
                    else:
                        priority = 3
                else:
                    priority = 4
            else:
                priority = int(priority)
            
            # 确定 location（分类）
            location = skill_path.parent.name
            
            skills_by_priority[priority].append({
                'name': metadata.get('name', skill_name),
                'description': metadata.get('description', ''),
                'location': location,
                'priority': priority
            })
        except Exception as e:
            print(f"⚠️  警告: 处理 skill {skill_name} 时出错: {e}")
            continue
    
    # 生成 AGENTS.md 内容
    lines = []
    lines.append('')
    lines.append('<skills_system priority="1">')
    lines.append('')
    lines.append('## Available Skills')
    lines.append('')
    lines.append('<!-- SKILLS_TABLE_START -->')
    lines.append('<usage>')
    lines.append('When users ask you to perform tasks, check if any of the available skills below can help complete the task more effectively. Skills provide specialized capabilities and domain knowledge.')
    lines.append('')
    lines.append('How to use skills:')
    lines.append('- Invoke: Bash("openskills read <skill-name>")')
    lines.append('- The skill content will load with detailed instructions on how to complete the task')
    lines.append('- Base directory provided in output for resolving bundled resources (references/, scripts/, assets/)')
    lines.append('')
    lines.append('Usage notes:')
    lines.append('- Only use skills listed in <available_skills> below')
    lines.append('- Do not invoke a skill that is already loaded in your context')
    lines.append('- Each skill invocation is stateless')
    lines.append('')
    lines.append('Priority and application order:')
    
    # 添加优先级说明
    for priority in sorted(skills_by_priority.keys()):
        skills = skills_by_priority[priority]
        category_name_en = get_priority_category_name(priority)[1]
        usage_desc = get_priority_usage_description(priority)
        
        lines.append(f'{priority}. **{category_name_en}** - {usage_desc}')
        
        if priority == 1:
            # Priority 1 列出具体技能
            for skill in skills[:3]:  # 只列出前3个
                # 根据技能名称添加说明
                if 'tool-permission' in skill['name']:
                    lines.append(f'   - {skill["name"]} (applied before every tool call)')
                elif 'mode-common' in skill['name']:
                    lines.append(f'   - {skill["name"]} (applied when generating responses)')
                elif 'security' in skill['name']:
                    lines.append(f'   - {skill["name"]} (applied before tool calls)')
                else:
                    lines.append(f'   - {skill["name"]}')
        elif priority == 2:
            # Priority 2 列出具体技能
            for skill in skills:
                lines.append(f'   - {skill["name"]} (when in {skill["name"].replace("-mode", "").title()} mode)')
        elif priority == 3:
            # Priority 3 列出技能名称
            skill_names = [s["name"] for s in skills]
            lines.append(f'   - {", ".join(skill_names)}')
        elif priority == 4:
            # Priority 4 说明按需加载
            lines.append('   - Check task requirements and load relevant domain skills')
            lines.append('   - Code tasks → code-organization, design-principles, problem-location')
            lines.append('   - Documentation tasks → document-format, document-generation, wiki-output')
            lines.append('   - Workflow tasks → phase-implementation, compatibility-check, etc.')
        
        lines.append('')
    
    lines.append('Application rules:')
    lines.append('- Always apply core skills first (from skills/core/ directory)')
    lines.append('- Apply mode skills based on current context')
    lines.append('- Apply code standards when writing code')
    lines.append('- Load domain skills only when needed for specific tasks')
    lines.append('</usage>')
    lines.append('')
    lines.append('<available_skills>')
    lines.append('')
    
    # 按优先级分组输出 skills
    for priority in sorted(skills_by_priority.keys()):
        skills = sorted(skills_by_priority[priority], key=lambda x: x['name'])
        category_name_zh, category_name_en = get_priority_category_name(priority)
        
        lines.append(f'<!-- ============================================================================')
        lines.append(f'     {category_name_zh}')
        lines.append(f'     ============================================================================ -->')
        lines.append('')
        
        for skill in skills:
            # 使用原始描述，如果已经包含优先级信息则不再添加
            description = skill['description']
            
            # 如果描述中还没有优先级信息，则添加
            if f'优先级：{skill["priority"]}' not in description:
                # 清理描述末尾的句号
                description = description.rstrip('。')
                priority_desc = get_priority_description(skill['priority'])
                if skill['priority'] == 4:
                    # Priority 4 需要根据 location 添加用途说明
                    location = skill['location']
                    usage_map = {
                        'code': '代码开发',
                        'documentation': '文档生成',
                        'workflow': '工作流程',
                        'interaction': '用户交互',
                        'project': '项目管理'
                    }
                    usage = usage_map.get(location, '特定场景')
                    description += f'。优先级：{skill["priority"]}{priority_desc}{usage}）'
                else:
                    description += f'。优先级：{skill["priority"]}{priority_desc}'
            
            lines.append('<skill>')
            lines.append(f'<name>{skill["name"]}</name>')
            lines.append(f'<description>{description}</description>')
            lines.append(f'<location>{skill["location"]}</location>')
            lines.append('</skill>')
            lines.append('')
    
    lines.append('</available_skills>')
    lines.append('<!-- SKILLS_TABLE_END -->')
    lines.append('')
    lines.append('</skills_system>')
    
    content = '\n'.join(lines)
    
    # 如果指定了输出路径，写入文件
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding='utf-8')
        print(f"✅ AGENTS.md 已生成: {output_path}")
    
    return content


def generate_agents(output_path: str = None):
    """生成 AGENTS.md 文件"""
    if output_path is None:
        output_path = Path.cwd() / 'AGENTS.md'
    else:
        output_path = Path(output_path)
    
    try:
        content = generate_agents_md(output_path)
        skill_count = len([l for l in content.split('\n') if '<skill>' in l])
        print(f"✅ 成功生成 AGENTS.md")
        print(f"   位置: {output_path.absolute()}")
        print(f"   包含 {skill_count} 个 skills")
    except Exception as e:
        print(f"❌ 生成失败: {e}")
        import traceback
        traceback.print_exc()
        raise
