#include <iostream>
#include <string>

namespace geometry {
    double calculate(double radius) {
        const double PI = 3.14159;
        return PI * radius * radius;
    }
}

namespace physics {
    double calculate(double mass, double velocity) {
        return 0.5 * mass * velocity * velocity;
    }
}

int main() {
    std::cout << "圆的面积 (半径=5): " << geometry::calculate(5.0) << std::endl;
    std::cout << "动能 (质量=10, 速度=3): " << physics::calculate(10.0, 3.0) << std::endl;

    return 0;
}