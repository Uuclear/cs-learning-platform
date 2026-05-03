#include <iostream>
#include <cmath>

class Vector3D {
private:
    double x, y, z;

public:
    // 构造函数
    Vector3D(double x = 0.0, double y = 0.0, double z = 0.0) : x(x), y(y), z(z) {}

    // 获取坐标
    double getX() const { return x; }
    double getY() const { return y; }
    double getZ() const { return z; }

    // 成员函数重载 + 运算符
    Vector3D operator+(const Vector3D& other) const {
        return Vector3D(x + other.x, y + other.y, z + other.z);
    }

    // 成员函数重载 - 运算符
    Vector3D operator-(const Vector3D& other) const {
        return Vector3D(x - other.x, y - other.y, z - other.z);
    }

    // 成员函数重载 * 运算符（标量乘法）
    Vector3D operator*(double scalar) const {
        return Vector3D(x * scalar, y * scalar, z * scalar);
    }

    // 成员函数重载 / 运算符（标量除法）
    Vector3D operator/(double scalar) const {
        if (std::abs(scalar) < 1e-9) {
            throw std::runtime_error("Division by zero");
        }
        return Vector3D(x / scalar, y / scalar, z / scalar);
    }

    // 点积运算符（成员函数）
    double dot(const Vector3D& other) const {
        return x * other.x + y * other.y + z * other.z;
    }

    // 叉积运算符（成员函数）
    Vector3D cross(const Vector3D& other) const {
        return Vector3D(
            y * other.z - z * other.y,
            z * other.x - x * other.z,
            x * other.y - y * other.x
        );
    }

    // 计算向量长度
    double length() const {
        return std::sqrt(x * x + y * y + z * z);
    }

    // 单位化向量
    Vector3D normalize() const {
        double len = length();
        if (std::abs(len) < 1e-9) {
            throw std::runtime_error("Cannot normalize zero vector");
        }
        return *this / len;
    }
};

// 友元函数重载 << 运算符（输出流）
std::ostream& operator<<(std::ostream& os, const Vector3D& vec) {
    os << "(" << vec.getX() << ", " << vec.getY() << ", " << vec.getZ() << ")";
    return os;
}

// 友元函数重载 >> 运算符（输入流）
std::istream& operator>>(std::istream& is, Vector3D& vec) {
    double x, y, z;
    is >> x >> y >> z;
    vec = Vector3D(x, y, z);
    return is;
}

// 非成员函数重载 * 运算符（标量在左边）
Vector3D operator*(double scalar, const Vector3D& vec) {
    return vec * scalar;
}

int main() {
    Vector3D v1(1.0, 2.0, 3.0);
    Vector3D v2(4.0, 5.0, 6.0);

    std::cout << "v1 = " << v1 << "\n";
    std::cout << "v2 = " << v2 << "\n\n";

    // 基本运算
    std::cout << "v1 + v2 = " << (v1 + v2) << "\n";
    std::cout << "v1 - v2 = " << (v1 - v2) << "\n";
    std::cout << "v1 * 2.0 = " << (v1 * 2.0) << "\n";
    std::cout << "3.0 * v1 = " << (3.0 * v1) << "\n";
    std::cout << "v1 / 2.0 = " << (v1 / 2.0) << "\n\n";

    // 向量运算
    std::cout << "Dot product: " << v1.dot(v2) << "\n";
    std::cout << "Cross product: " << v1.cross(v2) << "\n";
    std::cout << "Length of v1: " << v1.length() << "\n";
    std::cout << "Normalized v1: " << v1.normalize() << "\n\n";

    // 测试输入
    std::cout << "请输入一个三维向量 (x y z): ";
    Vector3D inputVec;
    std::cin >> inputVec;
    std::cout << "你输入的向量是: " << inputVec << "\n";

    return 0;
}