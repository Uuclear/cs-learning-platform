#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>

// C++ 风格读取文件
std::string readFileCpp(const std::string& filename) {
    std::ifstream file(filename);
    std::string content;
    std::string line;

    if (file.is_open()) {
        while (std::getline(file, line)) {
            content += line + "\n";
        }
        file.close();
    }

    return content;
}

// C 风格读取文件
std::string readFileC(const std::string& filename) {
    FILE* file = std::fopen(filename.c_str(), "r");
    std::string content;

    if (file != nullptr) {
        char buffer[1024];
        while (std::fgets(buffer, sizeof(buffer), file) != nullptr) {
            content += buffer;
        }
        std::fclose(file);
    }

    return content;
}

int main() {
    // 创建一个测试文件
    std::ofstream testFile("test.txt");
    testFile << "这是测试内容\n第二行\n第三行";
    testFile.close();

    std::cout << "=== C++ 风格读取 ===" << std::endl;
    std::string cppContent = readFileCpp("test.txt");
    std::cout << cppContent;

    std::cout << "\n=== C 风格读取 ===" << std::endl;
    std::string cContent = readFileC("test.txt");
    std::cout << cContent;

    // 清理测试文件
    std::remove("test.txt");

    return 0;
}