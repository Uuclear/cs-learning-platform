#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例3：移动设备检测器

这个脚本从User-Agent字符串检测移动设备与桌面设备，
并根据检测结果提供相应的内容或重定向。
"""

import re
from typing import Dict, Optional


class MobileDetector:
    """移动设备检测器类"""

    def __init__(self):
        """初始化移动设备检测模式"""
        # 移动设备User-Agent关键词
        self.mobile_patterns = [
            r'Android',
            r'iPhone',
            r'iPad',
            r'iPod',
            r'Windows Phone',
            r'Mobile',
            r'Tablet',
            r'BlackBerry',
            r'Opera Mini',
            r'Opera Mobi'
        ]

        # 桌面设备User-Agent关键词（用于排除）
        self.desktop_patterns = [
            r'Windows NT',
            r'Macintosh',
            r'Linux x86_64'
        ]

    def is_mobile(self, user_agent: str) -> bool:
        """
        检测是否为移动设备

        :param user_agent: User-Agent字符串
        :return: True表示移动设备，False表示桌面设备
        """
        if not user_agent:
            return False

        user_agent_lower = user_agent.lower()

        # 检查是否包含移动设备关键词
        for pattern in self.mobile_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                return True

        # 检查是否明确是桌面设备
        for pattern in self.desktop_patterns:
            if re.search(pattern, user_agent, re.IGNORECASE):
                # 但要排除同时包含Mobile的情况（如Windows Mobile）
                if not re.search(r'mobile', user_agent_lower):
                    return False

        # 默认情况下，如果没有明确的移动标识，假设为桌面设备
        return False

    def get_device_info(self, user_agent: str) -> Dict[str, Optional[str]]:
        """
        获取详细的设备信息

        :param user_agent: User-Agent字符串
        :return: 设备信息字典
        """
        info = {
            "device_type": "unknown",
            "os": "unknown",
            "browser": "unknown"
        }

        if not user_agent:
            return info

        # 检测操作系统
        if re.search(r'Android', user_agent, re.IGNORECASE):
            info["os"] = "Android"
        elif re.search(r'iPhone|iPad|iPod', user_agent, re.IGNORECASE):
            info["os"] = "iOS"
        elif re.search(r'Windows Phone', user_agent, re.IGNORECASE):
            info["os"] = "Windows Phone"
        elif re.search(r'Windows NT', user_agent, re.IGNORECASE):
            info["os"] = "Windows"
        elif re.search(r'Macintosh', user_agent, re.IGNORECASE):
            info["os"] = "macOS"
        elif re.search(r'Linux', user_agent, re.IGNORECASE):
            info["os"] = "Linux"

        # 检测浏览器
        if re.search(r'Chrome', user_agent, re.IGNORECASE):
            info["browser"] = "Chrome"
        elif re.search(r'Safari', user_agent, re.IGNORECASE):
            info["browser"] = "Safari"
        elif re.search(r'Firefox', user_agent, re.IGNORECASE):
            info["browser"] = "Firefox"
        elif re.search(r'Edge', user_agent, re.IGNORECASE):
            info["browser"] = "Edge"
        elif re.search(r'Opera', user_agent, re.IGNORECASE):
            info["browser"] = "Opera"

        # 确定设备类型
        if self.is_mobile(user_agent):
            if re.search(r'Pad|Tablet', user_agent, re.IGNORECASE):
                info["device_type"] = "tablet"
            else:
                info["device_type"] = "mobile"
        else:
            info["device_type"] = "desktop"

        return info

    def serve_content(self, user_agent: str, mobile_content: str, desktop_content: str) -> str:
        """
        根据设备类型提供相应内容

        :param user_agent: User-Agent字符串
        :param mobile_content: 移动端内容
        :param desktop_content: 桌面端内容
        :return: 选择的内容
        """
        if self.is_mobile(user_agent):
            return mobile_content
        else:
            return desktop_content


def main():
    """主函数：演示移动设备检测"""
    print("📱 移动设备检测器")
    print("=" * 50)

    detector = MobileDetector()

    # 测试用例
    test_cases = [
        {
            "name": "iPhone Safari",
            "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        },
        {
            "name": "Android Chrome",
            "user_agent": "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.97 Mobile Safari/537.36"
        },
        {
            "name": "iPad Safari",
            "user_agent": "Mozilla/5.0 (iPad; CPU OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1"
        },
        {
            "name": "Windows Chrome",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        },
        {
            "name": "Mac Safari",
            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"
        }
    ]

    print("🔍 设备检测结果:")
    for case in test_cases:
        is_mobile = detector.is_mobile(case["user_agent"])
        device_info = detector.get_device_info(case["user_agent"])

        print(f"\n{case['name']}:")
        print(f"  是否移动设备: {'✅ 是' if is_mobile else '❌ 否'}")
        print(f"  设备类型: {device_info['device_type']}")
        print(f"  操作系统: {device_info['os']}")
        print(f"  浏览器: {device_info['browser']}")

    print("\n" + "=" * 50)
    print("📄 内容服务演示:")

    mobile_content = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>移动端页面</title></head><body><h1>欢迎使用移动端！</h1></body></html>"
    desktop_content = "<!DOCTYPE html><html><head><title>桌面端页面</title></head><body><h1>欢迎使用桌面端！</h1></body></html>"

    # 测试内容服务
    test_ua = test_cases[0]["user_agent"]  # iPhone
    served_content = detector.serve_content(test_ua, mobile_content, desktop_content)

    if "移动端页面" in served_content:
        print("✅ 成功为移动设备提供移动端内容")
    else:
        print("❌ 内容服务失败")


if __name__ == "__main__":
    main()