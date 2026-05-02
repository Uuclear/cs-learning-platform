# ============================================
# 练习2解答：找出数组中的最大值和最小值
# 难度：⭐⭐
# ============================================

def find_max_min(arr):
    """
    找出数组中的最大值、最小值及其索引
    
    参数:
        arr: 数字列表
    返回:
        (最大值, 最大值的索引, 最小值, 最小值的索引) 元组
    """
    # 处理空数组的情况
    if not arr:
        return None, None, None, None
    
    # 初始化最大值和最小值为第一个元素
    max_val = arr[0]
    min_val = arr[0]
    max_idx = 0
    min_idx = 0
    
    # 从第二个元素开始遍历（索引1）
    for i in range(1, len(arr)):
        # 如果当前元素比最大值还大，更新最大值
        if arr[i] > max_val:
            max_val = arr[i]
            max_idx = i
        
        # 如果当前元素比最小值还小，更新最小值
        if arr[i] < min_val:
            min_val = arr[i]
            min_idx = i
    
    return max_val, max_idx, min_val, min_idx


# 测试
if __name__ == "__main__":
    # 测试数据
    test_array = [45, 12, 78, 23, 67, 89, 34]
    
    print("=== 练习2：找出最大值和最小值 ===")
    print(f"输入数组: {test_array}")
    
    max_val, max_idx, min_val, min_idx = find_max_min(test_array)
    
    print(f"最大值: {max_val} (索引{max_idx})")
    print(f"最小值: {min_val} (索引{min_idx})")
    
    # 验证
    assert max_val == 89 and max_idx == 5, "最大值或索引错误"
    assert min_val == 12 and min_idx == 1, "最小值或索引错误"
    print("\n✅ 测试通过！")
    
    # 额外测试：只有一个元素的数组
    print("\n=== 额外测试：单元素数组 ===")
    single = [42]
    result = find_max_min(single)
    print(f"单元素数组 [42]: 最大值={result[0]}, 最小值={result[2]}")
    assert result[0] == result[2] == 42, "单元素数组处理错误"
    print("✅ 单元素测试通过！")

# 输出:
# === 练习2：找出最大值和最小值 ===
# 输入数组: [45, 12, 78, 23, 67, 89, 34]
# 最大值: 89 (索引5)
# 最小值: 12 (索引1)
#
# ✅ 测试通过！
#
# === 额外测试：单元素数组 ===
# 单元素数组 [42]: 最大值=42, 最小值=42
# ✅ 单元素测试通过！
