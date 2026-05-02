# 示例1：堆的基本实现（最大堆）
# 用数组实现最大堆，包含插入、删除、上浮、下沉操作

class MaxHeap:
    """
    最大堆实现
    核心思想：每个节点的值都大于等于其子节点的值
    数组表示：父节点i的子节点在2*i+1和2*i+2
    """

    def __init__(self):
        # 用列表存储堆的元素，索引0是根节点
        self.heap = []

    def parent(self, i):
        """返回父节点的索引"""
        return (i - 1) // 2

    def left_child(self, i):
        """返回左子节点的索引"""
        return 2 * i + 1

    def right_child(self, i):
        """返回右子节点的索引"""
        return 2 * i + 2

    def has_parent(self, i):
        """判断是否有父节点"""
        return self.parent(i) >= 0

    def has_left_child(self, i):
        """判断是否有左子节点"""
        return self.left_child(i) < len(self.heap)

    def has_right_child(self, i):
        """判断是否有右子节点"""
        return self.right_child(i) < len(self.heap)

    def swap(self, i, j):
        """交换两个位置的元素"""
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def sift_up(self, i):
        """
        上浮操作：将新插入的元素向上调整到正确位置
        如果比父节点大，就和父节点交换，直到满足堆性质
        """
        while self.has_parent(i) and self.heap[i] > self.heap[self.parent(i)]:
            self.swap(i, self.parent(i))
            i = self.parent(i)

    def sift_down(self, i):
        """
        下沉操作：将根节点向下调整到正确位置
        如果比子节点小，就和较大的子节点交换
        """
        while self.has_left_child(i):
            # 先找出较大的子节点
            larger = self.left_child(i)
            if self.has_right_child(i) and self.heap[self.right_child(i)] > self.heap[larger]:
                larger = self.right_child(i)

            # 如果当前节点已经是最大的，就不用下沉了
            if self.heap[i] > self.heap[larger]:
                break

            # 否则和较大的子节点交换
            self.swap(i, larger)
            i = larger

    def insert(self, value):
        """
        插入元素：放到数组末尾，然后上浮到正确位置
        时间复杂度：O(log n)
        """
        self.heap.append(value)
        self.sift_up(len(self.heap) - 1)

    def extract_max(self):
        """
        删除并返回最大值（根节点）
        把最后一个元素移到根，然后下沉
        时间复杂度：O(log n)
        """
        if len(self.heap) == 0:
            return None

        if len(self.heap) == 1:
            return self.heap.pop()

        # 把最大值（根）保存下来
        max_value = self.heap[0]
        # 把最后一个元素移到根
        self.heap[0] = self.heap.pop()
        # 从根开始下沉
        self.sift_down(0)

        return max_value

    def peek(self):
        """查看最大值但不删除"""
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def size(self):
        """返回堆的大小"""
        return len(self.heap)

    def is_empty(self):
        """判断堆是否为空"""
        return len(self.heap) == 0

    def display(self):
        """打印堆的内容"""
        print(f"堆的内容: {self.heap}")


# ========== 测试代码 ==========
if __name__ == "__main__":
    print("=== 最大堆基本操作演示 ===\n")

    # 创建一个最大堆
    heap = MaxHeap()

    # 插入元素
    print("--- 插入元素 ---")
    values = [10, 20, 5, 30, 15, 25]
    for v in values:
        heap.insert(v)
        print(f"插入 {v} -> ", end="")
        heap.display()

    print()
    print("--- 查看最大值（不删除） ---")
    print(f"当前最大值: {heap.peek()}")
    heap.display()

    print()
    print("--- 依次删除最大值 ---")
    while not heap.is_empty():
        max_val = heap.extract_max()
        print(f"删除最大值 {max_val} -> ", end="")
        heap.display()

# 输出:
# === 最大堆基本操作演示 ===
#
# --- 插入元素 ---
# 插入 10 -> 堆的内容: [10]
# 插入 20 -> 堆的内容: [20, 10]
# 插入 5 -> 堆的内容: [20, 10, 5]
# 插入 30 -> 堆的内容: [30, 20, 5, 10]
# 插入 15 -> 堆的内容: [30, 20, 5, 10, 15]
# 插入 25 -> 堆的内容: [30, 20, 25, 10, 15, 5]
#
# --- 查看最大值（不删除） ---
# 当前最大值: 30
# 堆的内容: [30, 20, 25, 10, 15, 5]
#
# --- 依次删除最大值 ---
# 删除最大值 30 -> 堆的内容: [25, 20, 5, 10, 15]
# 删除最大值 25 -> 堆的内容: [20, 15, 5, 10]
# 删除最大值 20 -> 堆的内容: [15, 10, 5]
# 删除最大值 15 -> 堆的内容: [10, 5]
# 删除最大值 10 -> 堆的内容: [5]
# 删除最大值 5 -> 堆的内容: []
