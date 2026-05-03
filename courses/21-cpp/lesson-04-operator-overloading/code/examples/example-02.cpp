#include <iostream>
#include <vector>

class Vector2D {
private:
    double x, y;

public:
    // 构造函数
    Vector2D(double x = 0.0, double y = 0.0) : x(x), y(y) {}

    // 获取坐标
    double getX() const { return x; }
    double getY() const { return y; }

    // 成员函数重载 + 运算符
    Vector2D operator+(const Vector2D& other) const {
        return Vector2D(x + other.x, y + other.y);
    }

    // 成员函数重载 - 运算符
    Vector2D operator-(const Vector2D& other) const {
        return Vector2D(x - other.x, y - other.y);
    }

    // 成员函数重载 * 运算符（标量乘法）
    Vector2D operator*(double scalar) const {
        return Vector2D(x * scalar, y * scalar);
    }

    // 计算向量长度
    double length() const {
        return std::sqrt(x * x + y * y);
    }
};

// 友元函数重载 << 运算符（输出流）
std::ostream& operator<<(std::ostream& os, const Vector2D& vec) {
    os << "(" << vec.getX() << ", " << vec.getY() << ")";
    return os;
}

// 友元函数重载 >> 运算符（输入流）
std::istream& operator>>(std::istream& is, Vector2D& vec) {
    double x, y;
    is >> x >> y;
    vec = Vector2D(x, y);
    return is;
}

// 非成员函数重载 * 运算符（标量在左边）
Vector2D operator*(double scalar, const Vector2D& vec) {
    return vec * scalar; // 利用已有的成员函数重载
}

int main() {
    Vector2D v1(3.0, 4.0);
    Vector2D v2(1.0, 2.0);

    std::cout << "v1 = " << v1 << "\n";
    std::cout << "v2 = " << v2 << "\n\n";

    // 测试向量加法
    Vector2D sum = v1 + v2;
    std::cout << "v1 + v2 = " << sum << "\n";

    // 测试向量减法
    Vector2D diff = v1 - v2;
    std::cout << "v1 - v2 = " << diff << "\n";

    // 测试标量乘法（右边）
    Vector2D scaled1 = v1 * 2.0;
    std::cout << "v1 * 2.0 = " << scaled1 << "\n";

    // 测试标量乘法（左边）
    Vector2D scaled2 = 3.0 * v1;
    std::cout << "3.0 * v1 = " << scaled2 << "\n";

    // 测试向量长度
    std::cout << "Length of v1: " << v1.length() << "\n\n";

    // 测试输入流重载
    std::cout << "请输入一个二维向量 (x y): ";
    Vector2D inputVec;
    std::cin >> inputVec;
    std::cout << "你输入的向量是: " << inputVec << "\n";

    return 0;
}