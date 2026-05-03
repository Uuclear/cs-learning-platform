#include <iostream>
#include <cstdio>
#include <string>

int main() {
    std::cout << "=== C++ 风格 ===" << std::endl;
    std::string cpp_name;
    std::cout << "请输入姓名: ";
    std::getline(std::cin, cpp_name);
    std::cout << "C++ 风格: " << cpp_name << std::endl;

    std::cout << "\n=== C 风格 ===" << std::endl;
    char c_name[100];
    std::cout << "请输入姓名: ";
    std::fgets(c_name, sizeof(c_name), stdin);
    std::printf("C 风格: %s", c_name);

    return 0;
}