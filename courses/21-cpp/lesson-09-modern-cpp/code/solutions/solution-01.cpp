#include <iostream>
#include <vector>
#include <map>
#include <string>

int main() {
    // 使用 auto 和初始化列表创建数据结构
    auto numbers = std::vector<int>{1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    auto studentGrades = std::map<std::string, double>{
        {"张三", 85.5},
        {"李四", 92.0},
        {"王五", 78.5},
        {"赵六", 88.0}
    };

    std::cout << "=== 学生成绩管理系统 ===" << std::endl;

    // 使用范围 for 循环遍历 vector
    std::cout << "数字列表: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // 使用范围 for 循环和结构化绑定遍历 map
    std::cout << "\n学生成绩:" << std::endl;
    for (const auto& [name, grade] : studentGrades) {
        std::cout << "  " << name << ": " << grade << " 分" << std::endl;
    }

    // 计算平均分
    auto total = 0.0;
    for (const auto& [name, grade] : studentGrades) {
        total += grade;
    }
    auto average = total / studentGrades.size();
    std::cout << "\n班级平均分: " << average << " 分" << std::endl;

    // 找出最高分学生
    auto bestStudent = std::string{};
    auto bestGrade = 0.0;
    for (const auto& [name, grade] : studentGrades) {
        if (grade > bestGrade) {
            bestGrade = grade;
            bestStudent = name;
        }
    }
    std::cout << "最高分学生: " << bestStudent << " (" << bestGrade << " 分)" << std::endl;

    return 0;
}