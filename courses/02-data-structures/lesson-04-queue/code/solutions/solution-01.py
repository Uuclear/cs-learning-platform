# 练习1解答: 实现链表队列
# 用链表实现一个队列，确保 enqueue 和 dequeue 都是 O(1) 时间复杂度

class Node:
    """链表节点"""
    def __init__(self, val):
        self.val = val
        self.next = None


class LinkedListQueue:
    """
    链表实现的队列 - O(1) 入队和出队
    用 head 指向队首，tail 指向队尾
    """
    def __init__(self):
        self.head = None  # 队首指针
        self.tail = None  # 队尾指针
        self._size = 0    # 元素个数

    def enqueue(self, item):
        """
        入队：在链表尾部添加节点，O(1)
        """
        new_node = Node(item)
        if self.is_empty():
            # 队列为空，head 和 tail 都指向新节点
            self.head = new_node
            self.tail = new_node
        else:
            # 把新节点接在 tail 后面
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1
        print(f"  [入队] '{item}' → {self}")

    def dequeue(self):
        """
        出队：从链表头部移除节点，O(1)
        """
        if self.is_empty():
            print("  [警告] 队列为空！")
            return None
        item = self.head.val
        self.head = self.head.next
        # 如果出队后为空，tail 也要置为 None
        if self.head is None:
            self.tail = None
        self._size -= 1
        print(f"  [出队] '{item}' ← {self}")
        return item

    def front(self):
        """查看队首元素"""
        if self.is_empty():
            return None
        return self.head.val

    def is_empty(self):
        """判断队列是否为空"""
        return self.head is None

    def size(self):
        """返回元素个数"""
        return self._size

    def __str__(self):
        """打印队列内容"""
        items = []
        curr = self.head
        while curr:
            items.append(str(curr.val))
            curr = curr.next
        if not items:
            return "链表队列: [空]"
        return f"链表队列: [{' ← '.join(items)}] (共{self._size}个)"


def test_linked_list_queue():
    """测试链表队列"""
    print("=== 链表队列测试 ===\n")

    q = LinkedListQueue()
    print(f"初始: {q}\n")

    # 入队
    print("--- 入队测试 ---")
    q.enqueue(10)
    q.enqueue(20)
    q.enqueue(30)
    print()

    # 出队
    print("--- 出队测试 ---")
    q.dequeue()  # 应该移除 10
    q.dequeue()  # 应该移除 20
    print()

    # 查看队首
    print(f"当前队首: {q.front()}")
    print()

    # 全部出队
    print("--- 全部出队 ---")
    q.dequeue()  # 移除 30
    q.dequeue()  # 空队列警告
    print()

    print("链表队列优势：入队和出队都是 O(1)，不受数据量影响！")


if __name__ == "__main__":
    test_linked_list_queue()

# 预期输出:
# === 链表队列测试 ===
#
# 初始: 链表队列: [空]
#
# --- 入队测试 ---
#   [入队] '10' → 链表队列: [10] (共1个)
#   [入队] '20' → 链表队列: [10 ← 20] (共2个)
#   [入队] '30' → 链表队列: [10 ← 20 ← 30] (共3个)
#
# --- 出队测试 ---
#   [出队] '10' ← 链表队列: [20 ← 30] (共2个)
#   [出队] '20' ← 链表队列: [30] (共1个)
#
# 当前队首: 30
#
# --- 全部出队 ---
#   [出队] '30' ← 链表队列: [空]
#   [警告] 队列为空！
#
# 链表队列优势：入队和出队都是 O(1)，不受数据量影响！
