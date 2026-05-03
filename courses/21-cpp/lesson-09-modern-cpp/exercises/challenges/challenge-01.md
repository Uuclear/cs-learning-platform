# 挑战 1：现代 C++ 数据处理

## 背景
你正在开发一个学生成绩管理系统，需要处理大量的学生数据。传统的 C++ 方式代码冗长且容易出错。

## 任务
使用现代 C++ 特性重构以下代码：

```cpp
// 传统代码 - 需要重构
#include <iostream>
#include <vector>
#include <map>
#include <string>

struct Student {
    std::string name;
    std::map<std::string, double> grades;
};

double calculateAverage(const std::map<std::string, double>& grades) {
    if (grades.empty()) return 0.0;
    
    double sum = 0.0;
    for (std::map<std::string, double>::const_iterator it = grades.begin(); 
         it != grades.end(); ++it) {
        sum += it->second;
    }
    return sum / grades.size();
}

std::string findBestSubject(const std::map<std::string, double>& grades) {
    std::string bestSubject = "";
    double bestGrade = 0.0;
    
    for (std::map<std::string, double>::const_iterator it = grades.begin(); 
         it != grades.end(); ++it) {
        if (it->second > bestGrade) {
            bestGrade = it->second;
            bestSubject = it->first;
        }
    }
    return bestSubject;
}

int main() {
    std::vector<Student> students;
    students.push_back({"张三", {{"数学", 85.5}, {"英语", 92.0}, {"物理", 78.5}}});
    students.push_back({"李四", {{"数学", 90.0}, {"英语", 88.5}, {"物理", 85.0}}});
    
    for (size_t i = 0; i < students.size(); ++i) {
        Student& student = students[i];
        std::cout << "学生: " << student.name << std::endl;
        std::cout << "平均分: " << calculateAverage(student.grades) << std::endl;
        std::cout << "最佳科目: " << findBestSubject(student.grades) << std::endl;
        std::cout << "---" << std::endl;
    }
    
    return 0;
}
```

## 要求
1. 使用 `auto` 简化所有类型声明
2. 使用范围 for 循环替代传统的迭代器循环
3. 使用结构化绑定简化 map 遍历
4. 使用初始化列表简化容器初始化
5. 使用 `std::optional` 处理可能的错误情况（如空成绩）
6. 函数应该接受 `std::string_view` 参数以提高效率

## 提示
- 考虑如何使用 `std::optional<std::string>` 替代返回空字符串
- 思考如何让代码更安全、更高效
- 注意 const 正确性

## 验收标准
- 代码简洁易读
- 充分利用现代 C++ 特性
- 处理边界情况（如空数据）
- 性能优于原始代码