# solution-03.py - 列表处理器
def analyze_numbers(numbers):
    """
    分析数字列表并返回统计信息

    参数:
        numbers: 数字列表

    返回:
        包含统计信息的字典

    异常:
        ValueError: 如果列表为空或包含非数字元素
    """
    # 输入验证
    if not numbers:
        raise ValueError("列表不能为空")

    # 检查所有元素是否为数字
    for num in numbers:
        if not isinstance(num, (int, float)):
            raise ValueError(f"列表中包含非数字元素: {num}")

    # 计算统计信息
    total = sum(numbers)
    average = total / len(numbers)
    maximum = max(numbers)
    minimum = min(numbers)

    # 计算中位数
    sorted_numbers = sorted(numbers)
    n = len(sorted_numbers)
    if n % 2 == 0:
        # 偶数个元素，取中间两个的平均值
        median = (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
    else:
        # 奇数个元素，取中间的元素
        median = sorted_numbers[n//2]

    return {
        "sum": total,
        "average": average,
        "max": maximum,
        "min": minimum,
        "median": median,
        "count": len(numbers)
    }

# 测试示例
if __name__ == "__main__":
    try:
        # 测试奇数长度列表
        odd_list = [1, 3, 5, 7, 9]
        result1 = analyze_numbers(odd_list)
        print(f"奇数列表 {odd_list} 的统计信息:")
        for key, value in result1.items():
            print(f"  {key}: {value}")

        print()

        # 测试偶数长度列表
        even_list = [2, 4, 6, 8]
        result2 = analyze_numbers(even_list)
        print(f"偶数列表 {even_list} 的统计信息:")
        for key, value in result2.items():
            print(f"  {key}: {value}")

        # 测试空列表
        analyze_numbers([])
    except ValueError as e:
        print(f"错误: {e}")