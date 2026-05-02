# 示例2: 循环队列的实现
# 使用固定大小数组 + 首尾指针，通过取模运算循环利用空间

class CircularQueue:
    """
    循环队列 - 像旋转木马一样循环利用空间
    核心思想：数组首尾相连，形成一个"环"
    """
    def __init__(self, capacity):
        # 固定大小的数组
        self.capacity = capacity
        self.queue = [None] * capacity
        # 队首指针和队尾指针
        self.front = 0    # 指向队首元素
        self.rear = 0     # 指向下一个可插入的位置
        self.size = 0     # 当前元素个数

    def enqueue(self, item):
        """入队：把元素放到 rear 位置"""
        if self.is_full():
            print(f"  [警告] 队列已满（容量{self.capacity}），无法入队！")
            return False

        self.queue[self.rear] = item
        # rear 指针向前移动，到末尾后回到开头（取模运算）
        self.rear = (self.rear + 1) % self.capacity
        self.size += 1
        print(f"  [入队] '{item}' → {self}")
        return True

    def dequeue(self):
        """出队：取出 front 位置的元素"""
        if self.is_empty():
            print("  [警告] 队列为空，无法出队！")
            return None

        item = self.queue[self.front]
        self.queue[self.front] = None  # 清空
        # front 指针向前移动，到末尾后回到开头
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        print(f"  [出队] '{item}' ← {self}")
        return item

    def is_full(self):
        """队列是否已满"""
        return self.size == self.capacity

    def is_empty(self):
        """队列是否为空"""
        return self.size == 0

    def front_item(self):
        """查看队首元素"""
        if self.is_empty():
            return None
        return self.queue[self.front]

    def __str__(self):
        return f"循环队列: {self.queue}, 大小: {self.size}/{self.capacity}"


def demonstrate_circular_queue():
    """演示循环队列的工作原理"""
    print("=== 循环队列演示 ===\n")

    # 创建一个容量为4的循环队列（模拟停车场）
    parking = CircularQueue(capacity=4)
    print(f"初始状态: {parking}\n")

    # 车辆陆续进入
    print("--- 车辆进入停车场 ---")
    parking.enqueue("宝马")
    parking.enqueue("奔驰")
    parking.enqueue("特斯拉")
    parking.enqueue("比亚迪")
    print(f"\n停车场满了: {parking}\n")

    # 尝试再停一辆
    print("--- 试图再停车 ---")
    parking.enqueue("五菱宏光")  # 满了！
    print()

    # 车辆离开
    print("--- 车辆离开 ---")
    parking.dequeue()  # 宝马走了
    parking.dequeue()  # 奔驰走了
    print(f"\n空出两个车位: {parking}\n")

    # 新车进来 - 注意看 rear 指针回到了开头！
    print("--- 新车停入（复用空位） ---")
    parking.enqueue("小鹏")
    parking.enqueue("蔚来")
    print(f"\n最终状态: {parking}")
    print("  ↑ 注意：小鹏和蔚来停在了数组开头的空位，空间被复用了！")


# 运行演示
if __name__ == "__main__":
    demonstrate_circular_queue()

# 预期输出:
# === 循环队列演示 ===
#
# 初始状态: 循环队列: [None, None, None, None], 大小: 0/4
#
# --- 车辆进入停车场 ---
#   [入队] '宝马' → 循环队列: ['宝马', None, None, None], 大小: 1/4
#   [入队] '奔驰' → 循环队列: ['宝马', '奔驰', None, None], 大小: 2/4
#   [入队] '特斯拉' → 循环队列: ['宝马', '奔驰', '特斯拉', None], 大小: 3/4
#   [入队] '比亚迪' → 循环队列: ['宝马', '奔驰', '特斯拉', '比亚迪'], 大小: 4/4
#
# 停车场满了: 循环队列: ['宝马', '奔驰', '特斯拉', '比亚迪'], 大小: 4/4
#
# --- 试图再停车 ---
#   [警告] 队列已满（容量4），无法入队！
#
# --- 车辆离开 ---
#   [出队] '宝马' ← 循环队列: [None, '奔驰', '特斯拉', '比亚迪'], 大小: 3/4
#   [出队] '奔驰' ← 循环队列: [None, None, '特斯拉', '比亚迪'], 大小: 2/4
#
# 空出两个车位: 循环队列: [None, None, '特斯拉', '比亚迪'], 大小: 2/4
#
# --- 新车停入（复用空位） ---
#   [入队] '小鹏' → 循环队列: ['小鹏', None, '特斯拉', '比亚迪'], 大小: 3/4
#   [入队] '蔚来' → 循环队列: ['小鹏', '蔚来', '特斯拉', '比亚迪'], 大小: 4/4
#
# 最终状态: 循环队列: ['小鹏', '蔚来', '特斯拉', '比亚迪'], 大小: 4/4
#   ↑ 注意：小鹏和蔚来停在了数组开头的空位，空间被复用了！
