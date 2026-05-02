"""
策略模式示例 - 定义一系列算法，将它们封装起来并使它们可以互换

策略模式是一种行为型设计模式，它定义了一系列算法，并将每个算法封装起来，
使它们可以相互替换。策略模式让算法的变化独立于使用算法的客户。

在这个例子中，我们实现了一个支付系统，支持多种支付方式。
"""


from abc import ABC, abstractmethod


class PaymentStrategy(ABC):
    """支付策略抽象基类"""

    @abstractmethod
    def pay(self, amount: float) -> bool:
        """执行支付（需要子类实现）"""
        pass


class CreditCardPayment(PaymentStrategy):
    """信用卡支付策略"""

    def __init__(self, card_number: str, name: str):
        self.card_number = card_number
        self.name = name

    def pay(self, amount: float) -> bool:
        print(f"使用信用卡支付 ¥{amount:.2f}")
        print(f"卡号: **** **** **** {self.card_number[-4:]}")
        print(f"持卡人: {self.name}")
        # 模拟支付成功
        return True


class AlipayPayment(PaymentStrategy):
    """支付宝支付策略"""

    def __init__(self, account: str):
        self.account = account

    def pay(self, amount: float) -> bool:
        print(f"使用支付宝支付 ¥{amount:.2f}")
        print(f"支付宝账号: {self.account}")
        # 模拟支付成功
        return True


class WeChatPayment(PaymentStrategy):
    """微信支付策略"""

    def __init__(self, openid: str):
        self.openid = openid

    def pay(self, amount: float) -> bool:
        print(f"使用微信支付 ¥{amount:.2f}")
        print(f"微信ID: {self.openid[:8]}...")
        # 模拟支付成功
        return True


class ShoppingCart:
    """购物车类 - 使用策略模式"""

    def __init__(self):
        self.items = []
        self.payment_strategy = None

    def add_item(self, item: str, price: float):
        """添加商品到购物车"""
        self.items.append((item, price))

    def set_payment_strategy(self, strategy: PaymentStrategy):
        """设置支付策略"""
        self.payment_strategy = strategy

    def get_total(self) -> float:
        """计算总金额"""
        return sum(price for _, price in self.items)

    def checkout(self) -> bool:
        """结账"""
        if not self.payment_strategy:
            print("请先选择支付方式！")
            return False

        total = self.get_total()
        print(f"\n购物车总计: ¥{total:.2f}")
        print("开始支付...")

        # 使用当前策略执行支付
        return self.payment_strategy.pay(total)


# 使用示例
if __name__ == "__main__":
    # 创建购物车
    cart = ShoppingCart()
    cart.add_item("Python编程入门", 69.9)
    cart.add_item("设计模式实战", 89.5)
    cart.add_item("算法导论", 128.0)

    # 使用信用卡支付
    credit_card = CreditCardPayment("1234567890123456", "张三")
    cart.set_payment_strategy(credit_card)
    cart.checkout()

    print("\n" + "="*50 + "\n")

    # 使用支付宝支付
    alipay = AlipayPayment("zhangsan@example.com")
    cart.set_payment_strategy(alipay)
    cart.checkout()