#include <iostream>
#include <string>

int main() {
    std::cout << "Hello, C++ World!" << std::endl;

    std::cout << "请输入您的姓名: ";
    std::string name;
    std::getline(std::cin, name);

    std::cout << "请输入您的年龄: ";
    int age;
    std::cin >> age;

    std::cout << "您好, " << name << "! 您今年 " << age << " 岁。" << std::endl;

    return 0;
}