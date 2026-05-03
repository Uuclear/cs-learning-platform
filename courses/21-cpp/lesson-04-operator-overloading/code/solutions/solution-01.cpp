#include <iostream>
#include <cmath>

class Complex {
private:
    double real;
    double imag;

public:
    // 构造函数
    Complex(double r = 0.0, double i = 0.0) : real(r), imag(i) {}

    // 成员函数重载 + 运算符
    Complex operator+(const Complex& other) const {
        return Complex(real + other.real, imag + other.imag);
    }

    // 成员函数重载 - 运算符
    Complex operator-(const Complex& other) const {
        return Complex(real - other.real, imag - other.imag);
    }

    // 成员函数重载 * 运算符
    Complex operator*(const Complex& other) const {
        double newReal = real * other.real - imag * other.imag;
        double newImag = real * other.imag + imag * other.real;
        return Complex(newReal, newImag);
    }

    // 成员函数重载 / 运算符
    Complex operator/(const Complex& other) const {
        double denominator = other.real * other.real + other.imag * other.imag;
        if (std::abs(denominator) < 1e-9) {
            throw std::runtime_error("Division by zero");
        }
        double newReal = (real * other.real + imag * other.imag) / denominator;
        double newImag = (imag * other.real - real * other.imag) / denominator;
        return Complex(newReal, newImag);
    }

    // 成员函数重载 == 运算符
    bool operator==(const Complex& other) const {
        const double EPSILON = 1e-9;
        return std::abs(real - other.real) < EPSILON &&
               std::abs(imag - other.imag) < EPSILON;
    }

    // 成员函数重载 != 运算符
    bool operator!=(const Complex& other) const {
        return !(*this == other);
    }

    // 获取实部和虚部
    double getReal() const { return real; }
    double getImag() const { return imag; }

    // 显示复数
    void display() const {
        if (imag >= 0) {
            std::cout << real << " + " << imag << "i";
        } else {
            std::cout << real << " - " << -imag << "i";
        }
    }
};

// 友元函数重载 << 运算符
std::ostream& operator<<(std::ostream& os, const Complex& c) {
    if (c.getImag() >= 0) {
        os << c.getReal() << " + " << c.getImag() << "i";
    } else {
        os << c.getReal() << " - " << -c.getImag() << "i";
    }
    return os;
}

int main() {
    Complex c1(3.0, 4.0);  // 3 + 4i
    Complex c2(1.0, -2.0); // 1 - 2i

    std::cout << "c1 = " << c1 << "\n";
    std::cout << "c2 = " << c2 << "\n\n";

    // 测试所有运算符
    std::cout << "c1 + c2 = " << (c1 + c2) << "\n";
    std::cout << "c1 - c2 = " << (c1 - c2) << "\n";
    std::cout << "c1 * c2 = " << (c1 * c2) << "\n";
    std::cout << "c1 / c2 = " << (c1 / c2) << "\n\n";

    Complex c3(3.0, 4.0);
    std::cout << "c1 == c3: " << (c1 == c3 ? "true" : "false") << "\n";
    std::cout << "c1 != c2: " << (c1 != c2 ? "true" : "false") << "\n";

    return 0;
}