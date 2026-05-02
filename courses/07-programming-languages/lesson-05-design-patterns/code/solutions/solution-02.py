"""
练习2解答：装饰器模式实现

装饰器模式是一种结构型设计模式，它允许动态地给对象添加额外的职责，
而不改变其结构。装饰器提供了比继承更灵活的扩展功能的替代方案。
"""


from abc import ABC, abstractmethod


class Beverage(ABC):
    """饮料抽象基类"""

    def __init__(self):
        self.description = "未知饮料"

    def get_description(self) -> str:
        return self.description

    @abstractmethod
    def cost(self) -> float:
        pass


class Coffee(Beverage):
    """咖啡类（具体组件）"""

    def __init__(self):
        super().__init__()
        self.description = "黑咖啡"

    def cost(self) -> float:
        return 15.0


class Tea(Beverage):
    """茶类（具体组件）"""

    def __init__(self):
        super().__init__()
        self.description = "绿茶"

    def cost(self) -> float:
        return 12.0


class CondimentDecorator(Beverage):
    """调料装饰器抽象基类"""

    def __init__(self, beverage: Beverage):
        super().__init__()
        self.beverage = beverage

    @abstractmethod
    def get_description(self) -> str:
        pass


class Milk(CondimentDecorator):
    """牛奶装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return self.beverage.get_description() + ", 牛奶"

    def cost(self) -> float:
        return self.beverage.cost() + 3.0


class Sugar(CondimentDecorator):
    """糖装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return self.beverage.get_description() + ", 糖"

    def cost(self) -> float:
        return self.beverage.cost() + 1.0


class WhippedCream(CondimentDecorator):
    """奶油装饰器"""

    def __init__(self, beverage: Beverage):
        super().__init__(beverage)

    def get_description(self) -> str:
        return self.beverage.get_description() + ", 奶油"

    def cost(self) -> float:
        return self.beverage.cost() + 4.0


# 测试代码
if __name__ == "__main__":
    # 创建基础饮料
    coffee = Coffee()
    print(f"{coffee.get_description()}: ¥{coffee.cost():.2f}")

    # 添加牛奶
    coffee_with_milk = Milk(coffee)
    print(f"{coffee_with_milk.get_description()}: ¥{coffee_with_milk.cost():.2f}")

    # 再添加糖和奶油
    fancy_coffee = Sugar(WhippedCream(coffee_with_milk))
    print(f"{fancy_coffee.get_description()}: ¥{fancy_coffee.cost():.2f}")

    print()

    # 茶的例子
    tea = Tea()
    sweet_tea = Sugar(tea)
    print(f"{sweet_tea.get_description()}: ¥{sweet_tea.cost():.2f}")