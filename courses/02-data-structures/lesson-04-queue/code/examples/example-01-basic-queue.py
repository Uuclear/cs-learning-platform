# 示例1: 队列的基本实现
# 使用Python列表模拟队列，展示FIFO（先进先出）原则

class Queue:
    """
    队列类 - 先进先出的数据结构
    就像排队买奶茶，先到的先拿到
    """
    def __init__(self):
        # 用列表存储队列元素
        self.items = []

    def enqueue(self, item):
        """
        入队操作：把元素加到队尾
        就像新来的人站到队伍最后面
        """
        self.items.append(item)
        print(f"  [入队] '{item}' → 队列: {self.items}")

    def dequeue(self):
        """
        出队操作：从队首取出并移除元素
        就像队伍最前面的人办完事离开
        如果队列为空，返回 None
        """
        if self.is_empty():
            print("  [警告] 队列为空，无法出队！")
            return None
        item = self.items.pop(0)  # 从列表开头移除
        print(f"  [出队] '{item}' ← 队列: {self.items}")
        return item

    def front(self):
        """
        查看队首元素（不移除）
        就像看看下一个叫几号
        """
        if self.is_empty():
            return None
        return self.items[0]

    def is_empty(self):
        """判断队列是否为空"""
        return len(self.items) == 0

    def size(self):
        """返回队列中的元素个数"""
        return len(self.items)

    def __str__(self):
        """打印队列状态"""
        if self.is_empty():
            return "队列: [空]"
        return f"队列: {self.items} (共{self.size()}人)"


def demonstrate_basic_queue():
    """演示队列的基本操作"""
    print("=== 队列基本操作演示 ===\n")

    # 创建一个队列（模拟银行叫号）
    queue = Queue()
    print(f"初始状态: {queue}\n")

    # 顾客来排队
    print("--- 顾客陆续到来 ---")
    queue.enqueue("顾客A")
    queue.enqueue("顾客B")
    queue.enqueue("顾客C")
    print(f"当前状态: {queue}\n")

    # 查看下一个
    print("--- 查看下一个 ---")
    print(f"  队首是: {queue.front()}\n")

    # 顾客办理业务（出队）
    print("--- 顾客办理业务 ---")
    queue.dequeue()
    queue.dequeue()
    print(f"当前状态: {queue}\n")

    # 又来了新顾客
    print("--- 新顾客到来 ---")
    queue.enqueue("顾客D")
    queue.enqueue("顾客E")
    print(f"最终状态: {queue}")


# 运行演示
if __name__ == "__main__":
    demonstrate_basic_queue()

# 预期输出:
# === 队列基本操作演示 ===
#
# 初始状态: 队列: [空]
#
# --- 顾客陆续到来 ---
#   [入队] '顾客A' → 队列: ['顾客A']
#   [入队] '顾客B' → 队列: ['顾客A', '顾客B']
#   [入队] '顾客C' → 队列: ['顾客A', '顾客B', '顾客C']
# 当前状态: 队列: ['顾客A', '顾客B', '顾客C'] (共3人)
#
# --- 查看下一个 ---
#   队首是: 顾客A
#
# --- 顾客办理业务 ---
#   [出队] '顾客A' ← 队列: ['顾客B', '顾客C']
#   [出队] '顾客B' ← 队列: ['顾客C']
# 当前状态: 队列: ['顾客C'] (共1人)
#
# --- 新顾客到来 ---
#   [入队] '顾客D' → 队列: ['顾客C', '顾客D']
#   [入队] '顾客E' → 队列: ['顾客C', '顾客D', '顾客E']
# 最终状态: 队列: ['顾客C', '顾客D', '顾客E'] (共3人)
