# 挑战 1：学生成绩管理系统

## 要求

使用 STL 算法实现一个学生成绩管理系统，包含以下功能：

1. 定义一个 `Student` 结构体，包含姓名、分数、等级（A/B/C/D/F）字段
2. 使用 `std::sort` 按分数降序排列
3. 使用 `std::transform` 为每个学生计算等级（A: ≥90, B: ≥80, C: ≥70, D: ≥60, F: <60）
4. 使用 `std::find_if` 查找第一个不及格的学生
5. 使用 `std::count_if` 统计各等级的人数

## 提示

- 使用 Lambda 表达式定义比较函数和变换函数
- 考虑使用 `std::map` 或 `std::unordered_map` 来统计各等级人数
- 尝试使用 `std::partition` 将及格和不及格的学生分开

## 解答

参考 `code/solutions/solution-03.cpp` 中的综合实战代码，其中展示了类似的数据处理管道。
