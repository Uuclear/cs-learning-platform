# 单向链表实现
# 想象成小朋友手拉手：每个小朋友拿着自己的玩具（数据），同时牵着下一个小朋友的手（指针）


class Node:
    """链表节点：每个节点包含数据和指向下一个节点的指针"""
    def __init__(self, data):
        self.data = data      # 节点存储的数据
        self.next = None      # 指向下一个节点的指针，初始为空

    def __repr__(self):
        return f"Node({self.data})"


class SinglyLinkedList:
    """单向链表：只能从头往后走，不能回头"""
    def __init__(self):
        self.head = None      # 链表的头节点，初始为空
        self._size = 0        # 链表长度

    def is_empty(self):
        """判断链表是否为空"""
        return self.head is None

    def size(self):
        """返回链表长度"""
        return self._size

    def append(self, data):
        """在链表尾部添加元素"""
        new_node = Node(data)
        # 空链表的情况
        if self.head is None:
            self.head = new_node
        else:
            # 找到最后一个节点
            current = self.head
            while current.next is not None:
                current = current.next
            # 把新节点接在后面
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """在链表头部插入元素（这是链表的优势操作！）"""
        new_node = Node(data)
        new_node.next = self.head   # 新节点指向原来的头
        self.head = new_node        # 更新头指针
        self._size += 1

    def insert(self, index, data):
        """在指定位置插入元素"""
        if index < 0 or index > self._size:
            raise IndexError(f"插入位置越界: {index}, 链表长度: {self._size}")

        # 在头部插入，直接复用 prepend
        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        # 走到 index-1 的位置
        for _ in range(index - 1):
            current = current.next

        # 插入：新节点接替原来的链接关系
        new_node.next = current.next  # 新节点指向后面的节点
        current.next = new_node       # 前一个节点指向新节点
        self._size += 1

    def remove(self, data):
        """删除第一个匹配到的元素"""
        if self.head is None:
            raise ValueError("链表为空，无法删除")

        # 要删的是头节点
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next  # 跳过要删的节点
                self._size -= 1
                return True
            current = current.next

        raise ValueError(f"链表中没有找到元素: {data}")

    def search(self, data):
        """查找元素，返回索引；找不到返回-1"""
        current = self.head
        index = 0
        while current is not None:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def to_list(self):
        """将链表转换为Python列表（方便查看）"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __repr__(self):
        """打印链表的可读形式"""
        items = self.to_list()
        return " -> ".join(str(x) for x in items) + " -> None"


# ===== 测试代码 =====
if __name__ == "__main__":
    print("=" * 50)
    print("单向链表演示")
    print("=" * 50)

    # 创建空链表
    ll = SinglyLinkedList()
    print(f"\n1. 创建空链表: {ll}")
    print(f"   是否为空: {ll.is_empty()}, 长度: {ll.size()}")

    # 尾部追加元素
    print("\n2. 尾部追加 10, 20, 30:")
    ll.append(10)
    ll.append(20)
    ll.append(30)
    print(f"   {ll}")
    print(f"   长度: {ll.size()}")

    # 头部插入
    print("\n3. 头部插入 5:")
    ll.prepend(5)
    print(f"   {ll}")

    # 中间插入
    print("\n4. 在索引2处插入 15:")
    ll.insert(2, 15)
    print(f"   {ll}")

    # 查找元素
    print("\n5. 查找元素 30:")
    idx = ll.search(30)
    print(f"   30 的索引是: {idx}")
    print(f"   查找 99（不存在）: 索引 {ll.search(99)}")

    # 删除元素
    print("\n6. 删除元素 15:")
    ll.remove(15)
    print(f"   {ll}")

    print("\n7. 删除头部元素 5:")
    ll.remove(5)
    print(f"   {ll}")

    print(f"\n最终链表: {ll}")
    print(f"最终长度: {ll.size()}")

# 输出:
# ==================================================
# 单向链表演示
# ==================================================
#
# 1. 创建空链表:  -> None
#    是否为空: True, 长度: 0
#
# 2. 尾部追加 10, 20, 30:
#    10 -> 20 -> 30 -> None
#    长度: 3
#
# 3. 头部插入 5:
#    5 -> 10 -> 20 -> 30 -> None
#
# 4. 在索引2处插入 15:
#    5 -> 10 -> 15 -> 20 -> 30 -> None
#
# 5. 查找元素 30:
#    30 的索引是: 4
#    查找 99（不存在）: 索引 -1
#
# 6. 删除元素 15:
#    5 -> 10 -> 20 -> 30 -> None
#
# 7. 删除头部元素 5:
#    10 -> 20 -> 30 -> None
#
# 最终链表: 10 -> 20 -> 30 -> None
# 最终长度: 3
