#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案3：高级移动设备检测与优化

这个解决方案提供了更精确的移动设备检测和性能优化策略。
"""

import re
from typing import Dict, List, Optional, Tuple


class AdvancedMobileDetector:
    """高级移动设备检测器"""

    def __init__(self):
        """初始化检测规则"""
        self.device_patterns = {
            'iphone': r'iPhone.*OS\s+(\d+)',
            'ipad': r'iPad.*OS\s+(\d+)',
            'android_phone': r'Android\s+(\d+\.\d+).*Mobile',
            'android_tablet': r'Android\s+(\d+\.\d+)(?!.*Mobile)',
            'windows_phone': r'Windows Phone\s+OS\s+(\d+)',
            'windows_tablet': r'Windows NT\s+\d+\.\d+.*Touch'
        }

        self.performance_tiers = {
            'high': ['iPhone', 'iPad Pro', 'Samsung Galaxy S', 'Google Pixel'],
            'medium': ['iPad', 'Samsung Galaxy A', 'OnePlus', 'Xiaomi'],
            'low': ['Android Go', 'Feature Phone', 'Old Android']
        }

    def detect_device_type_and_version(self, user_agent: str) -> Dict[str, str]:
        """检测设备类型和版本"""
        result = {
            'device_type': 'desktop',
            'os': 'unknown',
            'os_version': 'unknown',
            'is_mobile': False,
            'is_tablet': False
        }

        if not user_agent:
            return result

        # 检测iOS设备
        if 'iPhone' in user_agent:
            result['device_type'] = 'mobile'
            result['os'] = 'iOS'
            result['is_mobile'] = True
            version_match = re.search(r'iPhone OS (\d+)_(\d+)', user_agent)
            if version_match:
                result['os_version'] = f"{version_match.group(1)}.{version_match.group(2)}"
        elif 'iPad' in user_agent:
            result['device_type'] = 'tablet'
            result['os'] = 'iOS'
            result['is_tablet'] = True
            version_match = re.search(r'CPU OS (\d+)_(\d+)', user_agent)
            if version_match:
                result['os_version'] = f"{version_match.group(1)}.{version_match.group(2)}"

        # 检测Android设备
        elif 'Android' in user_agent:
            if 'Mobile' in user_agent:
                result['device_type'] = 'mobile'
                result['is_mobile'] = True
            else:
                result['device_type'] = 'tablet'
                result['is_tablet'] = True

            result['os'] = 'Android'
            version_match = re.search(r'Android ([\d\.]+)', user_agent)
            if version_match:
                result['os_version'] = version_match.group(1)

        # 检测Windows设备
        elif 'Windows Phone' in user_agent:
            result['device_type'] = 'mobile'
            result['os'] = 'Windows Phone'
            result['is_mobile'] = True
            version_match = re.search(r'Windows Phone OS ([\d\.]+)', user_agent)
            if version_match:
                result['os_version'] = version_match.group(1)
        elif 'Windows NT' in user_agent and 'Touch' in user_agent:
            result['device_type'] = 'tablet'
            result['os'] = 'Windows'
            result['is_tablet'] = True

        return result

    def get_performance_tier(self, user_agent: str) -> str:
        """根据User-Agent判断设备性能等级"""
        if not user_agent:
            return 'unknown'

        user_agent_lower = user_agent.lower()

        for device in self.performance_tiers['high']:
            if device.lower() in user_agent_lower:
                return 'high'

        for device in self.performance_tiers['medium']:
            if device.lower() in user_agent_lower:
                return 'medium'

        for device in self.performance_tiers['low']:
            if device.lower() in user_agent_lower:
                return 'low'

        # 默认情况下，移动设备假设为中等性能，桌面设备假设为高性能
        if self.detect_device_type_and_version(user_agent)['is_mobile']:
            return 'medium'
        else:
            return 'high'

    def generate_optimized_content(self, user_agent: str, content_type: str = 'html') -> str:
        """生成针对设备优化的内容"""
        device_info = self.detect_device_type_and_version(user_agent)
        performance_tier = self.get_performance_tier(user_agent)

        if content_type == 'html':
            if device_info['is_mobile']:
                if performance_tier == 'low':
                    # 低性能设备：极简HTML
                    return self._generate_minimal_html()
                else:
                    # 中高性能设备：标准移动端HTML
                    return self._generate_mobile_html()
            else:
                # 桌面设备：完整HTML
                return self._generate_desktop_html()

        elif content_type == 'css':
            return self._generate_adaptive_css(performance_tier)

        elif content_type == 'js':
            return self._generate_conditional_js(device_info, performance_tier)

        return ""

    def _generate_minimal_html(self) -> str:
        """生成极简HTML（针对低性能设备）"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>轻量版</title>
    <style>
        body { font-family: sans-serif; margin: 10px; }
        .container { max-width: 100%; }
    </style>
</head>
<body>
    <div class="container">
        <h1>移动端优化内容</h1>
        <p>这是针对低性能设备的轻量版页面。</p>
    </div>
</body>
</html>
"""

    def _generate_mobile_html(self) -> str:
        """生成标准移动端HTML"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>移动端页面</title>
    <link rel="stylesheet" href="/styles/mobile.css">
    <link rel="manifest" href="/manifest.json">
</head>
<body>
    <div class="container">
        <h1>移动端优化内容</h1>
        <p>这是针对移动设备的标准页面。</p>
        <script src="/scripts/mobile.js" defer></script>
    </div>
</body>
</html>
"""

    def _generate_desktop_html(self) -> str:
        """生成桌面端HTML"""
        return """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>桌面端页面</title>
    <link rel="stylesheet" href="/styles/desktop.css">
</head>
<body>
    <div class="container">
        <h1>桌面端内容</h1>
        <p>这是针对桌面设备的完整页面。</p>
        <script src="/scripts/desktop.js" defer></script>
    </div>
</body>
</html>
"""

    def _generate_adaptive_css(self, performance_tier: str) -> str:
        """生成自适应CSS"""
        if performance_tier == 'low':
            return """
/* 轻量级CSS */
* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; margin: 0; padding: 10px; }
.container { max-width: 100%; }
img { max-width: 100%; height: auto; }
"""
        else:
            return """
/* 标准CSS */
* { box-sizing: border-box; }
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    margin: 0;
    padding: 20px;
    background: linear-gradient(to bottom, #f5f7fa, #c3cfe2);
}
.container {
    max-width: 1200px;
    margin: 0 auto;
    display: grid;
    gap: 20px;
}
img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
"""

    def _generate_conditional_js(self, device_info: Dict[str, str], performance_tier: str) -> str:
        """生成条件化JavaScript"""
        if performance_tier == 'low':
            return """
// 轻量级JavaScript
console.log('加载轻量版JS');
document.body.addEventListener('click', function(e) {
    console.log('点击:', e.target);
});
"""
        else:
            return f"""
// 标准JavaScript
console.log('设备信息:', {json.dumps(device_info)});
console.log('性能等级:', '{performance_tier}');

// 启用高级功能
if ('serviceWorker' in navigator && '{device_info["is_mobile"]}' === 'True') {{
    // 注册PWA Service Worker
    navigator.serviceWorker.register('/sw.js');
}}

// 触摸事件优化
document.body.addEventListener('touchstart', function(e) {{
    e.target.classList.add('active');
}}, {passive: true});

document.body.addEventListener('touchend', function(e) {{
    setTimeout(() => e.target.classList.remove('active'), 150);
}});
"""


def main():
    """主函数：演示高级移动设备检测"""
    detector = AdvancedMobileDetector()

    test_cases = [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 Mobile",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    ]

    for ua in test_cases:
        print(f"\n🔍 分析 User-Agent: {ua[:50]}...")

        device_info = detector.detect_device_type_and_version(ua)
        performance_tier = detector.get_performance_tier(ua)

        print(f"设备类型: {device_info['device_type']}")
        print(f"操作系统: {device_info['os']} {device_info['os_version']}")
        print(f"性能等级: {performance_tier}")

        # 生成优化内容示例
        html_content = detector.generate_optimized_content(ua, 'html')
        print(f"HTML长度: {len(html_content)} 字符")


if __name__ == "__main__":
    main()