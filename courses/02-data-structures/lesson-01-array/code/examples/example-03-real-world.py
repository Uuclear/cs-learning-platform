# ============================================
# 示例3：数组的实际应用场景
# 看看数组在生活中是怎么用的
# ============================================

# 场景1：学生成绩管理系统
print("=== 场景1：学生成绩管理 ===")
scores = [85, 92, 78, 96, 88, 73, 91]
print(f"学生成绩: {scores}")

# 计算平均分
total = 0
for score in scores:
    total += score
average = total / len(scores)
print(f"班级平均分: {average:.1f}")

# 找出最高分和最低分
max_score = scores[0]
min_score = scores[0]
for score in scores:
    if score > max_score:
        max_score = score
    if score < min_score:
        min_score = score
print(f"最高分: {max_score}, 最低分: {min_score}")
print()

# 场景2：实现一个简单的栈（Stack）
print("=== 场景2：用数组实现栈 ===")

class Stack:
    """
    栈：后进先出（LIFO）
    就像一叠盘子，最后放的先拿
    """
    def __init__(self):
        self.items = []  # 用数组存储
    
    def push(self, item):
        """入栈：放在最上面"""
        self.items.append(item)
        print(f"  入栈: {item}，当前栈: {self.items}")
    
    def pop(self):
        """出栈：拿走最上面的"""
        if not self.items:
            return None
        item = self.items.pop()
        print(f"  出栈: {item}，当前栈: {self.items}")
        return item

# 测试栈
stack = Stack()
stack.push("书本A")
stack.push("书本B")
stack.push("书本C")
print("开始出栈...")
stack.pop()
stack.pop()
print()

# 场景3：图片的像素存储
print("=== 场景3：图片像素存储 ===")
print("一张 3×3 的简单图片（数字代表灰度值）：")

# 用二维数组表示图片
image = [
    [255, 128, 0],    # 第一行：白、灰、黑
    [128, 255, 128],  # 第二行
    [0, 128, 255]     # 第三行
]

for row in image:
    print(row)

print("\n获取正中间的像素值:")
print(f"image[1][1] = {image[1][1]}  (白色)")

# 输出:
# === 场景1：学生成绩管理 ===
# 学生成绩: [85, 92, 78, 96, 88, 73, 91]
# 班级平均分: 86.1
# 最高分: 96, 最低分: 73
#
# === 场景2：用数组实现栈 ===
#   入栈: 书本A，当前栈: ['书本A']
#   入栈: 书本B，当前栈: ['书本A', '书本B']
#   入栈: 书本C，当前栈: ['书本A', '书本B', '书本C']
# 开始出栈...
#   出栈: 书本C，当前栈: ['书本A', '书本B']
#   出栈: 书本B，当前栈: ['书本A']
#
# === 场景3：图片像素存储 ===
# 一张 3×3 的简单图片（数字代表灰度值）：
# [255, 128, 0]
# [128, 255, 128]
# [0, 128, 255]
#
# 获取正中间的像素值:
# image[1][1] = 255  (白色)
