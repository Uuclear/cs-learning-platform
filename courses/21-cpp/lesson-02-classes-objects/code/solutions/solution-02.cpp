#include <iostream>
#include <string>
#include <vector>
#include <cmath>

/**
 * 解决方案2：图书类和点类的完整实现
 */

// 图书类实现
class Book {
private:
    std::string title;
    std::string author;
    std::string isbn;
    double price;

public:
    // 构造函数
    Book(std::string t, std::string a, std::string i, double p = 0.0)
        : title(t), author(a), isbn(i), price(p) {
        if (price < 0) price = 0;
    }

    // 获取书名
    std::string getTitle() const {
        return title;
    }

    // 获取作者
    std::string getAuthor() const {
        return author;
    }

    // 获取ISBN
    std::string getIsbn() const {
        return isbn;
    }

    // 获取价格
    double getPrice() const {
        return price;
    }

    // 设置价格（不能为负）
    void setPrice(double p) {
        if (p >= 0) {
            price = p;
        }
    }

    // 显示图书信息
    void displayInfo() const {
        std::cout << "书名：" << title << std::endl;
        std::cout << "作者：" << author << std::endl;
        std::cout << "ISBN：" << isbn << std::endl;
        std::cout << "价格：" << price << "元" << std::endl;
    }
};

// 点类实现
class Point {
private:
    double x, y;

public:
    // 默认构造函数
    Point(double xCoord = 0.0, double yCoord = 0.0) : x(xCoord), y(yCoord) {}

    // 获取x坐标
    double getX() const {
        return x;
    }

    // 获取y坐标
    double getY() const {
        return y;
    }

    // 移动x坐标（支持链式调用）
    Point& moveX(double deltaX) {
        x += deltaX;
        return *this;
    }

    // 移动y坐标（支持链式调用）
    Point& moveY(double deltaY) {
        y += deltaY;
        return *this;
    }

    // 同时移动x和y坐标（支持链式调用）
    Point& move(double deltaX, double deltaY) {
        x += deltaX;
        y += deltaY;
        return *this;
    }

    // 设置坐标位置
    Point& setPosition(double newX, double newY) {
        x = newX;
        y = newY;
        return *this;
    }

    // 计算到原点的距离
    double distanceFromOrigin() const {
        return std::sqrt(x * x + y * y);
    }

    // 计算到另一个点的距离
    double distanceTo(const Point& other) const {
        double dx = x - other.x;
        double dy = y - other.y;
        return std::sqrt(dx * dx + dy * dy);
    }

    // 显示点的信息
    void display() const {
        std::cout << "Point(" << x << ", " << y << ")" << std::endl;
    }
};

// 使用示例
int main() {
    std::cout << "=== 图书类解决方案 ===" << std::endl;

    // 创建图书对象
    Book book1("C++ Primer", "Stanley B. Lippman", "978-0321714114", 89.5);
    Book book2("Effective C++", "Scott Meyers", "978-0321334879", 75.0);

    // 显示图书信息
    book1.displayInfo();
    std::cout << std::endl;
    book2.displayInfo();

    // 修改价格
    book1.setPrice(95.0);
    std::cout << "\n修改后的价格：" << book1.getPrice() << "元" << std::endl;

    std::cout << "\n=== 点类解决方案 ===" << std::endl;

    // 创建点对象
    Point p1(3.0, 4.0);
    Point p2(0.0, 0.0);

    std::cout << "点p1: ";
    p1.display();
    std::cout << "点p2: ";
    p2.display();

    // 计算距离
    std::cout << "p1到原点的距离：" << p1.distanceFromOrigin() << std::endl;
    std::cout << "p1到p2的距离：" << p1.distanceTo(p2) << std::endl;

    // 链式调用演示
    std::cout << "\n=== 链式调用演示 ===" << std::endl;
    Point p3;
    std::cout << "初始点p3: ";
    p3.display();

    p3.moveX(5.0).moveY(3.0);
    std::cout << "移动后p3: ";
    p3.display();

    p3.setPosition(1.0, 1.0).move(2.0, 3.0);
    std::cout << "重新定位并移动后p3: ";
    p3.display();

    return 0;
}