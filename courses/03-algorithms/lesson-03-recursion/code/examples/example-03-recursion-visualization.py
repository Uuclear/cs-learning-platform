# 递归调用栈可视化
# 展示递归过程中调用栈的增长和收缩

def visualize_factorial(n, depth=0):
    """
    可视化阶乘递归的调用栈过程
    depth 参数用来缩进，展示递归深度
    """
    indent = "  " * depth  # 根据深度缩进
    
    # 打印进入信息
    print(f"{indent}>>> 进入 factorial({n})")
    
    # 基准情况
    if n <= 1:
        print(f"{indent}    基准情况: 返回 1")
        print(f"{indent}<<< 退出 factorial({n}), 返回 1")
        return 1
    
    # 递归调用
    print(f"{indent}    递归调用: {n} * factorial({n-1})")
    result = n * visualize_factorial(n - 1, depth + 1)
    
    # 打印返回信息
    print(f"{indent}    计算: {n} * {result // n} = {result}")
    print(f"{indent}<<< 退出 factorial({n}), 返回 {result}")
    
    return result


def visualize_call_tree(func_name, args_str, depth=0, level_info=None):
    """
    通用的递归调用树可视化工具
    以树形结构打印递归调用过程
    
    参数:
        func_name: 函数名（字符串）
        args_str: 参数描述（字符串）
        depth: 当前递归深度
        level_info: 每层需要展示的额外信息
    """
    if level_info is None:
        level_info = []
    
    indent = "  " * depth
    branch = "+" if depth == 0 else "|"
    prefix = f"{indent}{branch}-- "
    
    print(f"{prefix}[深度{depth}] 调用 {func_name}({args_str})")
    
    return indent, prefix


def demo_call_stack():
    """
    演示调用栈的完整生命周期
    """
    print("=== 递归调用栈可视化 ===\n")
    print("--- 计算 4! 的调用过程 ---\n")
    
    result = visualize_factorial(4)
    
    print(f"\n最终结果: 4! = {result}")
    
    print()
    print("--- 递归深度限制演示 ---")
    
    def factorial_simple(n):
        """简洁版阶乘（对比用）"""
        if n <= 1:
            return 1
        return n * factorial_simple(n - 1)
    
    try:
        # Python 默认递归深度限制大约 1000 层
        factorial_simple(2000)
    except RecursionError as e:
        print(f"  错误: {e}")
        print("  提示: Python 默认有递归深度限制，防止栈溢出")
    
    print()
    print("--- 查看当前递归深度限制 ---")
    import sys
    print(f"  Python 最大递归深度: {sys.getrecursionlimit()}")


if __name__ == "__main__":
    demo_call_stack()

# 预期输出:
# === 递归调用栈可视化 ===
#
# --- 计算 4! 的调用过程 ---
#
# >>> 进入 factorial(4)
#     递归调用: 4 * factorial(3)
#   >>> 进入 factorial(3)
#       递归调用: 3 * factorial(2)
#     >>> 进入 factorial(2)
#         递归调用: 2 * factorial(1)
#       >>> 进入 factorial(1)
#           基准情况: 返回 1
#       <<< 退出 factorial(1), 返回 1
#         计算: 2 * 1 = 2
#       <<< 退出 factorial(2), 返回 2
#       计算: 3 * 2 = 6
#     <<< 退出 factorial(3), 返回 6
#     计算: 4 * 6 = 24
#   <<< 退出 factorial(4), 返回 24
#
# 最终结果: 4! = 24
#
# --- 递归深度限制演示 ---
#   错误: maximum recursion depth exceeded
#   提示: Python 默认有递归深度限制，防止栈溢出
#
# --- 查看当前递归深度限制 ---
#   Python 最大递归深度: 1000
