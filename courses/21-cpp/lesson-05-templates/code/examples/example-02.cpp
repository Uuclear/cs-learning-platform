#include <iostream>
#include <vector>
#include <stdexcept>

// 类模板：通用栈容器
template<typename T>
class Stack {
private:
    std::vector<T> elements;

public:
    // 构造函数
    Stack() = default;

    // 拷贝构造函数
    Stack(const Stack& other) : elements(other.elements) {}

    // 赋值操作符
    Stack& operator=(const Stack& other) {
        if (this != &other) {
            elements = other.elements;
        }
        return *this;
    }

    // 入栈操作
    void push(const T& element) {
        elements.push_back(element);
    }

    // 出栈操作
    void pop() {
        if (elements.empty()) {
            throw std::out_of_range("Stack<>::pop(): empty stack");
        }
        elements.pop_back();
    }

    // 获取栈顶元素
    T& top() {
        if (elements.empty()) {
            throw std::out_of_range("Stack<>::top(): empty stack");
        }
        return elements.back();
    }

    const T& top() const {
        if (elements.empty()) {
            throw std::out_of_range("Stack<>::top(): empty stack");
        }
        return elements.back();
    }

    // 检查是否为空
    bool empty() const {
        return elements.empty();
    }

    // 获取大小
    size_t size() const {
        return elements.size();
    }
};

int main() {
    // 创建整数栈
    Stack<int> intStack;
    intStack.push(1);
    intStack.push(2);
    intStack.push(3);

    std::cout << "整数栈大小: " << intStack.size() << std::endl;
    std::cout << "栈顶元素: " << intStack.top() << std::endl;

    intStack.pop();
    std::cout << "出栈后栈顶元素: " << intStack.top() << std::endl;

    // 创建字符串栈
    Stack<std::string> stringStack;
    stringStack.push("Hello");
    stringStack.push("World");
    stringStack.push("C++");

    std::cout << "\n字符串栈大小: " << stringStack.size() << std::endl;
    while (!stringStack.empty()) {
        std::cout << "栈顶: " << stringStack.top() << std::endl;
        stringStack.pop();
    }

    // 测试异常处理
    try {
        Stack<double> emptyStack;
        emptyStack.top(); // 这会抛出异常
    } catch (const std::out_of_range& e) {
        std::cout << "\n捕获异常: " << e.what() << std::endl;
    }

    return 0;
}