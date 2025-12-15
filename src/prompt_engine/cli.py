"""
命令行接口模块。

提供 CLI 工具入口。
"""

import sys
from pathlib import Path

import click

from .merger import PromptMerger
from .validator import PromptValidator
from .generator import PromptGenerator
from .parser import PromptParser


@click.group()
@click.option(
    "--base-path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=None,
    help="提示词基础路径",
)
@click.pass_context
def cli(ctx, base_path):
    """Prompt Engine - 提示词结构化工具"""
    ctx.ensure_object(dict)
    if base_path:
        ctx.obj["base_path"] = base_path
    else:
        # 默认使用项目根目录
        ctx.obj["base_path"] = str(Path(__file__).parent.parent.parent)


@cli.command()
@click.option("--output", "-o", default="merged.md", help="输出文件路径")
@click.option("--stage", help="按阶段合并（如 common, development）")
@click.option("--type", help="按类型合并（如 frontend, backend）")
@click.option("--all", "-a", is_flag=True, help="合并所有提示词（所有阶段和类型）")
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def merge(ctx, output, stage, type, all, files):
    """合并提示词文件"""
    base_path = ctx.obj["base_path"]
    merger = PromptMerger(base_path)

    try:
        if all:
            # 合并所有提示词：先合并所有阶段，再合并所有类型
            import tempfile
            import os
            
            # 创建临时文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as tmp:
                temp_file = tmp.name
            
            try:
                # 先合并所有阶段
                stages = ["common", "requirements", "design", "development", "testing", "documentation"]
                all_files = []
                
                for stage_name in stages:
                    stage_dir = Path(base_path) / "prompts" / "stages" / stage_name
                    if stage_dir.exists():
                        for md_file in stage_dir.rglob("*.md"):
                            if md_file.name != "README.md":
                                all_files.append(str(md_file.relative_to(Path(base_path))))
                
                # 再合并所有类型
                types = ["frontend", "backend", "fullstack", "mobile"]
                for type_name in types:
                    type_dir = Path(base_path) / "prompts" / "types" / type_name
                    if type_dir.exists():
                        for md_file in type_dir.rglob("*.md"):
                            if md_file.name != "README.md":
                                all_files.append(str(md_file.relative_to(Path(base_path))))
                
                if all_files:
                    output_file = merger.merge(all_files, output)
                    click.echo(f"✓ 已合并 {len(all_files)} 个提示词文件到: {output_file}")
                else:
                    click.echo("警告: 未找到任何提示词文件", err=True)
                    sys.exit(1)
            finally:
                # 清理临时文件
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
        elif stage:
            output_file = merger.merge_by_stage(stage, output)
            click.echo(f"✓ 已合并阶段 '{stage}' 的提示词到: {output_file}")
        elif type:
            output_file = merger.merge_by_type(type, output)
            click.echo(f"✓ 已合并类型 '{type}' 的提示词到: {output_file}")
        elif files:
            output_file = merger.merge(list(files), output)
            click.echo(f"✓ 已合并 {len(files)} 个文件到: {output_file}")
        else:
            click.echo("错误: 请指定要合并的内容", err=True)
            click.echo("", err=True)
            click.echo("可用选项:", err=True)
            click.echo("  --all, -a          合并所有提示词", err=True)
            click.echo("  --stage STAGE      按阶段合并（如: common, development）", err=True)
            click.echo("  --type TYPE        按类型合并（如: frontend, backend）", err=True)
            click.echo("  FILES...           指定要合并的文件列表", err=True)
            click.echo("", err=True)
            click.echo("示例:", err=True)
            click.echo("  prompt-engine merge --all --output combined.md", err=True)
            click.echo("  prompt-engine merge --stage common --output common.md", err=True)
            click.echo("  prompt-engine merge file1.md file2.md --output merged.md", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--recursive", "-r", is_flag=True, help="递归验证子目录")
@click.pass_context
def validate(ctx, path, recursive):
    """验证提示词文件格式"""
    base_path = ctx.obj["base_path"]
    validator = PromptValidator(base_path)

    path_obj = Path(path)
    if path_obj.is_file():
        is_valid, errors = validator.validate_file(path)
        if is_valid:
            click.echo(f"✓ {path} 验证通过")
        else:
            click.echo(f"✗ {path} 验证失败:", err=True)
            for error in errors:
                click.echo(f"  - {error}", err=True)
            sys.exit(1)
    elif path_obj.is_dir():
        results = validator.validate_directory(path, recursive)
        valid_count = sum(1 for is_valid, _ in results.values() if is_valid)
        total_count = len(results)

        click.echo(f"验证完成: {valid_count}/{total_count} 个文件通过验证")

        if valid_count < total_count:
            for file_path, (is_valid, errors) in results.items():
                if not is_valid:
                    click.echo(f"\n✗ {file_path}:", err=True)
                    for error in errors:
                        click.echo(f"  - {error}", err=True)
            sys.exit(1)
    else:
        click.echo(f"错误: 路径不存在: {path}", err=True)
        sys.exit(1)


@cli.command()
@click.option("--template", "-t", help="模板文件路径")
@click.option("--output", "-o", required=True, help="输出文件路径")
@click.option("--var", multiple=True, help="模板变量（格式: key=value）")
@click.pass_context
def generate(ctx, template, output, var):
    """根据模板生成提示词"""
    base_path = ctx.obj["base_path"]
    generator = PromptGenerator(base_path)

    # 解析变量
    variables = {}
    for v in var:
        if "=" in v:
            key, value = v.split("=", 1)
            variables[key] = value

    try:
        if template:
            output_file = generator.generate_from_template(template, output, variables)
            click.echo(f"✓ 已生成提示词到: {output_file}")
        else:
            click.echo("错误: 请指定模板文件", err=True)
            sys.exit(1)
    except Exception as e:
        click.echo(f"错误: {e}", err=True)
        sys.exit(1)


@cli.command()
@click.pass_context
def list(ctx):
    """列出可用的提示词模板"""
    base_path = ctx.obj["base_path"]
    parser = PromptParser(base_path)

    # 列出阶段提示词
    stages_dir = Path(base_path) / "prompts" / "stages"
    if stages_dir.exists():
        click.echo("阶段提示词:")
        for stage_dir in sorted(stages_dir.iterdir()):
            if stage_dir.is_dir():
                prompts = parser.parse_directory(f"prompts/stages/{stage_dir.name}")
                click.echo(f"  {stage_dir.name}: {len(prompts)} 个提示词")

    # 列出类型提示词
    types_dir = Path(base_path) / "prompts" / "types"
    if types_dir.exists():
        click.echo("\n类型提示词:")
        for type_dir in sorted(types_dir.iterdir()):
            if type_dir.is_dir():
                prompts = parser.parse_directory(f"prompts/types/{type_dir.name}")
                click.echo(f"  {type_dir.name}: {len(prompts)} 个提示词")


def main():
    """CLI 入口函数"""
    cli()


if __name__ == "__main__":
    main()

