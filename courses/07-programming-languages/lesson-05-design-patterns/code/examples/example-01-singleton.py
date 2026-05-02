"""
单例模式示例 - 确保一个类只有一个实例

单例模式是一种创建型设计模式，它保证一个类只有一个实例，
并提供一个全局访问点来访问该实例。

在Python中，我们可以通过重写__new__方法来实现单例模式。
"""


class Singleton:
    """单例类的实现"""
    _instance = None  # 类变量，存储唯一的实例

    def __new__(cls):
        # 如果实例不存在，则创建新实例
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # 初始化实例属性
            cls._instance.value = None
        return cls._instance


# 使用示例
if __name__ == "__main__":
    # 创建两个"实例"
    singleton1 = Singleton()
    singleton2 = Singleton()

    # 设置第一个实例的值
    singleton1.value = "我是单例实例的值"

    # 检查两个实例是否相同
    print(f"singleton1 的值: {singleton1.value}")
    print(f"singleton2 的值: {singleton2.value}")
    print(f"singleton1 is singleton2: {singleton1 is singleton2}")
    print(f"singleton1 == singleton2: {singleton1 == singleton2}")