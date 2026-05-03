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
        // (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
        double newReal = real * other.real - imag * other.imag;
        double newImag = real * other.imag + imag * other.real;
        return Complex(newReal, newImag);
    }

    // 成员函数重载 == 运算符
    bool operator==(const Complex& other) const {
        const double EPSILON = 1e-9;
        return std::abs(real - other.real) < EPSILON &&
               std::abs(imag - other.imag) < EPSILON;
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

int main() {
    Complex c1(3.0, 4.0);  // 3 + 4i
    Complex c2(1.0, -2.0); // 1 - 2i

    std::cout << "c1 = ";
    c1.display();
    std::cout << "\nc2 = ";
    c2.display();
    std::cout << "\n\n";

    // 测试 + 运算符
    Complex sum = c1 + c2;
    std::cout << "c1 + c2 = ";
    sum.display();
    std::cout << "\n";

    // 测试 - 运算符
    Complex diff = c1 - c2;
    std::cout << "c1 - c2 = ";
    diff.display();
    std::cout << "\n";

    // 测试 * 运算符
    Complex product = c1 * c2;
    std::cout << "c1 * c2 = ";
    product.display();
    std::cout << "\n";

    // 测试 == 运算符
    Complex c3(3.0, 4.0);
    std::cout << "\nc1 == c3: " << (c1 == c3 ? "true" : "false") << "\n";
    std::cout << "c1 == c2: " << (c1 == c2 ? "true" : "false") << "\n";

    return 0;
}