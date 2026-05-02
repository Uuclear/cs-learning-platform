# ============================================
# 示例1：哈希表的基本操作演示
# 看看Python的dict（就是哈希表）有多好用
# ============================================

# 创建哈希表（字典）
student_scores = {
    "小明": 95,
    "小红": 88,
    "小刚": 72,
    "小丽": 99
}

print("=== 创建哈希表 ===")
print(f"学生成绩: {student_scores}")
print()

# 1. 查找 - O(1)，瞬间定位！
print("=== 查找元素 ===")
print(f"小明的成绩: {student_scores['小明']}")
print(f"小丽的成绩: {student_scores['小丽']}")
print()

# 2. 插入/更新 - O(1)，直接添加
print("=== 插入/更新元素 ===")
student_scores["小强"] = 85  # 新增
print(f"添加小强后: {student_scores}")

student_scores["小明"] = 98  # 更新已有键
print(f"小明考了98分: {student_scores}")
print()

# 3. 删除 - O(1)，说删就删
print("=== 删除元素 ===")
del student_scores["小刚"]
print(f"删除小刚后: {student_scores}")
print()

# 4. 检查键是否存在
print("=== 检查键是否存在 ===")
print(f"'小红'在表中吗？ {'小红' in student_scores}")
print(f"'小刚'在表中吗？ {'小刚' in student_scores}")
print()

# 5. 遍历
print("=== 遍历哈希表 ===")
for name, score in student_scores.items():
    print(f"  {name}: {score}分")
