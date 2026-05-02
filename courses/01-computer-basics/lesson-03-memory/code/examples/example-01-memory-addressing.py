# 内存寻址模拟
# 演示内存地址和值的概念

def demonstrate_memory_addressing():
    """
    模拟内存寻址过程
    展示变量在内存中的地址和值
    """
    print("=== 内存寻址模拟 ===\n")

    # 定义几个变量
    a = 42
    b = "Hello"
    c = [1, 2, 3]

    # 使用id()函数获取对象的内存地址（相当于门牌号）
    print(f"变量 a 的值: {a}")
    print(f"变量 a 的内存地址: {id(a)}")
    print(f"变量 a 的地址（十六进制）: {hex(id(a))}")
    print()

    print(f"变量 b 的值: {b}")
    print(f"变量 b 的内存地址: {hex(id(b))}")
    print()

    print(f"变量 c 的值: {c}")
    print(f"变量 c 的内存地址: {hex(id(c))}")
    print(f"列表 c 中第一个元素的地址: {hex(id(c[0]))}")
    print()

    # 演示引用（指针的概念）
    print("=== 引用（指针）演示 ===")
    d = a  # d 引用了 a 的值
    print(f"d = a 后，d 的值: {d}")
    print(f"d 的地址: {hex(id(d))}")
    print(f"注意：在Python中，小整数会被缓存复用，所以a和d可能指向同一地址")
    print()

    # 对于可变对象
    print("=== 可变对象的引用 ===")
    list1 = [1, 2, 3]
    list2 = list1  # list2 指向 list1 的同一个对象
    print(f"list1: {list1}, 地址: {hex(id(list1))}")
    print(f"list2: {list2}, 地址: {hex(id(list2))}")
    print(f"是否是同一个对象: {list1 is list2}")

    list2.append(4)  # 修改 list2
    print(f"\n修改 list2 后:")
    print(f"list1: {list1}")  # list1 也被改变了！
    print(f"list2: {list2}")


# 运行演示
if __name__ == "__main__":
    demonstrate_memory_addressing()

# 输出示例:
# === 内存寻址模拟 ===
#
# 变量 a 的值: 42
# 变量 a 的内存地址: 140735893619024
# 变量 a 的地址（十六进制）: 0x7ffeeb2a3d10
#
# 变量 b 的值: Hello
# 变量 b 的内存地址: 0x7ffeeb2a3d30
#
# 变量 c 的值: [1, 2, 3]
# 变量 c 的内存地址: 0x7ffeeb2a3d50
# 列表 c 中第一个元素的地址: 0x7ffeeb2a3d70
#
# === 引用（指针）演示 ===
# d = a 后，d 的值: 42
# d 的地址: 0x7ffeeb2a3d10
# ...
