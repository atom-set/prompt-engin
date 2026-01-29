"""YAML utility functions"""

import re
from typing import Dict, Optional, Tuple


def parse_frontmatter(content: str) -> Tuple[Optional[Dict], str]:
    """
    解析 YAML frontmatter
    
    Args:
        content: 文件内容
    
    Returns:
        (metadata_dict, content_without_frontmatter)
    """
    # 检查是否有 frontmatter
    if not content.startswith('---\n'):
        return None, content
    
    # 查找第二个 ---
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return None, content
    
    frontmatter_text = parts[1]
    content_without_frontmatter = parts[2]
    
    # 解析 frontmatter
    metadata = {}
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            
            # 处理列表格式 [a, b, c]
            if value.startswith('[') and value.endswith(']'):
                value = [item.strip().strip("'\"") for item in value[1:-1].split(',')]
            # 处理整数类型（如 priority）
            elif key == 'priority':
                try:
                    value = int(value)
                except ValueError:
                    pass  # 保持原值，后续验证会报错
            
            metadata[key] = value
    
    return metadata, content_without_frontmatter


def validate_frontmatter(metadata: Dict) -> Tuple[bool, list]:
    """
    验证 frontmatter 格式
    
    Args:
        metadata: 元数据字典
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    # 必需字段
    required_fields = ['name', 'description', 'tags']
    for field in required_fields:
        if field not in metadata:
            errors.append(f"缺少必需字段: {field}")
    
    # 验证 tags 是列表
    if 'tags' in metadata and not isinstance(metadata['tags'], list):
        errors.append("tags 必须是列表格式")
    
    # 验证 priority（可选字段，但如果存在必须是 1-4 的整数）
    if 'priority' in metadata:
        priority = metadata['priority']
        if not isinstance(priority, int):
            try:
                priority = int(priority)
            except (ValueError, TypeError):
                errors.append("priority 必须是整数")
        elif priority < 1 or priority > 4:
            errors.append("priority 必须在 1-4 之间")
    
    return len(errors) == 0, errors


def extract_metadata(content: str) -> Optional[Dict]:
    """
    提取 skill 的元数据
    
    Args:
        content: 文件内容
    
    Returns:
        元数据字典，如果没有 frontmatter 返回 None
    """
    metadata, _ = parse_frontmatter(content)
    return metadata
