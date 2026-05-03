#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 02: React 组件测试实现

这个文件提供了完整的 React 组件测试模拟实现，
包括组件渲染、元素查询、用户交互和断言验证。
"""

from typing import Dict, List, Optional, Callable


class Component:
    """React 组件的完整实现"""

    def __init__(self, name: str, props: Dict = None):
        self.name = name
        self.props = props or {}
        self.state = {}
        self.render_count = 0

    def set_state(self, new_state: Dict):
        """更新组件状态"""
        self.state.update(new_state)

    def render(self) -> 'ComponentOutput':
        self.render_count += 1

        if self.name == "Counter":
            count = self.state.get("count", 0)
            return ComponentOutput(
                children=[
                    ComponentOutput(text=f"计数: {count}", role="status"),
                    ComponentOutput(text="增加", role="button", click_handler=lambda: self.set_state({"count": count + 1})),
                    ComponentOutput(text="重置", role="button", click_handler=lambda: self.set_state({"count": 0}))
                ]
            )
        elif self.name == "Toggle":
            is_on = self.state.get("isOn", False)
            return ComponentOutput(
                children=[
                    ComponentOutput(text="开关", role="switch", checked=is_on),
                    ComponentOutput(text="切换", role="button", click_handler=lambda: self.set_state({"isOn": not is_on}))
                ]
            )
        elif self.name == "UserCard":
            user = self.props.get("user", {"name": "未知用户", "email": ""})
            return ComponentOutput(
                children=[
                    ComponentOutput(text=user["name"], role="heading"),
                    ComponentOutput(text=user["email"], role="text"),
                    ComponentOutput(text="编辑", role="button", click_handler=self.props.get("onEdit"))
                ]
            )
        else:
            return ComponentOutput(text=f"组件: {self.name}")


class ComponentOutput:
    """组件渲染输出的完整实现"""

    def __init__(self, text: str = "", role: str = "", **kwargs):
        self.text = text
        self.role = role
        self.children = kwargs.get("children", [])
        self.disabled = kwargs.get("disabled", False)
        self.placeholder = kwargs.get("placeholder", "")
        self.click_handler = kwargs.get("click_handler")
        self.checked = kwargs.get("checked", False)


class Screen:
    """testing-library/screen 的完整实现"""

    def __init__(self, component_output: ComponentOutput):
        self.component_output = component_output

    def get_by_role(self, role: str) -> ComponentOutput:
        elements = self._find_elements_by_role(self.component_output, role)
        if not elements:
            raise Exception(f"找不到 role='{role}' 的元素")
        return elements[0]

    def get_all_by_role(self, role: str) -> List[ComponentOutput]:
        elements = self._find_elements_by_role(self.component_output, role)
        if not elements:
            raise Exception(f"找不到 role='{role}' 的元素")
        return elements

    def get_by_text(self, text: str) -> ComponentOutput:
        elements = self._find_elements_by_text(self.component_output, text)
        if not elements:
            raise Exception(f"找不到包含文本 '{text}' 的元素")
        return elements[0]

    def query_by_role(self, role: str) -> Optional[ComponentOutput]:
        elements = self._find_elements_by_role(self.component_output, role)
        return elements[0] if elements else None

    def _find_elements_by_role(self, output: ComponentOutput, role: str) -> List[ComponentOutput]:
        elements = []
        if output.role == role:
            elements.append(output)
        for child in output.children:
            elements.extend(self._find_elements_by_role(child, role))
        return elements

    def _find_elements_by_text(self, output: ComponentOutput, text: str) -> List[ComponentOutput]:
        elements = []
        if output.text == text:
            elements.append(output)
        for child in output.children:
            elements.extend(self._find_elements_by_text(child, text))
        return elements


def render(component: Component) -> Screen:
    return Screen(component.render())


class fireEvent:
    """用户事件的完整实现"""

    @staticmethod
    def click(element: ComponentOutput):
        if element.disabled:
            raise Exception("无法点击禁用的元素")
        if element.click_handler:
            element.click_handler()

    @staticmethod
    def change(element: ComponentOutput, value: str):
        if hasattr(element, 'value'):
            element.value = value


# 完整的测试示例
def run_complete_component_tests():
    """运行完整的组件测试套件"""

    def test_counter_component():
        counter = Component("Counter")
        screen = render(counter)

        # 初始状态
        status = screen.get_by_text("计数: 0")
        increment_btn = screen.get_by_text("增加")
        reset_btn = screen.get_by_text("重置")

        # 增加计数
        fireEvent.click(increment_btn)
        screen = render(counter)  # 重新渲染
        status = screen.get_by_text("计数: 1")

        # 再次增加
        increment_btn = screen.get_by_text("增加")
        fireEvent.click(increment_btn)
        screen = render(counter)
        status = screen.get_by_text("计数: 2")

        # 重置
        reset_btn = screen.get_by_text("重置")
        fireEvent.click(reset_btn)
        screen = render(counter)
        status = screen.get_by_text("计数: 0")

        print("✅ Counter 组件测试通过!")

    def test_toggle_component():
        toggle = Component("Toggle")
        screen = render(toggle)

        switch = screen.get_by_role("switch")
        toggle_btn = screen.get_by_text("切换")

        # 初始状态应该是关闭的
        assert not switch.checked

        # 切换到开启
        fireEvent.click(toggle_btn)
        screen = render(toggle)
        switch = screen.get_by_role("switch")
        assert switch.checked

        # 切换回关闭
        toggle_btn = screen.get_by_text("切换")
        fireEvent.click(toggle_btn)
        screen = render(toggle)
        switch = screen.get_by_role("switch")
        assert not switch.checked

        print("✅ Toggle 组件测试通过!")

    def test_user_card_component():
        user = {"name": "张三", "email": "zhangsan@example.com"}
        edit_called = {"called": False}

        def handle_edit():
            edit_called["called"] = True

        card = Component("UserCard", {"user": user, "onEdit": handle_edit})
        screen = render(card)

        # 验证用户信息显示
        name_element = screen.get_by_text("张三")
        email_element = screen.get_by_text("zhangsan@example.com")
        edit_btn = screen.get_by_text("编辑")

        assert name_element.role == "heading"
        assert email_element.role == "text"

        # 测试编辑功能
        fireEvent.click(edit_btn)
        assert edit_called["called"]

        print("✅ UserCard 组件测试通过!")

    test_counter_component()
    test_toggle_component()
    test_user_card_component()


if __name__ == "__main__":
    print("🚀 运行完整 React 组件测试解决方案...")
    run_complete_component_tests()
    print("🏁 所有组件测试完成!")