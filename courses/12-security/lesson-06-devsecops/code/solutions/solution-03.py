#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 3: 安全的密钥管理

这个脚本展示了如何安全地处理敏感信息，
避免在代码中硬编码密钥。
"""

import os
from typing import Optional, List


class SecureConfig:
    """
    安全配置管理类
    使用环境变量和密钥管理服务
    """

    def __init__(self):
        self._config = {}

    def get_secret(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        从环境变量安全获取密钥

        参数:
            key: 环境变量名
            default: 默认值

        返回:
            密钥值或None
        """
        return os.environ.get(key, default)

    def validate_secrets(self, required_keys: List[str]) -> bool:
        """
        验证必需的密钥是否存在

        参数:
            required_keys: 必需的环境变量列表

        返回:
            所有密钥都存在则返回True
        """
        missing_keys = []
        for key in required_keys:
            if not os.environ.get(key):
                missing_keys.append(key)

        if missing_keys:
            print(f"错误：缺少必需的环境变量: {', '.join(missing_keys)}")
            return False

        return True


def setup_environment_example() -> str:
    """
    环境设置示例
    """
    example = '''
# .env 文件示例（不要提交到版本控制！）
DATABASE_URL=postgresql://user:password@localhost/mydb
API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here

# .gitignore 中添加
.env
*.key
*.pem
secrets/

# Docker运行时传递环境变量
docker run -e API_KEY=$API_KEY myapp

# Kubernetes Secret示例
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  api-key: <base64-encoded-key>
'''
    return example


# 使用示例
def main():
    """主函数示例"""
    config = SecureConfig()

    # 获取密钥
    api_key = config.get_secret("API_KEY")
    db_url = config.get_secret("DATABASE_URL")

    # 验证必需密钥
    if config.validate_secrets(["API_KEY", "DATABASE_URL"]):
        print("✅ 所有必需的密钥都已配置")
    else:
        print("❌ 缺少必需的密钥配置")


if __name__ == "__main__":
    main()