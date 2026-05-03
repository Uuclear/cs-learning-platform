#include <iostream>

// 示例1: 使用成员函数重载运算符
class PointMember {
private:
    int x, y;

public:
    PointMember(int x = 0, int y = 0) : x(x), y(y) {}

    // 成员函数重载 + 运算符
    PointMember operator+(const PointMember& other) const {
        return PointMember(x + other.x, y + other.y);
    }

    // 成员函数重载 << 运算符（这会导致编译错误！）
    // std::ostream& operator<<(std::ostream& os) const {
    //     os << "(" << x << ", " << y << ")";
    //     return os;
    // }

    void display() const {
        std::cout << "(" << x << ", " << y << ")";
    }

    int getX() const { return x; }
    int getY() const { return y; }
};

// 友元函数重载 << 运算符（正确的方式）
std::ostream& operator<<(std::ostream& os, const PointMember& point) {
    os << "(" << point.getX() << ", " << point.getY() << ")";
    return os;
}

// 示例2: 使用友元函数重载运算符
class PointFriend {
private:
    int x, y;

public:
    PointFriend(int x = 0, int y = 0) : x(x), y(y) {}

    // 声明友元函数
    friend PointFriend operator+(const PointFriend& p1, const PointFriend& p2);
    friend std::ostream& operator<<(std::ostream& os, const PointFriend& point);
    friend bool operator==(const PointFriend& p1, const PointFriend& p2);

    int getX() const { return x; }
    int getY() const { return y; }
};

// 友元函数定义
PointFriend operator+(const PointFriend& p1, const PointFriend& p2) {
    return PointFriend(p1.x + p2.x, p1.y + p2.y);
}

std::ostream& operator<<(std::ostream& os, const PointFriend& point) {
    os << "(" << point.x << ", " << point.y << ")";
    return os;
}

bool operator==(const PointFriend& p1, const PointFriend& p2) {
    return p1.x == p2.x && p1.y == p2.y;
}

// 演示为什么某些运算符必须用友元函数
class Number {
private:
    int value;

public:
    Number(int v = 0) : value(v) {}

    // 成员函数重载 + （int 在右边）
    Number operator+(int n) const {
        return Number(value + n);
    }

    // 注意：无法处理 int + Number 的情况（int 在左边）
    // 这需要友元函数或全局函数

    friend Number operator+(int n, const Number& num);
    friend std::ostream& operator<<(std::ostream& os, const Number& num);

    int getValue() const { return value; }
};

// 友元函数处理 int + Number
Number operator+(int n, const Number& num) {
    return Number(n + num.value);
}

std::ostream& operator<<(std::ostream& os, const Number& num) {
    os << num.value;
    return os;
}

int main() {
    std::cout << "=== 成员函数 vs 友元函数对比 ===\n\n";

    // PointMember 示例
    PointMember pm1(1, 2);
    PointMember pm2(3, 4);
    PointMember pmSum = pm1 + pm2;
    std::cout << "PointMember: " << pm1 << " + " << pm2 << " = " << pmSum << "\n\n";

    // PointFriend 示例
    PointFriend pf1(5, 6);
    PointFriend pf2(7, 8);
    PointFriend pfSum = pf1 + pf2;
    std::cout << "PointFriend: " << pf1 << " + " << pf2 << " = " << pfSum << "\n";
    std::cout << "PointFriend equality: " << (pf1 == pf1 ? "true" : "false") << "\n\n";

    // Number 示例 - 展示左操作数转换问题
    Number num(10);
    Number result1 = num + 5;  // 成员函数处理
    Number result2 = 5 + num;  // 友元函数处理
    std::cout << "num + 5 = " << result1 << "\n";
    std::cout << "5 + num = " << result2 << "\n";

    return 0;
}