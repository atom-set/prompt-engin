import logging
import shutil
import subprocess
from pathlib import Path


class SyncSkill:
    def __init__(self, project_path, skills, dry_run=False, reset=False, logger=None):
        self.project_path = Path(project_path)
        self.skills = skills or []
        self.dry_run = dry_run
        self.reset_flag = reset
        self.logger = logger or logging.getLogger(__name__)
        self.agents_path = self.project_path / "AGENTS.md"
        self.backup_path = self.agents_path.with_suffix(self.agents_path.suffix + ".bak")

    def run(self):
        if self.reset_flag:
            self.logger.info("Reset requested for project %s", self.project_path)
            self.reset()
            return

        if self.dry_run:
            self.logger.info("Dry run: skills %s would be installed into %s", self.skills, self.project_path)
            return

        self.prepare_directories()
        
        # 1. 安装用户选择的技能
        installed = []
        for skill in self.skills:
            result = self.install_skill(skill)
            if result:
                installed.append(skill)
        
        # 2. 注意：AGENTS.md 的同步由 openskills sync -y 负责
        # 清理操作也在 openskills sync 之后调用
        # 这里只负责安装技能，不执行清理
        
        if installed:
            self.validate(installed)
        else:
            self.logger.warning("No skills were installed for project %s", self.project_path)
    
    def cleanup_only(self):
        """只执行清理操作，不安装技能（用于在 openskills sync 之后清理未选择的技能）"""
        if not self.agents_path.exists():
            self.logger.info("AGENTS.md does not exist, skipping cleanup")
            return
        
        # 清理 AGENTS.md 中未选择的技能（只保留用户选择的技能）
        self.cleanup_unselected_skills_from_agents(self.skills)

    def prepare_directories(self):
        for subdir in [".claude/skills", ".agent/skills"]:
            path = self.project_path / subdir
            if not path.exists():
                self.logger.info("Creating directory %s", path)
                if not self.dry_run:
                    path.mkdir(parents=True, exist_ok=True)

    def install_skill(self, skill_path):
        """
        安装技能
        
        支持以下格式：
        - 本地路径：/path/to/skill 或 ./skill
        - GitHub 仓库：username/repo-name
        - GitHub 技能：username/repo-name/skill-name
        """
        # 判断是本地路径还是 GitHub 仓库
        if Path(skill_path).exists() or skill_path.startswith("./") or skill_path.startswith("../"):
            # 本地路径
            skill_source = Path(skill_path).resolve()
            if not skill_source.exists():
                self.logger.error("Skill path does not exist: %s", skill_path)
                return False
            
            # 提取技能名称（目录名）
            skill_name = skill_source.name
            
            # 安装到项目
            cmd = ["openskills", "install", str(skill_source), "-y"]
            self.logger.info("Installing local skill %s via %s", skill_name, " ".join(cmd))
            try:
                result = subprocess.run(
                    cmd,
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=str(self.project_path)
                )
                self.logger.info("Local skill %s installed successfully", skill_name)
                return True
            except subprocess.CalledProcessError as exc:
                self.logger.error("Failed to install local skill %s: %s", skill_path, exc.stderr or exc.stdout or exc)
                return False
        else:
            # GitHub 仓库或技能
            parts = skill_path.split("/")
            if len(parts) == 3:
                # 格式：owner/repo/skill-name
                repo_name = f"{parts[0]}/{parts[1]}"
                skill_short_name = parts[2]
            elif len(parts) == 2:
                # 格式：owner/repo（整个仓库）
                repo_name = skill_path
                skill_short_name = None
            else:
                # 其他格式，直接尝试安装
                repo_name = skill_path
                skill_short_name = None
            
            # 检查仓库是否已安装
            repo_installed = self.is_repo_installed(repo_name)
            
            if not repo_installed:
                # 安装整个仓库
                cmd = ["openskills", "install", repo_name, "-y"]
                self.logger.info("Installing repository %s via %s", repo_name, " ".join(cmd))
                try:
                    result = subprocess.run(
                        cmd,
                        check=True,
                        capture_output=True,
                        text=True,
                        cwd=str(self.project_path)
                    )
                    self.logger.info("Repository %s installed successfully", repo_name)
                except subprocess.CalledProcessError as exc:
                    self.logger.error("Failed to install repository %s: %s", repo_name, exc.stderr or exc.stdout or exc)
                    return False
            else:
                self.logger.info("Repository %s already installed", repo_name)
            
            # 如果指定了具体技能名称，验证技能是否存在
            if skill_short_name:
                skill_path_found = self.find_skill_path(skill_short_name, repo_name)
                if not skill_path_found:
                    self.logger.warning("Skill %s not found in repository %s, but continuing (openskills sync will handle it)", skill_short_name, repo_name)
                else:
                    self.logger.info("Skill %s found at %s", skill_short_name, skill_path_found)
            
            return True
    
    def is_repo_installed(self, repo_name):
        """检查仓库是否已安装"""
        for base in [".claude/skills", ".agent/skills"]:
            skills_dir = self.project_path / base
            if skills_dir.exists():
                # 检查是否有任何技能目录（包含 SKILL.md 文件）
                for item in skills_dir.iterdir():
                    if item.is_dir() and (item / "SKILL.md").exists():
                        return True
        return False
    
    def find_skill_path(self, skill_short_name, repo_name):
        """查找技能的实际路径"""
        for base in [".claude/skills", ".agent/skills"]:
            skills_dir = self.project_path / base
            if not skills_dir.exists():
                continue
            
            # 可能的路径格式
            possible_paths = [
                skills_dir / skill_short_name,  # 最常见：直接名称
                skills_dir / f"{repo_name.replace('/', '-')}-{skill_short_name}",  # 仓库-技能
            ]
            
            # 检查是否有子目录结构（repo_name/skill_short_name）
            repo_dir = skills_dir / repo_name.replace("/", "-")
            if repo_dir.exists() and repo_dir.is_dir():
                possible_paths.append(repo_dir / skill_short_name)
            
            for path in possible_paths:
                if path.exists() and (path / "SKILL.md").exists():
                    return path
        
        return None
    
    def cleanup_unselected_skills_from_agents(self, selected_skills):
        """从 AGENTS.md 中删除未选择的技能，只保留用户选择的技能"""
        if not self.agents_path.exists():
            self.logger.info("AGENTS.md does not exist, skipping cleanup")
            return
        
        # 提取用户选择的技能简短名称列表
        selected_skill_names = set()
        for skill in selected_skills:
            # 如果是路径，提取目录名
            if Path(skill).exists() or "/" in skill:
                parts = skill.split("/")
                if len(parts) == 3:
                    skill_short_name = parts[2]
                elif len(parts) == 2:
                    skill_short_name = parts[1]
                else:
                    skill_short_name = Path(skill).name if Path(skill).exists() else skill
            else:
                skill_short_name = skill
            selected_skill_names.add(skill_short_name)
        
        # 读取 AGENTS.md 文件内容
        content = self.agents_path.read_text()
        
        # 使用正则表达式提取所有技能块
        import re
        skill_pattern = r'(<skill>.*?</skill>)'
        skill_blocks = re.findall(skill_pattern, content, re.DOTALL)
        
        # 提取每个技能的名称
        kept_blocks = []
        removed_count = 0
        
        for block in skill_blocks:
            name_match = re.search(r'<name>(.*?)</name>', block, re.DOTALL)
            if name_match:
                skill_name = name_match.group(1).strip()
                if skill_name in selected_skill_names:
                    kept_blocks.append(block)
                else:
                    removed_count += 1
            else:
                # 如果无法解析技能名称，保留该块（避免误删）
                kept_blocks.append(block)
        
        # 检查是否有旧格式的技能条目（- name: skill-name）
        old_format_pattern = r'^- name:\s*(\S+)'
        old_format_matches = re.findall(old_format_pattern, content, re.MULTILINE)
        if old_format_matches:
            content = re.sub(r'^- name:.*$', '', content, flags=re.MULTILINE)
        
        # 重建 AGENTS.md 内容
        available_skills_pattern = r'(<available_skills>)(.*?)(</available_skills>)'
        
        def replace_skills(match):
            start_tag = match.group(1)
            end_tag = match.group(3)
            skills_content = "\n\n".join(kept_blocks)
            return f"{start_tag}\n{skills_content}\n{end_tag}"
        
        new_content = re.sub(available_skills_pattern, replace_skills, content, flags=re.DOTALL)
        
        # 写回 AGENTS.md
        if removed_count > 0 or old_format_matches:
            self.logger.info("Writing back AGENTS.md, removed %d unselected skills", removed_count)
            self.agents_path.write_text(new_content)
        else:
            self.logger.info("No cleanup needed, all skills are in the selection list")
    
    def validate(self, installed_skills):
        missing = []
        for skill in installed_skills:
            # 提取技能简短名称
            if Path(skill).exists() or "/" in skill:
                parts = skill.split("/")
                if len(parts) == 3:
                    skill_short_name = parts[2]
                elif len(parts) == 2:
                    skill_short_name = parts[1]
                else:
                    skill_short_name = Path(skill).name if Path(skill).exists() else skill
            else:
                skill_short_name = skill
            
            found = False
            # 查找技能路径
            for base in [".claude/skills", ".agent/skills"]:
                candidate = self.project_path / base / skill_short_name
                if candidate.exists() and (candidate / "SKILL.md").exists():
                    found = True
                    break
            
            if not found:
                missing.append(skill)
        if missing:
            self.logger.warning("The following skills might be missing files: %s", missing)
        else:
            self.logger.info("All installed skills found on disk")

    def reset(self):
        if self.backup_path.exists():
            shutil.copy2(self.backup_path, self.agents_path)
            self.logger.info("Restored AGENTS.md from backup")
        for skill in self.skills:
            for base in [".claude/skills", ".agent/skills"]:
                path = self.project_path / base / skill
                if path.exists():
                    shutil.rmtree(path, ignore_errors=True)
                    self.logger.info("Removed %s", path)
