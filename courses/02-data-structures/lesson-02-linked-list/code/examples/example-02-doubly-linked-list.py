# 双向链表实现
# 每个小朋友不仅牵着后面的手，还牵着前面的手
# 好处：可以从后往前走！


class DoublyNode:
    """双向链表节点：有前指针和后指针"""
    def __init__(self, data):
        self.data = data       # 数据
        self.next = None       # 后继（指向下一个）
        self.prev = None       # 前驱（指向上一个）

    def __repr__(self):
        return f"DNode({self.data})"


class DoublyLinkedList:
    """双向链表：可以从头走到底，也可以从尾走回头"""
    def __init__(self):
        self.head = None       # 头节点
        self.tail = None       # 尾节点（双向链表的特色！）
        self._size = 0

    def is_empty(self):
        return self.head is None

    def size(self):
        return self._size

    def append(self, data):
        """在尾部添加元素（双向链表的优势操作）"""
        new_node = DoublyNode(data)
        if self.head is None:
            # 空链表，头尾都指向新节点
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail     # 新节点的前驱指向原来的尾
            self.tail.next = new_node     # 原来的尾的后继指向新节点
            self.tail = new_node          # 更新尾指针
        self._size += 1

    def prepend(self, data):
        """在头部插入元素"""
        new_node = DoublyNode(data)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head     # 新节点的后继指向原来的头
            self.head.prev = new_node     # 原来的头的前驱指向新节点
            self.head = new_node          # 更新头指针
        self._size += 1

    def remove(self, data):
        """删除第一个匹配到的元素"""
        if self.head is None:
            raise ValueError("链表为空，无法删除")

        current = self.head
        while current is not None:
            if current.data == data:
                # 找到要删除的节点
                if current.prev is not None:
                    current.prev.next = current.next
                else:
                    # 删的是头节点
                    self.head = current.next

                if current.next is not None:
                    current.next.prev = current.prev
                else:
                    # 删的是尾节点
                    self.tail = current.prev

                self._size -= 1
                return True

            current = current.next

        raise ValueError(f"链表中没有找到元素: {data}")

    def forward(self):
        """从头到尾遍历"""
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def backward(self):
        """从尾到头遍历（双向链表的独门绝技！）"""
        result = []
        current = self.tail
        while current is not None:
            result.append(current.data)
            current = current.prev
        return result

    def __repr__(self):
        forward_items = self.forward()
        return " <-> ".join(str(x) for x in forward_items) + " <-> None"


# ===== 测试代码 =====
if __name__ == "__main__":
    print("=" * 50)
    print("双向链表演示")
    print("=" * 50)

    dll = DoublyLinkedList()

    # 尾部追加
    print("\n1. 尾部追加 A, B, C, D:")
    dll.append("A")
    dll.append("B")
    dll.append("C")
    dll.append("D")
    print(f"   {dll}")
    print(f"   头: {dll.head.data}, 尾: {dll.tail.data}")

    # 头部插入
    print("\n2. 头部插入 'START':")
    dll.prepend("START")
    print(f"   {dll}")

    # 正向遍历
    print("\n3. 正向遍历:")
    print(f"   {dll.forward()}")

    # 反向遍历（双向链表的杀手级功能！）
    print("\n4. 反向遍历（单向链表做不到！）:")
    print(f"   {dll.backward()}")

    # 删除元素
    print("\n5. 删除元素 'C':")
    dll.remove("C")
    print(f"   {dll}")
    print(f"   反向: {dll.backward()}")

    print(f"\n最终长度: {dll.size()}")

# 输出:
# ==================================================
# 双向链表演示
# ==================================================
#
# 1. 尾部追加 A, B, C, D:
#    A <-> B <-> C <-> D <-> None
#    头: A, 尾: D
#
# 2. 头部插入 'START':
#    START <-> A <-> B <-> C <-> D <-> None
#
# 3. 正向遍历:
#    ['START', 'A', 'B', 'C', 'D']
#
# 4. 反向遍历（单向链表做不到！）:
#    ['D', 'C', 'B', 'A', 'START']
#
# 5. 删除元素 'C':
#    START <-> A <-> B <-> D <-> None
#    反向: ['D', 'B', 'A', 'START']
#
# 最终长度: 4
