# variables_types.py
# 定义不同类型的变量
name = "Alice"          # 字符串
age = 30                # 整数
height = 1.75           # 浮点数
is_programmer = True    # 布尔值

# 查看变量类型
print(f"姓名: {name}, 类型: {type(name)}")
print(f"年龄: {age}, 类型: {type(age)}")
print(f"身高: {height}, 类型: {type(height)}")
print(f"是程序员: {is_programmer}, 类型: {type(is_programmer)}")

# 动态类型演示
dynamic_var = 42        # 现在是整数
print(f"动态变量初始值: {dynamic_var}, 类型: {type(dynamic_var)}")

dynamic_var = "Hello"   # 现在变成字符串！
print(f"动态变量新值: {dynamic_var}, 类型: {type(dynamic_var)}")