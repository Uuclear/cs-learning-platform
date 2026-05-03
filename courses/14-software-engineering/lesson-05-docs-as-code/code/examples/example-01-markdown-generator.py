#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例1：从Python docstrings生成Markdown文档

这个脚本演示了如何从Python函数的docstrings自动生成Markdown格式的API文档。
通过使用inspect模块，我们可以提取函数的签名、文档字符串等信息，
然后将其转换为结构化的Markdown文档。
"""

import inspect
from typing import Any, Callable, Dict, List, Optional


def extract_function_docs(func: Callable) -> Dict[str, Any]:
    """
    从函数对象提取文档信息

    参数:
        func: 要分析的函数对象

    返回:
        包含函数名称、签名、文档字符串和模块信息的字典
    """
    # 获取函数签名
    sig = inspect.signature(func)
    # 获取文档字符串，如果没有则使用默认值
    docstring = func.__doc__ or "无文档说明"

    return {
        "name": func.__name__,
        "signature": str(sig),
        "docstring": docstring.strip(),
        "module": func.__module__
    }


def generate_markdown_docs(functions: List[Callable]) -> str:
    """
    生成Markdown格式的文档

    参数:
        functions: 要生成文档的函数列表

    返回:
        Markdown格式的文档字符串
    """
    # 初始化Markdown文档
    markdown = "# API 文档\n\n"

    # 遍历每个函数并生成文档
    for func in functions:
        info = extract_function_docs(func)
        # 添加函数标题
        markdown += f"## `{info['name']}`\n\n"
        # 添加函数签名
        markdown += f"**签名**: `{info['signature']}`\n\n"
        # 添加文档字符串
        markdown += f"{info['docstring']}\n\n"
        # 添加分隔线
        markdown += "---\n\n"

    return markdown


def example_function(a: int, b: str = "default") -> str:
    """
    示例函数，用于演示文档生成

    这个函数接受一个整数和一个字符串参数，
    返回格式化的字符串结果。

    参数:
        a: 整数参数
        b: 字符串参数，默认值为"default"

    返回:
        格式化的字符串
    """
    return f"参数a={a}, 参数b={b}"


if __name__ == "__main__":
    # 演示用法
    functions_to_document = [example_function, extract_function_docs, generate_markdown_docs]
    docs = generate_markdown_docs(functions_to_document)
    print(docs)