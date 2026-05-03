#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cypress E2E 测试模拟器

这个文件模拟了 Cypress 端到端测试的核心功能：
- 页面导航 (visit)
- 元素查询 (get, contains)
- 用户交互 (click, type)
- 断言验证 (should)
- 网络请求 stubbing

注意：这是一个教学演示，用于理解 E2E 测试的概念。
"""

from typing import Dict, List, Optional, Callable
import time


class Page:
    """模拟网页页面"""

    def __init__(self, url: str):
        self.url = url
        self.elements = self._load_page_elements(url)

    def _load_page_elements(self, url: str) -> Dict[str, 'Element']:
        """根据 URL 加载页面元素"""
        elements = {}

        if "login" in url:
            # 登录页面元素
            elements["username"] = Element("input", {"id": "username", "placeholder": "用户名"})
            elements["password"] = Element("input", {"id": "password", "placeholder": "密码"})
            elements["submit"] = Element("button", {"id": "submit", "text": "登录"})
            elements["error"] = Element("div", {"id": "error", "text": "", "hidden": True})
        elif "dashboard" in url:
            # 仪表板页面元素
            elements["welcome"] = Element("h1", {"id": "welcome", "text": "欢迎回来！"})
            elements["logout"] = Element("button", {"id": "logout", "text": "退出登录"})
        else:
            # 默认首页
            elements["login-link"] = Element("a", {"id": "login-link", "text": "登录", "href": "/login"})

        return elements

    def get_element(self, selector: str) -> 'Element':
        """通过选择器获取元素"""
        # 简化的选择器解析
        if selector.startswith("#"):
            element_id = selector[1:]
            if element_id in self.elements:
                return self.elements[element_id]
        elif selector.startswith("["):
            # 属性选择器 [placeholder="用户名"]
            attr_part = selector[1:-1]
            if "=" in attr_part:
                attr_name, attr_value = attr_part.split("=", 1)
                attr_value = attr_value.strip('"')
                for element in self.elements.values():
                    if element.attrs.get(attr_name.strip()) == attr_value:
                        return element

        raise Exception(f"找不到元素: {selector}")

    def contains_text(self, text: str) -> 'Element':
        """查找包含指定文本的元素"""
        for element in self.elements.values():
            if element.text and text in element.text:
                return element
        raise Exception(f"找不到包含文本 '{text}' 的元素")


class Element:
    """模拟 HTML 元素"""

    def __init__(self, tag: str, attrs: Dict):
        self.tag = tag
        self.attrs = attrs
        self.text = attrs.get("text", "")
        self.value = ""
        self.hidden = attrs.get("hidden", False)

    def click(self):
        """模拟点击元素"""
        if self.hidden:
            raise Exception("无法点击隐藏元素")
        print(f"🖱️ 点击元素: {self.tag} ({self.attrs})")

        # 模拟点击后的页面跳转
        if self.attrs.get("href"):
            return Page(self.attrs["href"])
        return None

    def type(self, text: str):
        """模拟输入文本"""
        if self.hidden:
            raise Exception("无法在隐藏元素中输入")
        self.value = text
        print(f"⌨️ 在元素中输入: '{text}'")

    def should(self, assertion: str, expected_value: str = None):
        """执行断言"""
        if assertion == "be.visible":
            assert not self.hidden, "元素应该是可见的"
        elif assertion == "contain.text":
            assert expected_value in self.text, f"元素应该包含文本 '{expected_value}'"
        elif assertion == "have.value":
            assert self.value == expected_value, f"元素值应该是 '{expected_value}'"
        elif assertion == "exist":
            pass  # 元素存在（因为我们已经获取到了）
        else:
            raise Exception(f"不支持的断言: {assertion}")


class Cypress:
    """模拟 Cypress 测试框架"""

    def __init__(self):
        self.current_page = None
        self.intercepted_requests = {}

    def visit(self, url: str):
        """访问指定 URL"""
        print(f"🌐 访问页面: {url}")
        self.current_page = Page(url)
        # 模拟页面加载时间
        time.sleep(0.1)

    def get(self, selector: str) -> Element:
        """获取元素"""
        return self.current_page.get_element(selector)

    def contains(self, text: str) -> Element:
        """查找包含文本的元素"""
        return self.current_page.contains_text(text)

    def intercept(self, url_pattern: str, mock_response: Dict = None):
        """拦截网络请求（stubbing）"""
        self.intercepted_requests[url_pattern] = mock_response
        print(f"📡 拦截请求: {url_pattern}")

    def wait(self, ms: int):
        """等待指定毫秒"""
        time.sleep(ms / 1000)


# E2E 测试示例
def test_user_login_flow():
    """测试用户登录流程"""

    cy = Cypress()

    # 访问首页
    cy.visit("/")

    # 点击登录链接
    login_link = cy.get("#login-link")
    login_link.should("be.visible")
    login_link.should("contain.text", "登录")

    # 跳转到登录页面
    cy.visit("/login")

    # 验证登录表单元素存在
    username_input = cy.get("#username")
    password_input = cy.get("#password")
    submit_button = cy.get("#submit")

    username_input.should("exist")
    password_input.should("exist")
    submit_button.should("contain.text", "登录")

    # 输入凭据并提交
    username_input.type("testuser")
    password_input.type("password123")

    # 模拟 API 响应
    cy.intercept("/api/login", {"success": True, "user": {"name": "Test User"}})

    # 提交表单
    new_page = submit_button.click()
    if new_page:
        cy.current_page = new_page

    # 验证跳转到仪表板
    cy.visit("/dashboard")
    welcome_message = cy.contains("欢迎回来！")
    welcome_message.should("be.visible")

    print("✅ 用户登录 E2E 测试通过!")


def test_login_error_handling():
    """测试登录错误处理"""

    cy = Cypress()
    cy.visit("/login")

    # 输入错误凭据
    username_input = cy.get("#username")
    password_input = cy.get("#password")
    username_input.type("invalid")
    password_input.type("wrong")

    # 模拟 API 返回错误
    cy.intercept("/api/login", {"success": False, "error": "无效的凭据"})

    submit_button = cy.get("#submit")
    submit_button.click()

    # 验证错误消息显示
    error_message = cy.get("#error")
    # 在真实场景中，错误消息会被更新，这里简化处理
    error_message.text = "无效的凭据"
    error_message.hidden = False

    error_message.should("be.visible")
    error_message.should("contain.text", "无效的凭据")

    print("✅ 登录错误处理 E2E 测试通过!")


if __name__ == "__main__":
    print("🚀 开始运行 Cypress E2E 测试模拟...")

    test_user_login_flow()
    test_login_error_handling()

    print("🏁 E2E 测试模拟完成!")