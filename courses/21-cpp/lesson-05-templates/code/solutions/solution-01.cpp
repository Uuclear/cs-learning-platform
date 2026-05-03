#include <iostream>
#include <string>

// 函数模板：通用交换函数
template<typename T>
void mySwap(T& a, T& b) {
    T temp = a;
    a = b;
    b = temp;
}

// 函数模板：通用最大值函数
template<typename T>
T myMax(const T& a, const T& b) {
    return (a > b) ? a : b;
}

// 函数模板：通用最小值函数
template<typename T>
T myMin(const T& a, const T& b) {
    return (a < b) ? a : b;
}

// 多参数函数模板：找出多个值中的最大值
template<typename T>
T myMax(const T& first, const T& second) {
    return (first > second) ? first : second;
}

template<typename T, typename... Args>
T myMax(const T& first, const T& second, const Args&... args) {
    return myMax(myMax(first, second), args...);
}

int main() {
    // 测试整数交换
    int x = 10, y = 20;
    std::cout << "交换前: x = " << x << ", y = " << y << std::endl;
    mySwap(x, y);
    std::cout << "交换后: x = " << x << ", y = " << y << std::endl;

    // 测试字符串交换
    std::string str1 = "Hello";
    std::string str2 = "World";
    std::cout << "交换前: str1 = " << str1 << ", str2 = " << str2 << std::endl;
    mySwap(str1, str2);
    std::cout << "交换后: str1 = " << str1 << ", str2 = " << str2 << std::endl;

    // 测试最大值和最小值
    std::cout << "myMax(5, 3) = " << myMax(5, 3) << std::endl;
    std::cout << "myMin(5, 3) = " << myMin(5, 3) << std::endl;
    std::cout << "myMax(\"apple\", \"banana\") = " << myMax(std::string("apple"), std::string("banana")) << std::endl;

    // 测试多参数最大值
    std::cout << "myMax(1, 5, 3, 9, 2) = " << myMax(1, 5, 3, 9, 2) << std::endl;

    return 0;
}