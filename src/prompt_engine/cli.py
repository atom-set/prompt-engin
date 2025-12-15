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
@click.option(
    "--ide",
    type=click.Choice(["cursor", "trae", "antigravity", "both", "all"], case_sensitive=False),
    help="指定 IDE 格式：cursor（生成 .cursorrules）、trae（生成 .traerules）、antigravity（生成 .antigravityrules）、both（同时生成 cursor 和 trae）、all（同时生成所有 IDE 文件）",
)
@click.argument("files", nargs=-1, type=click.Path(exists=True))
@click.pass_context
def merge(ctx, output, stage, type, all, files, ide):
    """合并提示词文件"""
    base_path = ctx.obj["base_path"]
    merger = PromptMerger(base_path)
    
    # 根据 IDE 选项确定输出文件名
    ide_format = None
    output_files = []
    
    # IDE 文件扩展名映射
    ide_extensions = {
        "cursor": ".cursorrules",
        "trae": ".traerules",
        "antigravity": ".antigravityrules"
    }
    
    if ide:
        ide_lower = ide.lower()
        if ide_lower == "cursor":
            ide_format = "cursor"
            if output == "merged.md" or not output.endswith(tuple(ide_extensions.values())):
                # 如果输出文件名不是 .cursorrules，则自动改为 .cursorrules
                if output.endswith(".md"):
                    output = output[:-3] + ".cursorrules"
                elif not output.endswith(".cursorrules"):
                    output = output + ".cursorrules"
            output_files.append((output, "cursor"))
        elif ide_lower == "trae":
            ide_format = "trae"
            if output == "merged.md" or not output.endswith(tuple(ide_extensions.values())):
                # 如果输出文件名不是 .traerules，则自动改为 .traerules
                if output.endswith(".md"):
                    output = output[:-3] + ".traerules"
                elif not output.endswith(".traerules"):
                    output = output + ".traerules"
            output_files.append((output, "trae"))
        elif ide_lower == "antigravity":
            ide_format = "antigravity"
            if output == "merged.md" or not output.endswith(tuple(ide_extensions.values())):
                # 如果输出文件名不是 .antigravityrules，则自动改为 .antigravityrules
                if output.endswith(".md"):
                    output = output[:-3] + ".antigravityrules"
                elif not output.endswith(".antigravityrules"):
                    output = output + ".antigravityrules"
            output_files.append((output, "antigravity"))
        elif ide_lower == "both":
            # 同时生成 cursor 和 trae 两个文件
            base_output = output
            if base_output.endswith(".md"):
                base_output = base_output[:-3]
            elif base_output.endswith(tuple(ide_extensions.values())):
                base_output = base_output.rsplit(".", 1)[0]
            output_files.append((base_output + ".cursorrules", "cursor"))
            output_files.append((base_output + ".traerules", "trae"))
        elif ide_lower == "all":
            # 同时生成所有 IDE 文件（cursor、trae、antigravity）
            base_output = output
            if base_output.endswith(".md"):
                base_output = base_output[:-3]
            elif base_output.endswith(tuple(ide_extensions.values())):
                base_output = base_output.rsplit(".", 1)[0]
            output_files.append((base_output + ".cursorrules", "cursor"))
            output_files.append((base_output + ".traerules", "trae"))
            output_files.append((base_output + ".antigravityrules", "antigravity"))
    else:
        # 默认情况，使用原始输出文件名
        output_files.append((output, None))

    try:
        # 处理每个输出文件
        for output_file_path, format_type in output_files:
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
                        result_file = merger.merge(all_files, output_file_path, ide_format=format_type)
                        click.echo(f"✓ 已合并 {len(all_files)} 个提示词文件到: {result_file}")
                    else:
                        click.echo("警告: 未找到任何提示词文件", err=True)
                        sys.exit(1)
                finally:
                    # 清理临时文件
                    if os.path.exists(temp_file):
                        os.unlink(temp_file)
            elif stage:
                result_file = merger.merge_by_stage(stage, output_file_path, ide_format=format_type)
                click.echo(f"✓ 已合并阶段 '{stage}' 的提示词到: {result_file}")
            elif type:
                result_file = merger.merge_by_type(type, output_file_path, ide_format=format_type)
                click.echo(f"✓ 已合并类型 '{type}' 的提示词到: {result_file}")
            elif files:
                result_file = merger.merge(list(files), output_file_path, ide_format=format_type)
                click.echo(f"✓ 已合并 {len(files)} 个文件到: {result_file}")
            else:
                click.echo("错误: 请指定要合并的内容", err=True)
                click.echo("", err=True)
                click.echo("可用选项:", err=True)
                click.echo("  --all, -a          合并所有提示词", err=True)
                click.echo("  --stage STAGE      按阶段合并（如: common, development）", err=True)
                click.echo("  --type TYPE        按类型合并（如: frontend, backend）", err=True)
                click.echo("  --ide IDE          指定 IDE 格式（cursor/trae/antigravity/both/all）", err=True)
                click.echo("  FILES...           指定要合并的文件列表", err=True)
                click.echo("", err=True)
                click.echo("示例:", err=True)
                click.echo("  prompt-engine merge --all --output combined.md", err=True)
                click.echo("  prompt-engine merge --all --ide cursor --output .cursorrules", err=True)
                click.echo("  prompt-engine merge --all --ide trae --output .traerules", err=True)
                click.echo("  prompt-engine merge --all --ide antigravity --output .antigravityrules", err=True)
                click.echo("  prompt-engine merge --all --ide both --output rules", err=True)
                click.echo("  prompt-engine merge --all --ide all --output rules", err=True)
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

