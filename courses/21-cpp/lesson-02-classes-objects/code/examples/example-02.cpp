#include <iostream>
#include <string>
#include <cmath>

/**
 * 示例2：几何图形类
 * 演示面积计算、const成员函数的使用
 */
class Rectangle {
private:
    double width;
    double height;

public:
    // 构造函数
    Rectangle(double w = 0.0, double h = 0.0) : width(w), height(h) {
        if (width < 0) width = 0;
        if (height < 0) height = 0;
    }

    // 设置尺寸
    void setDimensions(double w, double h) {
        if (w >= 0) width = w;
        if (h >= 0) height = h;
    }

    // 获取宽度（const成员函数）
    double getWidth() const {
        return width;
    }

    // 获取高度（const成员函数）
    double getHeight() const {
        return height;
    }

    // 计算面积（const成员函数）
    double getArea() const {
        return width * height;
    }

    // 计算周长（const成员函数）
    double getPerimeter() const {
        return 2 * (width + height);
    }

    // 显示信息（const成员函数）
    void displayInfo() const {
        std::cout << "矩形 - 宽度：" << width
                  << "，高度：" << height
                  << "，面积：" << getArea()
                  << "，周长：" << getPerimeter() << std::endl;
    }
};

class Circle {
private:
    double radius;
    static constexpr double PI = 3.14159265358979323846;

public:
    // 构造函数
    Circle(double r = 0.0) : radius(r) {
        if (radius < 0) radius = 0;
    }

    // 设置半径
    void setRadius(double r) {
        if (r >= 0) radius = r;
    }

    // 获取半径（const成员函数）
    double getRadius() const {
        return radius;
    }

    // 计算面积（const成员函数）
    double getArea() const {
        return PI * radius * radius;
    }

    // 计算周长（const成员函数）
    double getPerimeter() const {
        return 2 * PI * radius;
    }

    // 显示信息（const成员函数）
    void displayInfo() const {
        std::cout << "圆形 - 半径：" << radius
                  << "，面积：" << getArea()
                  << "，周长：" << getPerimeter() << std::endl;
    }
};

// 使用示例
int main() {
    std::cout << "=== 几何图形类演示 ===" << std::endl;

    // 创建矩形对象
    Rectangle rect(5.0, 3.0);
    rect.displayInfo();

    // 创建圆形对象
    Circle circle(4.0);
    circle.displayInfo();

    // 修改尺寸
    rect.setDimensions(6.0, 4.0);
    std::cout << "\n修改后的矩形：" << std::endl;
    rect.displayInfo();

    circle.setRadius(5.0);
    std::cout << "\n修改后的圆形：" << std::endl;
    circle.displayInfo();

    return 0;
}