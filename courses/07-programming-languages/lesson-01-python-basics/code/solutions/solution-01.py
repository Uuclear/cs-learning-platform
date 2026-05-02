# solution-01.py - 温度转换器
def celsius_to_fahrenheit(celsius):
    """
    将摄氏度转换为华氏度

    参数:
        celsius: 摄氏度数值

    返回:
        对应的华氏度数值

    异常:
        TypeError: 如果输入不是数字类型
    """
    # 输入验证
    if not isinstance(celsius, (int, float)):
        raise TypeError("输入必须是数字")

    # 转换公式: F = C × 9/5 + 32
    fahrenheit = celsius * 9/5 + 32
    return fahrenheit

# 测试示例
if __name__ == "__main__":
    try:
        print(f"0°C = {celsius_to_fahrenheit(0)}°F")
        print(f"100°C = {celsius_to_fahrenheit(100)}°F")
        print(f"-40°C = {celsius_to_fahrenheit(-40)}°F")

        # 测试错误输入
        print(celsius_to_fahrenheit("not a number"))
    except TypeError as e:
        print(f"错误: {e}")