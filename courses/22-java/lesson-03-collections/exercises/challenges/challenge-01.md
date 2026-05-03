# 挑战 1：学生成绩管理系统

## 背景
你正在为一所学校开发一个简单的学生成绩管理系统。系统需要支持以下功能：

## 要求
1. 创建一个 `Student` 类，包含学生姓名、学号和成绩列表
2. 实现一个 `GradeManager` 类，使用合适的集合类型来：
   - 存储所有学生信息（学号作为唯一标识）
   - 支持添加、删除、查找学生
   - 计算班级平均分
   - 找出成绩最高的前 N 名学生
   - 统计各分数段的学生人数（90-100, 80-89, 70-79, 60-69, <60）

## 提示
- 使用 `Map<String, Student>` 来存储学生，其中 String 是学号
- 使用 `List<Double>` 来存储每个学生的多门课程成绩
- 考虑使用 Java 8 的 Stream API 来简化统计操作
- 确保处理边界情况（如空列表、无效输入等）

## 扩展挑战（可选）
- 实现按学生姓名排序的功能
- 添加导出成绩单到 CSV 文件的功能
- 支持从 CSV 文件导入学生数据

## 测试用例
```java
// 创建 GradeManager
GradeManager manager = new GradeManager();

// 添加学生
manager.addStudent("001", "张三");
manager.addStudent("002", "李四");
manager.addStudent("003", "王五");

// 添加成绩
manager.addGrade("001", 85.5);
manager.addGrade("001", 92.0);
manager.addGrade("002", 78.0);
manager.addGrade("002", 88.5);
manager.addGrade("003", 95.0);
manager.addGrade("003", 87.5);

// 测试功能
System.out.println("班级平均分: " + manager.getClassAverage());
System.out.println("最高分学生: " + manager.getTopStudents(1));
System.out.println("分数段统计: " + manager.getGradeDistribution());
```