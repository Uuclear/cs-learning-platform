# control_flow.py
# if-elif-else 条件语句
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "D"

print(f"分数 {score} 对应等级: {grade}")

# for 循环
fruits = ["苹果", "香蕉", "橙子", "葡萄"]
print("水果列表:")
for i, fruit in enumerate(fruits):
    print(f"{i+1}. {fruit}")

# while 循环
count = 3
print("倒计时:")
while count > 0:
    print(count)
    count -= 1
print("发射！")