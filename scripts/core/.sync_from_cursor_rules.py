#!/usr/bin/env python3
"""
从 cursor-rules 同步提示词到当前工程

这是一个隐藏工具，仅用于内部使用。
"""

import os
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Tuple, Optional


# 颜色定义
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


# 配置
SOURCE_DIR = Path("/Users/gengxiao/workspace/D-codeup/cursor-rules/rules")
TARGET_DIR = Path(__file__).parent.parent.parent / "prompts"

# 目录映射关系
DIRECTORY_MAPPING = {
    "stages": "stages",
    "project-types": "types",
    "templates": "templates",
}


def get_file_mtime(file_path: Path) -> Optional[float]:
    """获取文件修改时间戳"""
    try:
        return file_path.stat().st_mtime
    except Exception:
        return None


def should_sync_file(source_path: Path, target_path: Path) -> Tuple[bool, str]:
    """
    判断是否需要同步文件
    
    Returns:
        (是否需要同步, 原因)
    """
    if not source_path.exists():
        return False, "源文件不存在"
    
    if not target_path.exists():
        return True, "目标文件不存在"
    
    source_mtime = get_file_mtime(source_path)
    target_mtime = get_file_mtime(target_path)
    
    if source_mtime is None:
        return False, "无法获取源文件时间"
    
    if target_mtime is None:
        return True, "无法获取目标文件时间"
    
    if source_mtime > target_mtime:
        return True, "源文件更新"
    
    return False, "目标文件已是最新"


def sync_file(source_path: Path, target_path: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """
    同步单个文件
    
    Returns:
        (是否成功, 消息)
    """
    should_sync, reason = should_sync_file(source_path, target_path)
    
    if not should_sync:
        return True, f"跳过: {reason}"
    
    if dry_run:
        return True, f"[预览] 将同步: {source_path.name} ({reason})"
    
    try:
        # 确保目标目录存在
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 如果目标文件存在，先备份
        if target_path.exists():
            backup_path = target_path.with_suffix(f"{target_path.suffix}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            shutil.copy2(target_path, backup_path)
        
        # 复制文件
        shutil.copy2(source_path, target_path)
        
        return True, f"✓ 已同步: {target_path.relative_to(target_path.parent.parent.parent)}"
    except Exception as e:
        return False, f"✗ 同步失败: {e}"


def sync_directory(
    source_dir: Path,
    target_dir: Path,
    dry_run: bool = False,
    verbose: bool = True
) -> Tuple[int, int]:
    """
    同步整个目录
    
    Returns:
        (成功数量, 失败数量)
    """
    success_count = 0
    fail_count = 0
    
    if not source_dir.exists():
        if verbose:
            print(f"{Colors.YELLOW}警告: 源目录不存在: {source_dir}{Colors.NC}")
        return success_count, fail_count
    
    # 查找所有 .md 文件
    for source_file in source_dir.rglob("*.md"):
        # 跳过 README.md（可选）
        if source_file.name == "README.md":
            continue
        
        # 计算相对路径
        relative_path = source_file.relative_to(source_dir)
        
        # 计算目标路径
        target_file = target_dir / relative_path
        
        # 同步文件
        success, message = sync_file(source_file, target_file, dry_run)
        
        if success:
            success_count += 1
            if verbose and ("已同步" in message or "[预览]" in message):
                print(f"  {message}")
        else:
            fail_count += 1
            if verbose:
                print(f"  {Colors.RED}{message}{Colors.NC}")
    
    return success_count, fail_count


def sync_all(source_dir: Path, target_dir: Path, dry_run: bool = False, verbose: bool = True) -> bool:
    """同步所有目录"""
    if not source_dir.exists():
        print(f"{Colors.RED}错误: 源目录不存在: {source_dir}{Colors.NC}")
        return False
    
    print(f"{Colors.BLUE}开始同步提示词...{Colors.NC}")
    print(f"{Colors.BLUE}源目录: {source_dir}{Colors.NC}")
    print(f"{Colors.BLUE}目标目录: {target_dir}{Colors.NC}")
    if dry_run:
        print(f"{Colors.YELLOW}模式: 预览模式（不会实际修改文件）{Colors.NC}")
    print()
    
    total_success = 0
    total_fail = 0
    
    # 同步各个目录
    for source_subdir, target_subdir in DIRECTORY_MAPPING.items():
        source_path = source_dir / source_subdir
        target_path = target_dir / target_subdir
        
        if verbose:
            print(f"{Colors.BLUE}同步目录: {source_subdir} -> {target_subdir}{Colors.NC}")
        
        success, fail = sync_directory(source_path, target_path, dry_run, verbose)
        total_success += success
        total_fail += fail
        
        if verbose:
            if success > 0:
                print(f"  {Colors.GREEN}成功: {success}{Colors.NC}")
            if fail > 0:
                print(f"  {Colors.RED}失败: {fail}{Colors.NC}")
            print()
    
    # 显示统计
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print(f"{Colors.BLUE}同步完成{Colors.NC}")
    print(f"{Colors.BLUE}========================================{Colors.NC}")
    print()
    print(f"{Colors.GREEN}成功: {total_success}{Colors.NC}")
    if total_fail > 0:
        print(f"{Colors.RED}失败: {total_fail}{Colors.NC}")
    print()
    
    return total_fail == 0


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="从 cursor-rules 同步提示词到当前工程",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 预览模式（不实际修改文件）
  python .sync_from_cursor_rules.py --dry-run
  
  # 实际同步
  python .sync_from_cursor_rules.py
  
  # 静默模式
  python .sync_from_cursor_rules.py --quiet
        """
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="预览模式，不实际修改文件"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，只显示错误"
    )
    
    parser.add_argument(
        "--source",
        type=str,
        default=str(SOURCE_DIR),
        help=f"源目录路径（默认: {SOURCE_DIR}）"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        default=str(TARGET_DIR),
        help=f"目标目录路径（默认: {TARGET_DIR}）"
    )
    
    args = parser.parse_args()
    
    # 解析路径
    source_dir = Path(args.source)
    target_dir = Path(args.target)
    
    # 执行同步
    success = sync_all(source_dir, target_dir, dry_run=args.dry_run, verbose=not args.quiet)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

