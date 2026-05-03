#include <iostream>
#include <string>
#include <string_view>
#include <vector>

// 传统的字符串函数 - 会创建不必要的副本
void processStringOld(const std::string& str) {
    std::cout << "处理字符串 (传统): \"" << str << "\"" << std::endl;
    std::cout << "长度: " << str.length() << std::endl;
}

// 使用 string_view 的高效函数 - 零拷贝
void processStringView(std::string_view sv) {
    std::cout << "处理字符串 (string_view): \"" << sv << "\"" << std::endl;
    std::cout << "长度: " << sv.length() << std::endl;

    // string_view 支持大部分 string 操作
    if (!sv.empty()) {
        std::cout << "首字符: " << sv[0] << std::endl;
        std::cout << "子字符串(0,3): " << sv.substr(0, 3) << std::endl;
    }
}

// 模拟从文件或网络读取大量字符串数据
std::vector<std::string> generateTestData() {
    return {
        "Hello, World!",
        "Modern C++ is awesome",
        "std::string_view saves memory",
        "No more unnecessary copies",
        "Efficient string processing"
    };
}

int main() {
    std::cout << "=== std::string_view 高效字符串处理 ===" << std::endl;

    // 1. 从字符串字面量创建 string_view
    std::string_view literal = "这是一个字符串字面量";
    processStringView(literal);

    // 2. 从 std::string 创建 string_view
    std::string text = "这是一个 std::string 对象";
    std::string_view fromString = text;
    processStringView(fromString);

    // 3. 直接传递字符串字面量 - 自动转换
    std::cout << "\n--- 直接传递字面量 ---" << std::endl;
    processStringOld("直接传递给传统函数");  // 会创建临时 string 对象
    processStringView("直接传递给 string_view 函数");  // 零拷贝

    // 4. 处理大量数据的性能对比
    std::cout << "\n--- 处理大量数据 ---" << std::endl;
    auto testData = generateTestData();

    std::cout << "使用传统方式处理:" << std::endl;
    for (const auto& data : testData) {
        processStringOld(data);  // 每次都会传递 string 引用，但调用时可能有开销
    }

    std::cout << "\n使用 string_view 处理:" << std::endl;
    for (const auto& data : testData) {
        processStringView(data);  // 零拷贝，更高效
    }

    // 5. string_view 的其他特性
    std::cout << "\n--- string_view 其他特性 ---" << std::endl;
    std::string original = "Hello, Modern C++ Programming!";
    std::string_view view(original);

    // 移除前缀和后缀 (C++20 特性，这里展示概念)
    // 在 C++17 中需要手动实现
    auto trimmed = view;
    while (!trimmed.empty() && trimmed.front() == ' ') {
        trimmed.remove_prefix(1);
    }
    while (!trimmed.empty() && trimmed.back() == ' ') {
        trimmed.remove_suffix(1);
    }
    std::cout << "去除空格后: \"" << trimmed << "\"" << std::endl;

    // 比较操作
    std::string_view hello = "Hello";
    std::string_view world = "World";
    std::cout << "比较结果: " << (hello < world ? "Hello < World" : "Hello >= World") << std::endl;

    return 0;
}