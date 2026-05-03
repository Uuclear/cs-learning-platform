#include <iostream>
#include <string>

namespace math_utils {
    int add(int a, int b) {
        return a + b;
    }

    double multiply(double a, double b) {
        return a * b;
    }
}

namespace string_utils {
    std::string concatenate(const std::string& a, const std::string& b) {
        return a + " " + b;
    }
}

int main() {
    // 使用完整的命名空间限定
    std::cout << "5 + 3 = " << math_utils::add(5, 3) << std::endl;
    std::cout << "2.5 * 4.0 = " << math_utils::multiply(2.5, 4.0) << std::endl;

    // 使用 using 声明
    using string_utils::concatenate;
    std::cout << concatenate("Hello", "World") << std::endl;

    return 0;
}