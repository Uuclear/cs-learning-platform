#include <iostream>
#include <map>
#include <string>
#include <sstream>
#include <cctype>

// 将字符串转换为小写
std::string toLowerCase(const std::string& str) {
    std::string result = str;
    for (char& c : result) {
        c = std::tolower(static_cast<unsigned char>(c));
    }
    return result;
}

// 词频统计函数
std::map<std::string, int> countWordFrequency(const std::string& text) {
    std::map<std::string, int> wordCount;
    std::istringstream iss(text);
    std::string word;

    while (iss >> word) {
        // 简单的单词清理：移除标点符号
        std::string cleanWord;
        for (char c : word) {
            if (std::isalpha(c)) {
                cleanWord += c;
            }
        }

        if (!cleanWord.empty()) {
            cleanWord = toLowerCase(cleanWord);
            wordCount[cleanWord]++;
        }
    }

    return wordCount;
}

int main() {
    std::string text = "Hello world! Hello C++ programming. "
                      "C++ is powerful and efficient. "
                      "Programming with C++ is fun!";

    std::cout << "原文本: " << text << std::endl;
    std::cout << "\n=== 词频统计结果 ===" << std::endl;

    auto frequencies = countWordFrequency(text);

    // map自动按键排序输出
    for (const auto& [word, count] : frequencies) {
        std::cout << word << ": " << count << std::endl;
    }

    std::cout << "\n=== 查找特定单词 ===" << std::endl;
    std::string searchWord = "c++";
    if (frequencies.find(searchWord) != frequencies.end()) {
        std::cout << "'" << searchWord << "' 出现了 "
                  << frequencies[searchWord] << " 次" << std::endl;
    } else {
        std::cout << "'" << searchWord << "' 没有在文本中找到" << std::endl;
    }

    return 0;
}