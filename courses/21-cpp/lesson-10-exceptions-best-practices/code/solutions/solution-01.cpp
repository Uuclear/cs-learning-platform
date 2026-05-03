#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>

// 解决方案：改进的异常处理示例
void demonstrateImprovedExceptions() {
    std::cout << "=== 改进的异常处理示例 ===" << std::endl;

    // 示例1: 使用 at() 而不是 [] 进行安全访问
    try {
        std::vector<int> numbers = {1, 2, 3, 4, 5};
        int index = 10;
        if (index < numbers.size()) {
            int value = numbers[index];
            std::cout << "安全访问值: " << value << std::endl;
        } else {
            throw std::out_of_range("索引超出范围: " + std::to_string(index));
        }
    } catch (const std::out_of_range& e) {
        std::cout << "捕获到范围异常: " << e.what() << std::endl;
    }

    // 示例2: 使用具体的异常类型
    try {
        throw std::domain_error("数学域错误：负数不能开平方根");
    } catch (const std::domain_error& e) {
        std::cout << "捕获到域错误: " << e.what() << std::endl;
    } catch (const std::logic_error& e) {
        std::cout << "捕获到逻辑错误: " << e.what() << std::endl;
    } catch (const std::runtime_error& e) {
        std::cout << "捕获到运行时错误: " << e.what() << std::endl;
    } catch (const std::exception& e) {
        std::cout << "捕获到通用异常: " << e.what() << std::endl;
    }

    // 示例3: 避免抛出基本类型，总是使用异常类
    try {
        throw std::runtime_error("使用异常类而不是C风格字符串");
    } catch (const std::exception& e) {
        std::cout << "最佳实践 - " << e.what() << std::endl;
    }

    // 示例4: 异常安全的函数设计
    auto safeDivide = [](double a, double b) -> double {
        if (b == 0.0) {
            throw std::invalid_argument("除数不能为零 - 使用异常进行错误报告");
        }
        return a / b;
    };

    try {
        std::cout << "10.0 / 3.0 = " << safeDivide(10.0, 3.0) << std::endl;
        std::cout << "10.0 / 0.0 = " << safeDivide(10.0, 0.0) << std::endl;
    } catch (const std::invalid_argument& e) {
        std::cout << "安全除法错误: " << e.what() << std::endl;
    }
}

// 异常规范和文档
/**
 * @brief 安全的数组访问函数
 * @param arr 输入数组
 * @param index 访问索引
 * @return 数组元素的引用
 * @throws std::out_of_range 如果索引超出范围
 * @throws std::invalid_argument 如果数组为空
 */
template<typename T>
const T& safeAt(const std::vector<T>& arr, size_t index) {
    if (arr.empty()) {
        throw std::invalid_argument("数组为空");
    }
    if (index >= arr.size()) {
        throw std::out_of_range("索引 " + std::to_string(index) + 
                               " 超出范围 [0, " + std::to_string(arr.size() - 1) + "]");
    }
    return arr[index];
}

void testSafeAt() {
    std::cout << "\n=== 安全数组访问测试 ===" << std::endl;
    
    std::vector<std::string> fruits = {"apple", "banana", "cherry"};
    
    try {
        std::cout << "水果[1]: " << safeAt(fruits, 1) << std::endl;
        std::cout << "水果[5]: " << safeAt(fruits, 5) << std::endl;
    } catch (const std::exception& e) {
        std::cout << "数组访问错误: " << e.what() << std::endl;
    }
    
    try {
        std::vector<int> empty;
        safeAt(empty, 0);
    } catch (const std::exception& e) {
        std::cout << "空数组错误: " << e.what() << std::endl;
    }
}

int main() {
    demonstrateImprovedExceptions();
    testSafeAt();

    std::cout << "\n程序正常结束！" << std::endl;
    return 0;
}
