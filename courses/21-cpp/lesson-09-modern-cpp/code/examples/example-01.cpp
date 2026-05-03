#include <iostream>
#include <vector>
#include <map>
#include <string>

int main() {
    // 1. auto 类型推导 - 让编译器自动推断类型
    auto number = 42;           // int
    auto pi = 3.14159;          // double
    auto name = "Hello";        // const char*
    auto message = std::string("World"); // std::string

    std::cout << "=== auto 类型推导 ===" << std::endl;
    std::cout << "number: " << number << " (类型: int)" << std::endl;
    std::cout << "pi: " << pi << " (类型: double)" << std::endl;
    std::cout << "name: " << name << std::endl;
    std::cout << "message: " << message << std::endl;

    // 2. 初始化列表 - 统一的初始化语法
    std::vector<int> vec1{1, 2, 3, 4, 5};           // 列表初始化
    std::vector<int> vec2 = {6, 7, 8, 9, 10};       // 复制列表初始化
    std::map<std::string, int> scores{{"Alice", 95}, {"Bob", 87}, {"Charlie", 92}};

    std::cout << "\n=== 初始化列表 ===" << std::endl;
    std::cout << "vec1: ";
    for (const auto& val : vec1) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    std::cout << "vec2: ";
    for (const auto& val : vec2) {
        std::cout << val << " ";
    }
    std::cout << std::endl;

    std::cout << "scores: ";
    for (const auto& [name, score] : scores) {
        std::cout << name << ":" << score << " ";
    }
    std::cout << std::endl;

    // 3. 范围 for 循环 - 简洁遍历容器
    std::vector<std::string> fruits{"apple", "banana", "orange", "grape"};

    std::cout << "\n=== 范围 for 循环 ===" << std::endl;
    std::cout << "水果列表: ";
    for (const auto& fruit : fruits) {
        std::cout << fruit << " ";
    }
    std::cout << std::endl;

    // 修改容器中的元素
    std::cout << "转换为大写: ";
    for (auto& fruit : fruits) {  // 注意这里是引用，可以修改
        for (auto& c : fruit) {
            c = std::toupper(c);
        }
        std::cout << fruit << " ";
    }
    std::cout << std::endl;

    return 0;
}