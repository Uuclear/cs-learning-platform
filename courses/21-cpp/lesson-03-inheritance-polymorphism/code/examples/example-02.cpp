#include <iostream>
#include <vector>
#include <memory>

// 抽象基类：形状
class Shape {
protected:
    std::string color;

public:
    Shape(const std::string& c) : color(c) {}

    // 虚析构函数（必须！）
    virtual ~Shape() = default;

    // 纯虚函数 - 必须在派生类中实现
    virtual double area() const = 0;
    virtual void draw() const = 0;
    virtual std::string getType() const = 0;

    // 普通虚函数 - 可以有默认实现
    virtual void setColor(const std::string& newColor) {
        color = newColor;
    }

    std::string getColor() const { return color; }
};

// 圆形类
class Circle : public Shape {
private:
    double radius;

public:
    Circle(const std::string& c, double r) : Shape(c), radius(r) {}

    double area() const override {
        return 3.14159265359 * radius * radius;
    }

    void draw() const override {
        std::cout << "Drawing a " << color << " circle with radius " << radius << std::endl;
    }

    std::string getType() const override {
        return "Circle";
    }

    double getRadius() const { return radius; }
};

// 矩形类
class Rectangle : public Shape {
private:
    double width, height;

public:
    Rectangle(const std::string& c, double w, double h) : Shape(c), width(w), height(h) {}

    double area() const override {
        return width * height;
    }

    void draw() const override {
        std::cout << "Drawing a " << color << " rectangle (" << width << " x " << height << ")" << std::endl;
    }

    std::string getType() const override {
        return "Rectangle";
    }

    double getWidth() const { return width; }
    double getHeight() const { return height; }
};

// 三角形类
class Triangle : public Shape {
private:
    double base, height;

public:
    Triangle(const std::string& c, double b, double h) : Shape(c), base(b), height(h) {}

    double area() const override {
        return 0.5 * base * height;
    }

    void draw() const override {
        std::cout << "Drawing a " << color << " triangle (base: " << base << ", height: " << height << ")" << std::endl;
    }

    std::string getType() const override {
        return "Triangle";
    }

    double getBase() const { return base; }
    double getHeight() const { return height; }
};

// 多态函数：处理任何形状
void processShape(const Shape& shape) {
    std::cout << "Processing a " << shape.getType() << ":" << std::endl;
    shape.draw();
    std::cout << "Area: " << shape.area() << std::endl;
    std::cout << "Color: " << shape.getColor() << std::endl;
    std::cout << "---" << std::endl;
}

// 多态容器：存储不同类型的形状
void demonstratePolymorphism() {
    std::vector<std::unique_ptr<Shape>> shapes;

    // 添加不同类型的形状到同一个容器
    shapes.push_back(std::make_unique<Circle>("red", 5.0));
    shapes.push_back(std::make_unique<Rectangle>("blue", 4.0, 6.0));
    shapes.push_back(std::make_unique<Triangle>("green", 8.0, 3.0));

    std::cout << "\n=== 多态容器演示 ===" << std::endl;
    double totalArea = 0.0;

    for (const auto& shape : shapes) {
        shape->draw();
        totalArea += shape->area();
    }

    std::cout << "Total area of all shapes: " << totalArea << std::endl;
}

int main() {
    std::cout << "=== 虚函数与多态演示 ===" << std::endl;

    // 创建具体的形状对象
    Circle circle("red", 3.0);
    Rectangle rectangle("blue", 4.0, 5.0);
    Triangle triangle("green", 6.0, 4.0);

    std::cout << "\n--- 使用具体类型 ---" << std::endl;
    std::cout << "Circle area: " << circle.area() << std::endl;
    std::cout << "Rectangle area: " << rectangle.area() << std::endl;
    std::cout << "Triangle area: " << triangle.area() << std::endl;

    std::cout << "\n--- 多态函数调用 ---" << std::endl;
    processShape(circle);
    processShape(rectangle);
    processShape(triangle);

    // 演示多态容器
    demonstratePolymorphism();

    // 演示通过基类指针的多态
    std::cout << "\n=== 基类指针多态演示 ===" << std::endl;
    Shape* shapes[] = {
        new Circle("yellow", 2.0),
        new Rectangle("purple", 3.0, 7.0)
    };

    for (int i = 0; i < 2; ++i) {
        std::cout << shapes[i]->getType() << " with area " << shapes[i]->area() << std::endl;
        delete shapes[i]; // 虚析构函数确保正确清理
    }

    return 0;
}