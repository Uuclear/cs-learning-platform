#include <iostream>
#include <typeinfo>
#include <string>

// 基础模板：通用打印函数
template<typename T>
void printType(const T& value) {
    std::cout << "通用模板: " << value << " (类型: " << typeid(T).name() << ")" << std::endl;
}

// 全特化：针对 const char* 的特化版本
template<>
void printType<const char*>(const char* const& value) {
    std::cout << "全特化 (const char*): " << value << " (C风格字符串)" << std::endl;
}

// 全特化：针对 std::string 的特化版本
template<>
void printType<std::string>(const std::string& value) {
    std::cout << "全特化 (std::string): " << value << " (长度: " << value.length() << ")" << std::endl;
}

// 类模板：通用容器
template<typename T, typename U>
class Pair {
public:
    T first;
    U second;

    Pair(const T& f, const U& s) : first(f), second(s) {}

    void display() {
        std::cout << "通用 Pair: (" << first << ", " << second << ")" << std::endl;
    }
};

// 偏特化：当第二个类型是 int 时的特化版本
template<typename T>
class Pair<T, int> {
public:
    T first;
    int second;

    Pair(const T& f, int s) : first(f), second(s) {}

    void display() {
        std::cout << "偏特化 Pair<T, int>: (" << first << ", " << second << ") - 第二个元素是整数" << std::endl;
    }
};

// 偏特化：当两个类型相同时的特化版本
template<typename T>
class Pair<T, T> {
public:
    T first;
    T second;

    Pair(const T& f, const T& s) : first(f), second(s) {}

    void display() {
        std::cout << "偏特化 Pair<T, T>: (" << first << ", " << second << ") - 两个元素类型相同" << std::endl;
        if (first == second) {
            std::cout << "  注意：两个元素值也相同！" << std::endl;
        }
    }
};

int main() {
    std::cout << "=== 函数模板特化演示 ===" << std::endl;
    printType(42);                    // 通用模板
    printType(3.14);                  // 通用模板
    printType("Hello World");         // 全特化 (const char*)
    printType(std::string("C++"));    // 全特化 (std::string)

    std::cout << "\n=== 类模板偏特化演示 ===" << std::endl;
    Pair<double, std::string> p1(3.14, "pi");
    p1.display();                     // 通用 Pair

    Pair<std::string, int> p2("年龄", 25);
    p2.display();                     // 偏特化 Pair<T, int>

    Pair<int, int> p3(10, 20);
    p3.display();                     // 偏特化 Pair<T, T>

    Pair<int, int> p4(5, 5);
    p4.display();                     // 偏特化 Pair<T, T> with same values

    return 0;
}