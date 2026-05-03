#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例 2: 依赖项漏洞扫描模拟器

这个脚本模拟了软件依赖项扫描工具的功能，
用于检测项目依赖中已知的安全漏洞。
"""

import json
import random
from typing import Dict, List, Tuple


def simulate_vulnerability_database() -> Dict[str, List[Dict]]:
    """
    模拟漏洞数据库

    返回:
        包含包名和对应漏洞列表的字典
    """
    return {
        "requests": [
            {"id": "CVE-2023-1234", "severity": "HIGH", "description": "HTTP请求伪造漏洞"},
            {"id": "CVE-2022-5678", "severity": "MEDIUM", "description": "证书验证绕过"}
        ],
        "django": [
            {"id": "CVE-2023-9876", "severity": "CRITICAL", "description": "远程代码执行漏洞"},
            {"id": "CVE-2023-5432", "severity": "HIGH", "description": "跨站脚本漏洞"}
        ],
        "flask": [
            {"id": "CVE-2022-1111", "severity": "MEDIUM", "description": "会话固定漏洞"}
        ],
        "numpy": [
            {"id": "CVE-2023-2222", "severity": "LOW", "description": "内存泄漏问题"}
        ]
    }


def parse_requirements_file(content: str) -> Dict[str, str]:
    """
    解析requirements.txt格式的依赖文件

    参数:
        content: 文件内容字符串

    返回:
        包名和版本号的字典
    """
    dependencies = {}
    for line in content.strip().split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            # 处理各种依赖格式
            if '==' in line:
                package, version = line.split('==', 1)
                dependencies[package.strip()] = version.strip()
            elif '>=' in line:
                package, _ = line.split('>=', 1)
                dependencies[package.strip()] = "unknown"
            elif '<=' in line:
                package, _ = line.split('<=', 1)
                dependencies[package.strip()] = "unknown"
            elif line:  # 只有包名
                dependencies[line] = "latest"

    return dependencies


def scan_dependencies(dependencies: Dict[str, str], vuln_db: Dict[str, List[Dict]]) -> List[Dict]:
    """
    扫描依赖项中的漏洞

    参数:
        dependencies: 依赖项字典 {包名: 版本}
        vuln_db: 漏洞数据库

    返回:
        发现的漏洞列表
    """
    vulnerabilities = []

    for package, version in dependencies.items():
        if package in vuln_db:
            for vuln in vuln_db[package]:
                vulnerabilities.append({
                    "package": package,
                    "version": version,
                    "vulnerability_id": vuln["id"],
                    "severity": vuln["severity"],
                    "description": vuln["description"]
                })

    return vulnerabilities


def get_severity_score(severity: str) -> int:
    """获取严重性评分"""
    scores = {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}
    return scores.get(severity, 0)


def main():
    """主函数：演示依赖项扫描"""
    print("=== 依赖项漏洞扫描模拟器 ===")

    # 模拟的requirements.txt内容
    requirements_content = """
# 项目依赖
requests==2.28.1
django==4.1.5
flask>=2.0.0
numpy
pandas==1.5.2
# 开发依赖
pytest==7.2.0
black
"""

    # 加载漏洞数据库
    vuln_db = simulate_vulnerability_database()

    # 解析依赖
    dependencies = parse_requirements_file(requirements_content)
    print(f"\n发现 {len(dependencies)} 个依赖项:")
    for package, version in dependencies.items():
        print(f"  - {package} ({version})")

    # 扫描漏洞
    vulnerabilities = scan_dependencies(dependencies, vuln_db)

    if vulnerabilities:
        print(f"\n⚠️  发现 {len(vulnerabilities)} 个安全漏洞:")

        # 按严重性排序
        vulnerabilities.sort(key=lambda x: get_severity_score(x["severity"]), reverse=True)

        for vuln in vulnerabilities:
            print(f"\n  包: {vuln['package']} (版本: {vuln['version']})")
            print(f"  漏洞ID: {vuln['vulnerability_id']}")
            print(f"  严重性: {vuln['severity']}")
            print(f"  描述: {vuln['description']}")

        # 统计严重性
        severity_counts = {}
        for vuln in vulnerabilities:
            severity = vuln["severity"]
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        print(f"\n严重性统计:")
        for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
            if severity in severity_counts:
                print(f"  {severity}: {severity_counts[severity]} 个")

        print("\n建议：在CI/CD管道中集成SCA（软件组成分析）工具")
        print("      定期扫描依赖项并及时更新到安全版本")
    else:
        print("\n✅ 未发现已知的安全漏洞！")


if __name__ == "__main__":
    main()