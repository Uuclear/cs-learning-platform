# ============================================
# 练习1解答：数组求和与平均值
# 难度：⭐
# ============================================

def calculate_sum_and_average(arr):
    """
    计算数组的和与平均值
    
    参数:
        arr: 数字列表
    返回:
        (总和, 平均值) 元组
    """
    # 初始化总和为0
    total = 0
    
    # 遍历数组，累加每个元素
    for num in arr:
        total += num
    
    # 计算平均值（注意转换为浮点数）
    average = total / len(arr)
    
    return total, average


# 测试
if __name__ == "__main__":
    # 测试数据
    test_array = [10, 20, 30, 40, 50]
    
    print("=== 练习1：数组求和与平均值 ===")
    print(f"输入数组: {test_array}")
    
    total, average = calculate_sum_and_average(test_array)
    
    print(f"总和: {total}")
    print(f"平均值: {average}")
    
    # 验证
    assert total == 150, "总和计算错误"
    assert average == 30.0, "平均值计算错误"
    print("\n✅ 测试通过！")

# 输出:
# === 练习1：数组求和与平均值 ===
# 输入数组: [10, 20, 30, 40, 50]
# 总和: 150
# 平均值: 30.0
#
# ✅ 测试通过！
