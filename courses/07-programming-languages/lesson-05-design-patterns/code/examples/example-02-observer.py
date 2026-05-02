"""
观察者模式示例 - 定义对象间的一对多依赖关系

观察者模式是一种行为型设计模式，它定义了对象之间的一对多依赖关系，
当一个对象的状态发生改变时，所有依赖于它的对象都会得到通知并自动更新。

在这个例子中，我们实现了一个简单的新闻订阅系统。
"""


class Subject:
    """被观察者（主题）基类"""

    def __init__(self):
        self._observers = []  # 存储所有观察者

    def attach(self, observer):
        """添加观察者"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        """移除观察者"""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, message):
        """通知所有观察者"""
        for observer in self._observers:
            observer.update(message)


class NewsPublisher(Subject):
    """新闻发布者（具体的被观察者）"""

    def __init__(self, name):
        super().__init__()
        self.name = name
        self._latest_news = ""

    def publish_news(self, news):
        """发布新闻"""
        self._latest_news = news
        print(f"\n【{self.name}】发布了新消息: {news}")
        # 通知所有订阅者
        self.notify(news)


class Observer:
    """观察者基类"""

    def __init__(self, name):
        self.name = name

    def update(self, message):
        """接收更新（需要子类实现）"""
        pass


class NewsSubscriber(Observer):
    """新闻订阅者（具体的观察者）"""

    def update(self, message):
        """接收到新闻更新"""
        print(f"  → {self.name} 收到了消息: {message}")


# 使用示例
if __name__ == "__main__":
    # 创建新闻发布者
    tech_news = NewsPublisher("科技前沿")
    sports_news = NewsPublisher("体育快讯")

    # 创建订阅者
    alice = NewsSubscriber("Alice")
    bob = NewsSubscriber("Bob")
    charlie = NewsSubscriber("Charlie")

    # 订阅新闻
    tech_news.attach(alice)
    tech_news.attach(bob)
    sports_news.attach(bob)
    sports_news.attach(charlie)

    # 发布新闻
    tech_news.publish_news("Python 3.12正式发布！")
    sports_news.publish_news("中国队赢得世界冠军！")

    # 取消订阅
    tech_news.detach(alice)
    tech_news.publish_news("新的AI框架震撼发布！")