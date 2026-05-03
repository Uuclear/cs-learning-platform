#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案1：扩展的Markdown文档生成器

这个解决方案扩展了示例1的功能，支持类文档生成、
模块级别文档提取，并可以将输出保存到文件。
"""

import inspect
import os
from typing import Any, Callable, Dict, List, Optional, Type


def extract_function_docs(func: Callable) -> Dict[str, Any]:
    """从函数对象提取文档信息"""
    sig = inspect.signature(func)
    docstring = func.__doc__ or "无文档说明"

    return {
        "name": func.__name__,
        "signature": str(sig),
        "docstring": docstring.strip(),
        "module": func.__module__,
        "type": "function"
    }


def extract_class_docs(cls: Type) -> Dict[str, Any]:
    """从类对象提取文档信息"""
    methods = []
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        if not name.startswith('_') or name in ['__init__', '__str__', '__repr__']:
            methods.append(extract_function_docs(method))

    docstring = cls.__doc__ or "无文档说明"

    return {
        "name": cls.__name__,
        "docstring": docstring.strip(),
        "methods": methods,
        "module": cls.__module__,
        "type": "class"
    }


def extract_module_docs(module) -> Dict[str, Any]:
    """从模块对象提取文档信息"""
    docstring = module.__doc__ or "无模块文档"

    # 获取模块中的函数和类
    functions = []
    classes = []

    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and obj.__module__ == module.__name__:
            functions.append(extract_function_docs(obj))
        elif inspect.isclass(obj) and obj.__module__ == module.__name__:
            classes.append(extract_class_docs(obj))

    return {
        "name": module.__name__,
        "docstring": docstring.strip(),
        "functions": functions,
        "classes": classes,
        "type": "module"
    }


def generate_markdown_docs_from_module(module) -> str:
    """从模块生成完整的Markdown文档"""
    module_info = extract_module_docs(module)

    markdown = f"# 模块: {module_info['name']}\n\n"
    markdown += f"{module_info['docstring']}\n\n"

    if module_info['functions']:
        markdown += "## 函数\n\n"
        for func in module_info['functions']:
            markdown += f"### `{func['name']}`\n\n"
            markdown += f"**签名**: `{func['signature']}`\n\n"
            markdown += f"{func['docstring']}\n\n"

    if module_info['classes']:
        markdown += "## 类\n\n"
        for cls in module_info['classes']:
            markdown += f"### `{cls['name']}`\n\n"
            markdown += f"{cls['docstring']}\n\n"

            if cls['methods']:
                markdown += "**方法**:\n\n"
                for method in cls['methods']:
                    markdown += f"- `{method['name']}`: {method['docstring']}\n"
            markdown += "\n"

    return markdown


def save_markdown_docs(markdown_content: str, output_file: str) -> None:
    """将Markdown内容保存到文件"""
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)


if __name__ == "__main__":
    # 示例：为当前模块生成文档
    import sys
    current_module = sys.modules[__name__]
    docs = generate_markdown_docs_from_module(current_module)
    print(docs)

    # 保存到文件
    save_markdown_docs(docs, "output/module_docs.md")
    print(f"\n文档已保存到: output/module_docs.md")