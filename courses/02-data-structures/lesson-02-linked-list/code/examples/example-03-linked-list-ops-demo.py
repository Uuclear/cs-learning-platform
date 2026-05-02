# 链表操作综合演示 + 链表 vs 数组对比
# 用实际性能对比展示：为什么链表和数组各有所长


import time


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def size(self):
        return self._size

    def append(self, data):
        """在尾部添加元素"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def prepend(self, data):
        """在头部插入（O(1)操作）"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at(self, index, data):
        """在指定位置插入"""
        if index < 0 or index > self._size:
            raise IndexError("索引越界")
        if index == 0:
            self.prepend(data)
            return
        new_node = Node(data)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def to_list(self):
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result


def compare_head_insert(n):
    """对比：在头部连续插入n个元素"""
    # 链表：每次O(1)，总O(n)
    ll = SinglyLinkedList()
    start = time.perf_counter()
    for i in range(n):
        ll.prepend(i)
    ll_time = time.perf_counter() - start

    # 数组：每次插入到开头O(n)，总O(n^2)
    arr = []
    start = time.perf_counter()
    for i in range(n):
        arr.insert(0, i)
    arr_time = time.perf_counter() - start

    return ll_time, arr_time


def compare_tail_insert(n):
    """对比：在尾部连续追加n个元素"""
    # 链表：每次需要遍历到尾，O(n)，总O(n^2)
    ll = SinglyLinkedList()
    start = time.perf_counter()
    for i in range(n):
        ll.append(i)
    ll_time = time.perf_counter() - start

    # 数组：append是摊还O(1)，总O(n)
    arr = []
    start = time.perf_counter()
    for i in range(n):
        arr.append(i)
    arr_time = time.perf_counter() - start

    return ll_time, arr_time


def compare_random_access(n, k):
    """对比：随机访问第k个元素"""
    # 构建数据
    ll = SinglyLinkedList()
    arr = []
    for i in range(n):
        ll.append(i)
        arr.append(i)

    # 链表：需要从头走k步，O(k)
    start = time.perf_counter()
    current = ll.head
    for _ in range(k):
        current = current.next
    ll_result = current.data
    ll_time = time.perf_counter() - start

    # 数组：直接索引，O(1)
    start = time.perf_counter()
    arr_result = arr[k]
    arr_time = time.perf_counter() - start

    return ll_time, arr_time, ll_result, arr_result


# ===== 主程序 =====
if __name__ == "__main__":
    print("=" * 55)
    print("链表 vs 数组：性能对比实验")
    print("=" * 55)

    # 实验1：头部插入
    print("\n🔬 实验1：在头部连续插入10000个元素")
    print("-" * 40)
    ll_t, arr_t = compare_head_insert(10000)
    print(f"  链表耗时: {ll_t*1000:.2f} 毫秒")
    print(f"  数组耗时: {arr_t*1000:.2f} 毫秒")
    print(f"  链表快 {arr_t/ll_t:.0f} 倍！")
    print("  💡 链表头部插入是O(1)，数组需要移动所有元素O(n)")

    # 实验2：尾部插入
    print("\n🔬 实验2：在尾部连续追加10000个元素")
    print("-" * 40)
    ll_t, arr_t = compare_tail_insert(10000)
    print(f"  链表耗时: {ll_t*1000:.2f} 毫秒")
    print(f"  数组耗时: {arr_t*1000:.2f} 毫秒")
    print(f"  数组快 {ll_t/arr_t:.0f} 倍！")
    print("  💡 数组append是摊还O(1)，链表需要遍历到尾O(n)")

    # 实验3：随机访问
    print("\n🔬 实验3：随机访问第5000个元素（共10000个）")
    print("-" * 40)
    ll_t, arr_t, ll_r, arr_r = compare_random_access(10000, 5000)
    print(f"  链表耗时: {ll_t*1000:.2f} 毫秒")
    print(f"  数组耗时: {arr_t*1000:.2f} 毫秒")
    print(f"  数组快得多！（链表需逐步遍历，数组直接寻址）")

    # 总结
    print("\n" + "=" * 55)
    print("📊 总结：谁更适合什么场景？")
    print("=" * 55)
    print("""
  场景                赢家      原因
  ────────────────────────────────────────────
  频繁在中间插入/删除    链表     O(1) vs O(n) 移动
  频繁随机访问          数组     O(1) vs O(n) 遍历
  尾部频繁追加          数组     摊还O(1)，内存连续
  头部频繁插入          链表     O(1)，不需要搬数据
  内存占用            数组     无额外指针开销
""")

# 输出（时间因机器而异，趋势一致）:
# =======================================================
# 链表 vs 数组：性能对比实验
# =======================================================
#
# 🔬 实验1：在头部连续插入10000个元素
# ----------------------------------------
#   链表耗时: X.XX 毫秒
#   数组耗时: XX.XX 毫秒
#   链表快 X 倍！
#   💡 链表头部插入是O(1)，数组需要移动所有元素O(n)
#
# 🔬 实验2：在尾部连续追加10000个元素
# ----------------------------------------
#   链表耗时: XX.XX 毫秒
#   数组耗时: X.XX 毫秒
#   数组快 X 倍！
#   💡 数组append是摊还O(1)，链表需要遍历到尾O(n)
#
# 🔬 实验3：随机访问第5000个元素（共10000个）
# ----------------------------------------
#   链表耗时: X.XX 毫秒
#   数组耗时: 0.XX 毫秒
#   数组快得多！（链表需逐步遍历，数组直接寻址）
#
# =======================================================
# 📊 总结：谁更适合什么场景？
# =======================================================
#
#   场景                赢家      原因
#   ────────────────────────────────────────────
#   频繁在中间插入/删除    链表     O(1) vs O(n) 移动
#   频繁随机访问          数组     O(1) vs O(n) 遍历
#   尾部频繁追加          数组     摊还O(1)，内存连续
#   头部频繁插入          链表     O(1)，不需要搬数据
#   内存占用            数组     无额外指针开销
