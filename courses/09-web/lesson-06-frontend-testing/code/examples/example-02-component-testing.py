#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
React 组件测试模拟器

这个文件模拟了 React Testing Library 的核心功能：
- 组件渲染 (render)
- 查询元素 (getByRole, getByText 等)
- 用户交互 (fireEvent.click)
- 断言验证

注意：这是一个教学演示，用于理解组件测试的概念。
"""

from typing import Dict, List, Optional, Callable


class Component:
    """模拟 React 组件"""

    def __init__(self, name: str, props: Dict = None):
        self.name = name
        self.props = props or {}
        self.state = {}
        self.render_count = 0

    def render(self) -> 'ComponentOutput':
        """渲染组件并返回输出"""
        self.render_count += 1

        # 模拟不同组件的渲染逻辑
        if self.name == "Button":
            return ComponentOutput(
                text=self.props.get("children", "按钮"),
                role="button",
                disabled=self.props.get("disabled", False),
                click_handler=self.props.get("onClick")
            )
        elif self.name == "LoginForm":
            return ComponentOutput(
                children=[
                    ComponentOutput(text="用户名", role="label"),
                    ComponentOutput(role="textbox", placeholder="输入用户名"),
                    ComponentOutput(text="密码", role="label"),
                    ComponentOutput(role="textbox", placeholder="输入密码"),
                    ComponentOutput(text="登录", role="button", click_handler=self.props.get("onSubmit"))
                ]
            )
        else:
            return ComponentOutput(text=f"未知组件: {self.name}")


class ComponentOutput:
    """模拟组件渲染输出"""

    def __init__(self, text: str = "", role: str = "", **kwargs):
        self.text = text
        self.role = role
        self.children = kwargs.get("children", [])
        self.disabled = kwargs.get("disabled", False)
        self.placeholder = kwargs.get("placeholder", "")
        self.click_handler = kwargs.get("click_handler")


class Screen:
    """模拟 testing-library/screen 对象"""

    def __init__(self, component_output: ComponentOutput):
        self.component_output = component_output

    def get_by_role(self, role: str) -> ComponentOutput:
        """根据 ARIA role 查询元素"""
        elements = self._find_elements_by_role(self.component_output, role)
        if not elements:
            raise Exception(f"找不到 role='{role}' 的元素")
        return elements[0]  # 返回第一个匹配的元素

    def get_by_text(self, text: str) -> ComponentOutput:
        """根据文本内容查询元素"""
        elements = self._find_elements_by_text(self.component_output, text)
        if not elements:
            raise Exception(f"找不到包含文本 '{text}' 的元素")
        return elements[0]

    def _find_elements_by_role(self, output: ComponentOutput, role: str) -> List[ComponentOutput]:
        """递归查找指定 role 的元素"""
        elements = []
        if output.role == role:
            elements.append(output)
        for child in output.children:
            elements.extend(self._find_elements_by_role(child, role))
        return elements

    def _find_elements_by_text(self, output: ComponentOutput, text: str) -> List[ComponentOutput]:
        """递归查找包含指定文本的元素"""
        elements = []
        if output.text == text:
            elements.append(output)
        for child in output.children:
            elements.extend(self._find_elements_by_text(child, text))
        return elements


def render(component: Component) -> Screen:
    """渲染组件并返回 screen 对象"""
    output = component.render()
    return Screen(output)


class fireEvent:
    """模拟用户事件"""

    @staticmethod
    def click(element: ComponentOutput):
        """模拟点击事件"""
        if element.disabled:
            raise Exception("无法点击禁用的元素")
        if element.click_handler:
            element.click_handler()


# 测试示例
def test_button_component():
    """测试 Button 组件"""

    def setup_button_with_click():
        click_count = {"count": 0}

        def handle_click():
            click_count["count"] += 1

        button = Component("Button", {
            "children": "点击我",
            "onClick": handle_click
        })
        return button, click_count

    def test_button_renders_correctly():
        button, _ = setup_button_with_click()
        screen = render(button)

        button_element = screen.get_by_role("button")
        assert button_element.text == "点击我"
        assert not button_element.disabled

    def test_button_click_handler():
        button, click_count = setup_button_with_click()
        screen = render(button)

        button_element = screen.get_by_role("button")
        fireEvent.click(button_element)

        assert click_count["count"] == 1

    def test_disabled_button():
        disabled_button = Component("Button", {
            "children": "禁用按钮",
            "disabled": True
        })
        screen = render(disabled_button)

        button_element = screen.get_by_role("button")
        assert button_element.disabled

        try:
            fireEvent.click(button_element)
            assert False, "应该抛出异常"
        except Exception:
            pass  # 预期的异常

    print("✅ Button 组件渲染正确")
    test_button_renders_correctly()

    print("✅ Button 点击处理器工作正常")
    test_button_click_handler()

    print("✅ 禁用按钮无法点击")
    test_disabled_button()


def test_login_form_component():
    """测试 LoginForm 组件"""

    def setup_login_form():
        submit_called = {"called": False}

        def handle_submit():
            submit_called["called"] = True

        form = Component("LoginForm", {"onSubmit": handle_submit})
        return form, submit_called

    def test_form_has_required_elements():
        form, _ = setup_login_form()
        screen = render(form)

        # 验证表单包含必要的元素
        username_label = screen.get_by_text("用户名")
        password_label = screen.get_by_text("密码")
        login_button = screen.get_by_text("登录")

        assert username_label.role == "label"
        assert password_label.role == "label"
        assert login_button.role == "button"

    def test_form_submission():
        form, submit_called = setup_login_form()
        screen = render(form)

        login_button = screen.get_by_text("登录")
        fireEvent.click(login_button)

        assert submit_called["called"] == True

    print("✅ 登录表单包含必要元素")
    test_form_has_required_elements()

    print("✅ 登录表单提交功能正常")
    test_form_submission()


if __name__ == "__main__":
    print("🚀 开始运行 React 组件测试模拟...")

    test_button_component()
    test_login_form_component()

    print("🏁 组件测试模拟完成!")