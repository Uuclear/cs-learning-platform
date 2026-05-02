"""
练习1解答：工厂模式实现

工厂模式是一种创建型设计模式，它提供了一种创建对象的最佳方式，
而无需指定要创建的对象的具体类。
"""


from abc import ABC, abstractmethod


class Animal(ABC):
    """动物抽象基类"""

    @abstractmethod
    def speak(self):
        pass


class Dog(Animal):
    """狗类"""

    def speak(self):
        return "汪汪！"


class Cat(Animal):
    """猫类"""

    def speak(self):
        return "喵喵！"


class Duck(Animal):
    """鸭子类"""

    def speak(self):
        return "嘎嘎！"


class AnimalFactory:
    """动物工厂类"""

    @staticmethod
    def create_animal(animal_type: str) -> Animal:
        """根据类型创建动物实例"""
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        elif animal_type.lower() == "duck":
            return Duck()
        else:
            raise ValueError(f"不支持的动物类型: {animal_type}")


# 测试代码
if __name__ == "__main__":
    # 创建不同类型的动物
    animals = ["dog", "cat", "duck"]

    for animal_type in animals:
        animal = AnimalFactory.create_animal(animal_type)
        print(f"{animal_type.capitalize()}: {animal.speak()}")