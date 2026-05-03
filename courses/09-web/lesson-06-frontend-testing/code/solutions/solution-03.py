#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
解决方案 03: Cypress E2E 测试实现

这个文件提供了完整的 Cypress E2E 测试模拟实现，
包括页面导航、元素交互、网络 stubbing 和复杂用户流程。
"""

from typing import Dict, List, Optional, Callable
import time
import json


class Page:
    """网页页面的完整实现"""

    def __init__(self, url: str, initial_data: Dict = None):
        self.url = url
        self.data = initial_data or {}
        self.elements = self._load_page_elements(url)

    def _load_page_elements(self, url: str) -> Dict[str, 'Element']:
        elements = {}

        if "shop" in url:
            # 电商页面
            elements["product-list"] = Element("div", {"id": "product-list"})
            elements["cart-icon"] = Element("button", {"id": "cart-icon", "text": "🛒 购物车 (0)"})
            elements["search"] = Element("input", {"id": "search", "placeholder": "搜索商品..."})
        elif "product" in url:
            # 商品详情页面
            product_id = url.split("/")[-1]
            product = self.data.get("products", {}).get(product_id, {"name": "未知商品", "price": 0})
            elements["product-name"] = Element("h1", {"id": "product-name", "text": product["name"]})
            elements["product-price"] = Element("span", {"id": "product-price", "text": f"¥{product['price']}"})
            elements["add-to-cart"] = Element("button", {"id": "add-to-cart", "text": "加入购物车"})
            elements["back-link"] = Element("a", {"id": "back-link", "text": "返回商店", "href": "/shop"})
        elif "cart" in url:
            # 购物车页面
            cart_items = self.data.get("cart", [])
            elements["cart-items"] = Element("div", {"id": "cart-items"})
            elements["checkout"] = Element("button", {"id": "checkout", "text": "结账"})
            elements["empty-msg"] = Element("div", {"id": "empty-msg", "text": "购物车为空", "hidden": len(cart_items) > 0})

            # 动态创建购物车项目元素
            for i, item in enumerate(cart_items):
                elements[f"cart-item-{i}"] = Element("div", {
                    "class": "cart-item",
                    "text": f"{item['name']} - ¥{item['price']}"
                })
        else:
            # 首页
            elements["shop-link"] = Element("a", {"id": "shop-link", "text": "进入商店", "href": "/shop"})

        return elements

    def get_element(self, selector: str) -> 'Element':
        if selector.startswith("#"):
            element_id = selector[1:]
            if element_id in self.elements:
                return self.elements[element_id]
        elif selector.startswith("."):
            class_name = selector[1:]
            for element in self.elements.values():
                if element.attrs.get("class") == class_name:
                    return element
        elif selector.startswith("["):
            attr_part = selector[1:-1]
            if "=" in attr_part:
                attr_name, attr_value = attr_part.split("=", 1)
                attr_value = attr_value.strip('"')
                for element in self.elements.values():
                    if element.attrs.get(attr_name.strip()) == attr_value:
                        return element

        raise Exception(f"找不到元素: {selector}")

    def contains_text(self, text: str) -> 'Element':
        for element in self.elements.values():
            if element.text and text in element.text:
                return element
        raise Exception(f"找不到包含文本 '{text}' 的元素")


class Element:
    """HTML 元素的完整实现"""

    def __init__(self, tag: str, attrs: Dict):
        self.tag = tag
        self.attrs = attrs
        self.text = attrs.get("text", "")
        self.value = ""
        self.hidden = attrs.get("hidden", False)

    def click(self):
        if self.hidden:
            raise Exception("无法点击隐藏元素")
        print(f"🖱️ 点击: {self.text or self.tag}")

        if self.attrs.get("href"):
            return Page(self.attrs["href"])
        return None

    def type(self, text: str):
        if self.hidden:
            raise Exception("无法在隐藏元素中输入")
        self.value = text
        print(f"⌨️ 输入: '{text}'")

    def should(self, assertion: str, expected_value: str = None):
        if assertion == "be.visible":
            assert not self.hidden, "元素应该是可见的"
        elif assertion == "contain.text":
            assert expected_value in self.text, f"元素应该包含文本 '{expected_value}'"
        elif assertion == "have.value":
            assert self.value == expected_value, f"元素值应该是 '{expected_value}'"
        elif assertion == "exist":
            pass
        elif assertion == "be.hidden":
            assert self.hidden, "元素应该是隐藏的"
        else:
            raise Exception(f"不支持的断言: {assertion}")


class Cypress:
    """Cypress 框架的完整实现"""

    def __init__(self):
        self.current_page = None
        self.intercepted_requests = {}
        self.session_data = {}

    def visit(self, url: str):
        print(f"🌐 访问: {url}")
        # 使用会话数据初始化页面
        page_data = self.session_data.copy()
        self.current_page = Page(url, page_data)
        time.sleep(0.05)  # 模拟加载时间

    def get(self, selector: str) -> Element:
        return self.current_page.get_element(selector)

    def contains(self, text: str) -> Element:
        return self.current_page.contains_text(text)

    def intercept(self, url_pattern: str, mock_response: Dict = None):
        self.intercepted_requests[url_pattern] = mock_response
        print(f"📡 拦截 API: {url_pattern}")

    def wait(self, ms: int):
        time.sleep(ms / 1000)

    def task(self, task_name: str, *args):
        """模拟 Cypress 自定义任务"""
        if task_name == "clearCart":
            self.session_data["cart"] = []
            print("🗑️ 清空购物车")
        elif task_name == "addProductToCart":
            product_id = args[0]
            products = self.session_data.get("products", {})
            product = products.get(product_id)
            if product:
                cart = self.session_data.setdefault("cart", [])
                cart.append(product)
                print(f"➕ 添加商品到购物车: {product['name']}")


# 完整的 E2E 测试示例
def test_complete_shopping_flow():
    """测试完整的购物流程"""

    cy = Cypress()

    # 设置产品数据
    products = {
        "p1": {"name": "笔记本电脑", "price": 5999},
        "p2": {"name": "无线鼠标", "price": 199},
        "p3": {"name": "机械键盘", "price": 899}
    }
    cy.session_data["products"] = products

    # 开始测试
    cy.visit("/")

    # 进入商店
    shop_link = cy.get("#shop-link")
    shop_link.should("be.visible")
    shop_link.should("contain.text", "进入商店")

    cy.visit("/shop")

    # 验证商店页面
    cart_icon = cy.get("#cart-icon")
    cart_icon.should("contain.text", "购物车 (0)")

    # 搜索商品
    search_input = cy.get("#search")
    search_input.type("笔记本电脑")

    # 查看商品详情
    cy.visit("/product/p1")

    product_name = cy.get("#product-name")
    product_price = cy.get("#product-price")
    add_to_cart_btn = cy.get("#add-to-cart")

    product_name.should("contain.text", "笔记本电脑")
    product_price.should("contain.text", "¥5999")

    # 添加到购物车
    add_to_cart_btn.click()
    cy.task("addProductToCart", "p1")

    # 返回商店并添加第二个商品
    back_link = cy.get("#back-link")
    back_link.click()

    cy.visit("/product/p2")
    cy.get("#add-to-cart").click()
    cy.task("addProductToCart", "p2")

    # 查看购物车
    cy.visit("/cart")

    # 验证购物车内容
    cart_item_0 = cy.get("#cart-item-0")
    cart_item_1 = cy.get("#cart-item-1")
    checkout_btn = cy.get("#checkout")

    cart_item_0.should("contain.text", "笔记本电脑")
    cart_item_1.should("contain.text", "无线鼠标")
    checkout_btn.should("be.visible")

    # 结账
    checkout_btn.click()
    print("✅ 完整购物流程 E2E 测试通过!")


def test_empty_cart_scenario():
    """测试空购物车场景"""

    cy = Cypress()
    cy.task("clearCart")  # 确保购物车为空

    cy.visit("/cart")

    empty_msg = cy.get("#empty-msg")
    empty_msg.should("be.visible")
    empty_msg.should("contain.text", "购物车为空")

    print("✅ 空购物车场景 E2E 测试通过!")


if __name__ == "__main__":
    print("🚀 运行完整 Cypress E2E 测试解决方案...")
    test_complete_shopping_flow()
    test_empty_cart_scenario()
    print("🏁 所有 E2E 测试完成!")