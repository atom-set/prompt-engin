"""Skills 分析工具模块

提供 skills 的检验、优化、整合、优先级分析功能
"""
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field

from .file_utils import get_skills_dir, list_all_skills, read_skill_content
from .yaml_utils import parse_frontmatter, validate_frontmatter


@dataclass
class SkillInfo:
    """Skill 信息数据类"""
    name: str
    path: Path
    category: str
    metadata: Dict
    content: str
    content_without_frontmatter: str
    line_count: int
    issues: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    priority: Optional[int] = None
    dependencies: Set[str] = field(default_factory=set)


@dataclass
class AnalysisResult:
    """分析结果数据类"""
    skills: List[SkillInfo]
    duplicates: List[Tuple[str, str, float]]  # (skill1, skill2, similarity)
    missing_sections: Dict[str, List[str]]  # skill_name -> missing sections
    quality_issues: Dict[str, List[str]]  # skill_name -> issues
    optimization_suggestions: Dict[str, List[str]]  # skill_name -> suggestions
    priority_analysis: Dict[str, Dict]  # skill_name -> priority info
    integration_opportunities: List[Dict]  # integration suggestions


class SkillsAnalyzer:
    """Skills 分析器"""
    
    def __init__(self, skills_dir: Optional[Path] = None):
        """初始化分析器"""
        self.skills_dir = skills_dir or get_skills_dir()
        self.skills: Dict[str, SkillInfo] = {}
        self.result: Optional[AnalysisResult] = None
    
    def load_all_skills(self) -> Dict[str, SkillInfo]:
        """加载所有 skills"""
        skills_list = list_all_skills()
        self.skills = {}
        
        for skill_name, skill_path in skills_list:
            try:
                content = read_skill_content(skill_path)
                metadata, content_without_frontmatter = parse_frontmatter(content)
                
                # 确定分类
                category = self._extract_category(skill_path)
                
                skill_info = SkillInfo(
                    name=skill_name,
                    path=skill_path,
                    category=category,
                    metadata=metadata or {},
                    content=content,
                    content_without_frontmatter=content_without_frontmatter,
                    line_count=len(content.splitlines())
                )
                
                self.skills[skill_name] = skill_info
            except Exception as e:
                print(f"⚠️  警告: 加载 skill {skill_name} 时出错: {e}")
        
        return self.skills
    
    def _extract_category(self, path: Path) -> str:
        """从路径提取分类"""
        parts = path.parts
        if 'skills' in parts:
            idx = parts.index('skills')
            if idx + 1 < len(parts):
                return parts[idx + 1]
        return 'unknown'
    
    def validate_all(self) -> AnalysisResult:
        """检验所有 skills"""
        if not self.skills:
            self.load_all_skills()
        
        missing_sections = {}
        quality_issues = {}
        
        required_sections = [
            "## 使用场景",
            "## 触发条件",
            "## 与其他规则的配合"
        ]
        
        for skill_name, skill_info in self.skills.items():
            issues = []
            missing = []
            
            # 检查 frontmatter
            is_valid, errors = validate_frontmatter(skill_info.metadata)
            if not is_valid:
                issues.extend([f"Frontmatter 错误: {e}" for e in errors])
            
            # 检查必需章节
            for section in required_sections:
                if section not in skill_info.content:
                    missing.append(section)
            
            # 检查内容质量
            content_issues = self._check_content_quality(skill_info)
            issues.extend(content_issues)
            
            if missing:
                missing_sections[skill_name] = missing
            if issues:
                quality_issues[skill_name] = issues
                skill_info.issues = issues
        
        # 检测重复内容
        duplicates = self._detect_duplicates()
        
        # 优先级分析
        priority_analysis = self._analyze_priorities()
        
        # 整合机会
        integration_opportunities = self._find_integration_opportunities()
        
        self.result = AnalysisResult(
            skills=list(self.skills.values()),
            duplicates=duplicates,
            missing_sections=missing_sections,
            quality_issues=quality_issues,
            optimization_suggestions={},
            priority_analysis=priority_analysis,
            integration_opportunities=integration_opportunities
        )
        
        return self.result
    
    def _check_content_quality(self, skill_info: SkillInfo) -> List[str]:
        """检查内容质量"""
        issues = []
        content = skill_info.content_without_frontmatter
        
        # 检查内容长度
        if len(content.strip()) < 100:
            issues.append("内容过短，建议补充详细说明")
        
        # 检查是否有示例
        if "示例" not in content and "example" not in content.lower():
            issues.append("缺少示例，建议添加使用示例")
        
        # 检查描述长度
        description = skill_info.metadata.get('description', '')
        if len(description) < 20:
            issues.append("描述过短，建议提供更详细的描述")
        elif len(description) > 200:
            issues.append("描述过长，建议精简到 200 字以内")
        
        # 检查标签数量
        tags = skill_info.metadata.get('tags', [])
        if len(tags) < 2:
            issues.append("标签数量过少，建议添加更多相关标签")
        elif len(tags) > 8:
            issues.append("标签数量过多，建议精简到 8 个以内")
        
        # 检查是否有代码块
        if "```" not in content:
            issues.append("缺少代码示例，建议添加代码示例")
        
        return issues
    
    def _detect_duplicates(self) -> List[Tuple[str, str, float]]:
        """检测重复内容"""
        duplicates = []
        skill_names = list(self.skills.keys())
        
        for i, name1 in enumerate(skill_names):
            for name2 in skill_names[i+1:]:
                similarity = self._calculate_similarity(
                    self.skills[name1].content_without_frontmatter,
                    self.skills[name2].content_without_frontmatter
                )
                
                if similarity > 0.7:  # 70% 相似度阈值
                    duplicates.append((name1, name2, similarity))
        
        return sorted(duplicates, key=lambda x: x[2], reverse=True)
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """计算文本相似度（简单实现）"""
        # 使用简单的词汇重叠度
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1 & words2
        union = words1 | words2
        
        return len(intersection) / len(union) if union else 0.0
    
    def _analyze_priorities(self) -> Dict[str, Dict]:
        """分析优先级"""
        priority_analysis = {}
        
        # 优先级规则
        priority_rules = {
            'core': 1,
            'mode': 2,
            'code': 3,
            'documentation': 4,
            'workflow': 4,
            'interaction': 4,
            'project': 4,
        }
        
        for skill_name, skill_info in self.skills.items():
            category = skill_info.category
            tags = skill_info.metadata.get('tags', [])
            
            # 优先从 frontmatter 读取 priority 字段
            priority_from_frontmatter = None
            if 'priority' in skill_info.metadata:
                try:
                    priority_from_frontmatter = int(skill_info.metadata['priority'])
                    if 1 <= priority_from_frontmatter <= 4:
                        # 直接使用 frontmatter 中的 priority
                        final_priority = priority_from_frontmatter
                        skill_info.priority = final_priority
                        priority_analysis[skill_name] = {
                            'priority': final_priority,
                            'category': category,
                            'source': 'frontmatter',
                            'tags': tags,
                            'description': skill_info.metadata.get('description', '')[:100] + '...' if len(skill_info.metadata.get('description', '')) > 100 else skill_info.metadata.get('description', '')
                        }
                        continue
                except (ValueError, TypeError):
                    pass  # 如果解析失败，继续使用推断逻辑
            
            # 如果没有 frontmatter priority，使用推断逻辑
            # 从分类确定基础优先级
            base_priority = priority_rules.get(category, 5)
            
            # 从标签中提取优先级信息
            priority_from_tags = None
            for tag in tags:
                if 'priority' in tag.lower() or tag in ['core', 'mode']:
                    if tag == 'core':
                        priority_from_tags = 1
                    elif tag == 'mode':
                        priority_from_tags = 2
                    break
            
            # 从描述中提取优先级信息
            description = skill_info.metadata.get('description', '')
            priority_from_desc = None
            if '优先级：1' in description or '最高' in description:
                priority_from_desc = 1
            elif '优先级：2' in description:
                priority_from_desc = 2
            elif '优先级：3' in description:
                priority_from_desc = 3
            elif '优先级：4' in description:
                priority_from_desc = 4
            
            # 确定最终优先级
            final_priority = priority_from_desc or priority_from_tags or base_priority
            
            skill_info.priority = final_priority
            
            priority_analysis[skill_name] = {
                'priority': final_priority,
                'category': category,
                'base_priority': base_priority,
                'source': 'inferred',
                'tags': tags,
                'description': description[:100] + '...' if len(description) > 100 else description
            }
        
        return priority_analysis
    
    def _find_integration_opportunities(self) -> List[Dict]:
        """查找整合机会"""
        opportunities = []
        
        # 查找相似的 skills
        duplicates = self._detect_duplicates()
        for skill1, skill2, similarity in duplicates:
            if similarity > 0.8:
                opportunities.append({
                    'type': 'merge',
                    'skills': [skill1, skill2],
                    'similarity': similarity,
                    'suggestion': f"考虑合并 {skill1} 和 {skill2}（相似度 {similarity:.1%}）"
                })
        
        # 查找相关 skills（通过标签）
        tag_groups = defaultdict(list)
        for skill_name, skill_info in self.skills.items():
            tags = skill_info.metadata.get('tags', [])
            for tag in tags:
                tag_groups[tag].append(skill_name)
        
        for tag, skills in tag_groups.items():
            if len(skills) > 3:
                opportunities.append({
                    'type': 'group',
                    'tag': tag,
                    'skills': skills,
                    'suggestion': f"标签 '{tag}' 下有 {len(skills)} 个 skills，考虑创建子分类"
                })
        
        return opportunities
    
    def optimize_suggestions(self) -> Dict[str, List[str]]:
        """生成优化建议"""
        if not self.result:
            self.validate_all()
        
        suggestions = {}
        
        for skill_name, skill_info in self.skills.items():
            skill_suggestions = []
            
            # 基于问题生成建议
            if skill_info.issues:
                for issue in skill_info.issues:
                    if "内容过短" in issue:
                        skill_suggestions.append("补充详细的使用场景和示例")
                    elif "缺少示例" in issue:
                        skill_suggestions.append("添加代码示例或使用场景示例")
                    elif "描述过短" in issue:
                        skill_suggestions.append("扩展描述，说明 skill 的具体用途")
                    elif "标签数量" in issue:
                        skill_suggestions.append("优化标签，确保标签准确反映 skill 的功能")
            
            # 检查依赖关系
            dependencies = self._extract_dependencies(skill_info)
            if dependencies:
                skill_info.dependencies = dependencies
                # 依赖关系已存在，不需要建议明确
            # 注意：如果依赖关系为空，可能是正常的（某些 skill 没有依赖），
            # 所以不自动建议添加依赖关系，除非有明确的上下文表明需要依赖
            
            # 检查优先级一致性（更智能的规则）
            category = skill_info.category
            priority = skill_info.priority
            tags = skill_info.metadata.get('tags', [])
            
            # core 分类的 skills 可以有不同优先级，根据内容和标签判断
            if category == 'core':
                # Priority 1: 核心基础规则（mode, security, permission 相关）
                if priority != 1 and any(tag in ['mode', 'security', 'permission'] for tag in tags):
                    if 'mode-common' in skill_name or 'security' in skill_name or 'permission' in skill_name:
                        skill_suggestions.append("核心基础规则（mode/security/permission）建议设置为优先级 1")
                
                # Priority 2: 模式规则（act-mode, plan-mode, file-write, solution-output）
                # 这些已经有正确的优先级，不需要建议
                
                # Priority 3: 代码标准（code-format, naming, comments 等）
                # 这些已经有正确的优先级，不需要建议
                
                # 如果 core 分类的 skill 没有设置优先级，建议设置
                if priority is None:
                    if any(tag in ['mode', 'security', 'permission'] for tag in tags):
                        skill_suggestions.append("建议设置优先级为 1（核心基础规则）")
                    elif any(tag in ['code', 'format', 'naming', 'function', 'comments', 'error'] for tag in tags):
                        skill_suggestions.append("建议设置优先级为 3（代码标准）")
                    else:
                        skill_suggestions.append("建议根据 skill 类型设置合适的优先级（1-3）")
            
            if skill_suggestions:
                suggestions[skill_name] = skill_suggestions
                skill_info.suggestions = skill_suggestions
        
        self.result.optimization_suggestions = suggestions
        return suggestions
    
    def _extract_dependencies(self, skill_info: SkillInfo) -> Set[str]:
        """提取依赖关系"""
        dependencies = set()
        content = skill_info.content
        
        # 从"与其他规则的配合"章节提取
        if "## 与其他规则的配合" in content:
            section_start = content.find("## 与其他规则的配合")
            section_end = content.find("##", section_start + 1)
            if section_end == -1:
                section_end = len(content)
            
            section_content = content[section_start:section_end]
            
            # 查找 skill 名称（使用反引号，格式为 skill-name）
            # 排除常见的工具名称和命令
            excluded_words = {
                'ls', 'df', 'rmdir', 'uname', 'printenv', 'du', 'hostname', 
                'mkdir', 'whoami', 'test', 'ln', 'setenv', 'ps', 'date', 
                'file', 'tail', 'wc', 'cp', 'head', 'chown', 'type', 'env', 
                'echo', 'terminal', 'top', 'unlink', 'chmod', 'make', 'cat', 
                'rm', 'mv', 'touch', 'export', 'stat', 'which', 'grep', 'pwd', 
                'find', 'cd', 'git', 'python', 'bash', 'sh', 'curl', 'wget'
            }
            
            # 查找 skill 名称（格式：`skill-name` 或 skill-name）
            # skill 名称通常包含连字符，长度在 3-30 字符之间
            matches = re.findall(r'`([a-z][a-z0-9-]{2,29})`', section_content)
            for match in matches:
                dep = match.strip()
                # 排除工具名称和当前 skill
                if dep not in excluded_words and dep != skill_info.name:
                    # 验证是否是有效的 skill 名称（包含连字符或符合命名规范）
                    if '-' in dep or len(dep) >= 5:
                        # 检查是否在已知的 skills 列表中
                        if any(dep in skill_name or skill_name.endswith(dep) 
                               for skill_name in self.skills.keys()):
                            dependencies.add(dep)
        
        return dependencies
    
    def generate_priority_report(self) -> str:
        """生成优先级报告"""
        if not self.result:
            self.validate_all()
        
        priority_groups = defaultdict(list)
        for skill_name, skill_info in self.skills.items():
            priority = skill_info.priority or 5
            priority_groups[priority].append((skill_name, skill_info))
        
        report = []
        report.append("=" * 60)
        report.append("Skills 优先级分析报告")
        report.append("=" * 60)
        report.append("")
        
        for priority in sorted(priority_groups.keys()):
            skills = priority_groups[priority]
            report.append(f"优先级 {priority} ({len(skills)} 个 skills):")
            report.append("-" * 60)
            
            for skill_name, skill_info in sorted(skills, key=lambda x: x[0]):
                category = skill_info.category
                description = skill_info.metadata.get('description', '')[:60]
                report.append(f"  - {skill_name} ({category})")
                report.append(f"    {description}...")
            
            report.append("")
        
        return "\n".join(report)
    
    def generate_integration_report(self) -> str:
        """生成整合报告"""
        if not self.result:
            self.validate_all()
        
        report = []
        report.append("=" * 60)
        report.append("Skills 整合建议报告")
        report.append("=" * 60)
        report.append("")
        
        if not self.result.integration_opportunities:
            report.append("✅ 未发现明显的整合机会")
            return "\n".join(report)
        
        # 合并建议
        merge_ops = [op for op in self.result.integration_opportunities if op['type'] == 'merge']
        if merge_ops:
            report.append("🔄 合并建议:")
            report.append("-" * 60)
            for op in merge_ops:
                skills = op['skills']
                similarity = op['similarity']
                report.append(f"  - {skills[0]} ↔ {skills[1]} (相似度: {similarity:.1%})")
                report.append(f"    建议: {op['suggestion']}")
            report.append("")
        
        # 分组建议
        group_ops = [op for op in self.result.integration_opportunities if op['type'] == 'group']
        if group_ops:
            report.append("📁 分组建议:")
            report.append("-" * 60)
            for op in group_ops:
                report.append(f"  - 标签 '{op['tag']}': {len(op['skills'])} 个 skills")
                report.append(f"    {', '.join(op['skills'][:5])}{'...' if len(op['skills']) > 5 else ''}")
            report.append("")
        
        return "\n".join(report)
