# 挑战 1：学生信息管理系统

## 目标
创建一个完整的学生信息管理系统，使用结构体来组织学生数据，并实现基本的管理功能。

## 要求

### 1. 结构体定义
定义以下结构体：
- `Course`：包含课程名称（50字符）、课程代码（10字符）、学分（整数）、成绩（浮点数）
- `Student`：包含学号（整数）、姓名（50字符）、邮箱（30字符）、课程数量（整数）、课程数组（最多10门课程）、GPA（浮点数）

### 2. 功能实现
实现以下函数：
- `void addStudent(Student *students, int *count, int id, const char *name, const char *email)` - 添加新学生
- `void addCourse(Student *student, const char *courseName, const char *courseCode, int credits, float grade)` - 为学生添加课程
- `float calculateGPA(Student *student)` - 计算学生的GPA（加权平均）
- `void printStudent(Student *student)` - 打印学生详细信息

### 3. 主程序
- 创建一个可以存储最多100个学生的数组
- 添加至少3个学生，每个学生至少有3门课程
- 计算并显示每个学生的GPA
- 按GPA从高到低排序并显示学生列表

## 提示
- 使用动态内存分配来管理学生数组（可选，但推荐）
- 注意字符串复制时的边界检查
- GPA计算公式：Σ(成绩 × 学分) / Σ(学分)
- 使用结构体指针来提高效率

## 扩展挑战（可选）
- 实现按学号或姓名搜索学生
- 添加删除学生功能
- 将学生数据保存到文件并从文件加载

## 评估标准
- 代码正确性（40%）
- 内存管理（20%）
- 代码结构和可读性（20%）
- 功能完整性（20%）