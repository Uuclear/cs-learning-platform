#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 2: 安全的依赖管理

这个脚本展示了如何安全地管理项目依赖，
包括使用锁定文件和定期更新。
"""

import json
from typing import Dict, List


def create_secure_requirements() -> str:
    """
    创建安全的依赖配置示例
    """
    secure_deps = {
        "dependencies": {
            # 使用精确版本号
            "requests": "==2.31.0",  # 最新安全版本
            "django": "==4.2.7",     # LTS版本，定期安全更新
            "flask": "==2.3.3"       # 最新稳定版本
        },
        "security_practices": [
            "使用requirements.txt锁定确切版本",
            "定期运行pip-audit检查漏洞",
            "设置自动依赖更新（如Dependabot）",
            "使用虚拟环境隔离依赖"
        ]
    }

    return json.dumps(secure_deps, indent=2, ensure_ascii=False)


def generate_pip_audit_command() -> str:
    """
    生成pip-audit命令示例
    """
    return "pip install pip-audit && pip-audit -r requirements.txt"


# 安全实践示例
SECURITY_PRACTICES = '''
# .github/dependabot.yml 示例
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"

# CI/CD中的安全扫描步骤
- name: 依赖漏洞扫描
  run: |
    pip install safety
    safety check -r requirements.txt --full-report
'''