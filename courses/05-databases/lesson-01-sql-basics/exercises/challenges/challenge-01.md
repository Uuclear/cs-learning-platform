# 挑战1：学生成绩管理系统

## 难度
⭐⭐

## 描述
设计一个学生成绩管理数据库，并编写SQL查询。

要求：
1. 创建学生表（students）：id, name, class
2. 创建成绩表（grades）：id, student_id, subject, score
3. 插入至少5名学生和对应的成绩数据
4. 查询每个学生的平均分，按平均分降序排列

## 提示
- 使用 `CREATE TABLE` 创建表
- 使用 `JOIN` 连接两个表
- 使用 `AVG()` 聚合函数和 `GROUP BY`
