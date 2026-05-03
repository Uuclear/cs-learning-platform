#include <iostream>
#include <vector>

int main() {
    // 创建vector并初始化
    std::vector<int> numbers = {10, 20, 30, 40, 50};

    std::cout << "=== Vector 基本操作 ===" << std::endl;
    std::cout << "初始vector: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "大小: " << numbers.size() << std::endl;
    std::cout << "容量: " << numbers.capacity() << std::endl;

    // 添加元素
    numbers.push_back(60);
    std::cout << "添加60后: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    std::cout << "\n=== 迭代器遍历 ===" << std::endl;

    // 使用传统迭代器
    std::cout << "传统迭代器遍历: ";
    for (auto it = numbers.begin(); it != numbers.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    // 使用反向迭代器
    std::cout << "反向迭代器遍历: ";
    for (auto rit = numbers.rbegin(); rit != numbers.rend(); ++rit) {
        std::cout << *rit << " ";
    }
    std::cout << std::endl;

    // 使用范围for循环
    std::cout << "范围for循环遍历: ";
    for (const auto& num : numbers) {
        std::cout << num << " ";
    }
    std::cout << std::endl;

    // 访问特定元素
    std::cout << "\n=== 元素访问 ===" << std::endl;
    std::cout << "第一个元素: " << numbers.front() << std::endl;
    std::cout << "最后一个元素: " << numbers.back() << std::endl;
    std::cout << "索引2的元素: " << numbers[2] << std::endl;
    std::cout << "索引3的元素(at): " << numbers.at(3) << std::endl;

    return 0;
}