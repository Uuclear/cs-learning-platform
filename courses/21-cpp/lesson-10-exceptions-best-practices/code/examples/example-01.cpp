#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>

// 基本异常处理示例
void demonstrateBasicExceptions() {
    std::cout << "=== 基本异常处理示例 ===" << std::endl;

    // 示例1: 标准异常 - out_of_range
    try {
        std::vector<int> numbers = {1, 2, 3, 4, 5};
        int value = numbers.at(10); // 这会抛出 std::out_of_range
        std::cout << "Value: " << value << std::endl;
    } catch (const std::out_of_range& e) {
        std::cout << "捕获到范围异常: " << e.what() << std::endl;
    }

    // 示例2: 多重catch块
    try {
        throw std::invalid_argument("无效参数异常");
    } catch (const std::invalid_argument& e) {
        std::cout << "捕获到无效参数异常: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "捕获到通用异常: " << e.what() << std::endl;
    }

    // 示例3: 抛出基本类型异常（不推荐，但可行）
    try {
        throw "这是一个C风格字符串异常";
    } catch (const char* msg) {
        std::cout << "捕获到C风格字符串异常: " << msg << std::endl;
    }

    // 示例4: 重新抛出异常
    try {
        try {
            throw std::runtime_error("内部错误");
        } catch (const std::runtime_error& e) {
            std::cout << "内部处理: " << e.what() << std::endl;
            throw; // 重新抛出当前异常
        }
    } catch (const std::exception& e) {
        std::cout << "外部处理: " << e.what() << std::endl;
    }
}

// 函数可能抛出异常的情况
double divide(double a, double b) {
    if (b == 0.0) {
        throw std::invalid_argument("除数不能为零");
    }
    return a / b;
}

void testDivide() {
    std::cout << "\n=== 除法函数异常测试 ===" << std::endl;

    try {
        double result = divide(10.0, 2.0);
        std::cout << "10.0 / 2.0 = " << result << std::endl;

        result = divide(10.0, 0.0); // 这会抛出异常
        std::cout << "10.0 / 0.0 = " << result << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cout << "除法错误: " << e.what() << std::endl;
    }
}

int main() {
    demonstrateBasicExceptions();
    testDivide();

    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
