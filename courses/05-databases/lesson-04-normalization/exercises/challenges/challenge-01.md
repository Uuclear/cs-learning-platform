# 将混乱的数据表规范化到3NF

**难度**: ⭐⭐⭐

## 描述

你收到了一个来自客户的数据表，包含了员工、部门和项目信息。这个表结构混乱，存在大量数据冗余和各种异常。你的任务是分析这个表的函数依赖关系，并将其规范化到第三范式（3NF）。

原始表结构如下：

```
employee_projects (
    employee_id INTEGER,
    employee_name TEXT,
    employee_email TEXT,
    department_id INTEGER,
    department_name TEXT,
    department_manager TEXT,
    project_id INTEGER,
    project_name TEXT,
    project_budget REAL,
    hours_worked REAL,
    PRIMARY KEY (employee_id, project_id)
)
```

示例数据：
- (1, '张三', 'zhang@company.com', 101, 'IT部门', '李经理', 201, '网站开发', 50000.0, 40.0)
- (1, '张三', 'zhang@company.com', 101, 'IT部门', '李经理', 202, '移动应用', 30000.0, 20.0)
- (2, '李四', 'li@company.com', 101, 'IT部门', '李经理', 201, '网站开发', 50000.0, 35.0)
- (3, '王五', 'wang@company.com', 102, 'HR部门', '赵经理', 203, '招聘系统', 20000.0, 30.0)

## 要求

1. **分析函数依赖**：识别表中的所有函数依赖关系
2. **识别范式违反**：指出违反1NF、2NF、3NF的具体情况
3. **设计3NF模式**：创建规范化的表结构，满足3NF要求
4. **实现数据迁移**：编写SQL脚本将原始数据迁移到新表结构
5. **验证结果**：确保新设计消除了所有异常并保持数据完整性

## 提示

- 注意识别传递依赖：`department_id → department_name → department_manager`
- 考虑多对多关系：员工和项目之间是多对多关系
- 确保每个表都有适当的主键和外键约束
- 在设计时考虑实际业务需求，如查询员工项目工时、部门预算等
- 使用SQLite3进行实现和测试

## 评估标准

- ✅ 正确识别所有函数依赖
- ✅ 完全消除1NF、2NF、3NF违反
- ✅ 设计合理的表结构和关系
- ✅ 数据迁移脚本正确无误
- ✅ 查询性能和数据完整性得到保证