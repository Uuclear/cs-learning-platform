#include <iostream>
#include <vector>
#include <algorithm>
#include <string>

// 定义一个学生结构体
struct Student {
    std::string name;
    int score;

    // 构造函数
    Student(const std::string& n, int s) : name(n), score(s) {}
};

// 自定义比较函数：按分数从高到低排序
bool compareByScoreDesc(const Student& a, const Student& b) {
    return a.score > b.score;
}

// 自定义比较函数：按姓名字母顺序排序
bool compareByName(const Student& a, const Student& b) {
    return a.name < b.name;
}

int main() {
    std::vector<Student> students = {
        {"张三", 85},
        {"李四", 92},
        {"王五", 78},
        {"赵六", 96},
        {"钱七", 88}
    };

    std::cout << "=== 原始学生列表 ===" << std::endl;
    for (const auto& student : students) {
        std::cout << student.name << ": " << student.score << std::endl;
    }

    // 使用 std::sort 进行排序
    std::cout << "\n=== 按分数从高到低排序 ===" << std::endl;
    std::sort(students.begin(), students.end(), compareByScoreDesc);
    for (const auto& student : students) {
        std::cout << student.name << ": " << student.score << std::endl;
    }

    // 重置为原始顺序
    students = {{"张三", 85}, {"李四", 92}, {"王五", 78}, {"赵六", 96}, {"钱七", 88}};

    std::cout << "\n=== 按姓名字母顺序排序 ===" << std::endl;
    std::sort(students.begin(), students.end(), compareByName);
    for (const auto& student : students) {
        std::cout << student.name << ": " << student.score << std::endl;
    }

    // 对简单类型进行排序
    std::vector<int> numbers = {5, 2, 8, 1, 9, 3};
    std::cout << "\n=== 数字排序 ===" << std::endl;
    std::cout << "排序前: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::sort(numbers.begin(), numbers.end());
    std::cout << "升序排序后: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::sort(numbers.begin(), numbers.end(), std::greater<int>());
    std::cout << "降序排序后: ";
    for (int num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    return 0;
}