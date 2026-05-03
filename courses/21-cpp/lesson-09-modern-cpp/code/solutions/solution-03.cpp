#include <iostream>
#include <string>
#include <string_view>
#include <vector>
#include <optional>

// 高效的字符串分割函数，使用 string_view 避免复制
std::vector<std::string_view> splitString(std::string_view text, char delimiter) {
    std::vector<std::string_view> result;
    size_t start = 0;
    size_t end = 0;

    while ((end = text.find(delimiter, start)) != std::string_view::npos) {
        result.emplace_back(text.substr(start, end - start));
        start = end + 1;
    }

    // 添加最后一部分
    if (start < text.length()) {
        result.emplace_back(text.substr(start));
    }

    return result;
}

// 安全的字符串到数字转换
std::optional<int> stringToInt(std::string_view str) {
    if (str.empty()) {
        return std::nullopt;
    }

    try {
        size_t pos = 0;
        int value = std::stoi(std::string(str), &pos);
        if (pos == str.length()) {
            return value;
        }
    } catch (const std::exception&) {
        // 转换失败
    }
    return std::nullopt;
}

// 高效的文本处理函数
void processTextData(std::string_view data) {
    std::cout << "处理文本数据: \"" << data << "\"" << std::endl;

    // 分割文本
    auto words = splitString(data, ' ');
    std::cout << "单词数量: " << words.size() << std::endl;

    // 处理每个单词
    for (size_t i = 0; i < words.size(); ++i) {
        std::cout << "  单词 " << (i + 1) << ": \"" << words[i] << "\"" << std::endl;

        // 尝试转换为数字
        if (auto number = stringToInt(words[i])) {
            std::cout << "    -> 转换为数字: " << *number << std::endl;
        }
    }
}

int main() {
    std::cout << "=== string_view 高效解决方案 ===" << std::endl;

    // 1. 处理不同来源的字符串数据
    std::cout << "\n--- 处理字符串字面量 ---" << std::endl;
    processTextData("Hello World 42 Programming");

    std::cout << "\n--- 处理 std::string 对象 ---" << std::endl;
    std::string dynamicText = "Modern C++ 2026 is awesome";
    processTextData(dynamicText);

    std::cout << "\n--- 处理子字符串 ---" << std::endl;
    std::string longText = "This is a very long text that we want to process efficiently";
    std::string_view subView = longText.substr(10, 25); // 高效！无复制
    processTextData(subView);

    // 2. 性能对比演示
    std::cout << "\n--- 性能优势演示 ---" << std::endl;
    std::vector<std::string> largeDataSet = {
        "Processing large amounts of text data efficiently",
        "Using string_view to avoid unnecessary memory allocations",
        "Modern C++ features make code both safer and faster",
        "Zero-copy string processing with std::string_view"
    };

    // 模拟大量文本处理
    size_t totalProcessed = 0;
    for (const auto& text : largeDataSet) {
        // 使用 string_view 处理，避免额外复制
        std::string_view view = text;
        totalProcessed += view.length();

        // 简单的文本分析
        auto wordCount = splitString(view, ' ').size();
        std::cout << "处理了 " << view.length() << " 字符, " << wordCount << " 个单词" << std::endl;
    }
    std::cout << "总共处理了 " << totalProcessed << " 个字符" << std::endl;

    // 3. 安全的字符串操作
    std::cout << "\n--- 安全字符串转换 ---" << std::endl;
    std::vector<std::string_view> testValues = {"123", "45.6", "abc", "", "-789", "12x34"};

    for (const auto& value : testValues) {
        if (auto num = stringToInt(value)) {
            std::cout << "\"" << value << "\" -> " << *num << std::endl;
        } else {
            std::cout << "\"" << value << "\" -> 转换失败" << std::endl;
        }
    }

    return 0;
}