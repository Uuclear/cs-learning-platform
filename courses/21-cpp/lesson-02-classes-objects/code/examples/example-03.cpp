#include <iostream>
#include <string>

/**
 * 示例3：this指针与链式调用
 * 演示this指针的使用和方法链式调用
 */
class Person {
private:
    std::string name;
    int age;
    std::string city;

public:
    // 默认构造函数
    Person() : name("未知"), age(0), city("未知") {}

    // 带参数的构造函数
    Person(std::string n, int a, std::string c)
        : name(n), age(a), city(c) {}

    // 使用this指针设置姓名
    Person& setName(std::string n) {
        this->name = n;  // 明确使用this指针
        return *this;    // 返回当前对象的引用，支持链式调用
    }

    // 使用this指针设置年龄
    Person& setAge(int a) {
        if (a >= 0) {
            this->age = a;
        }
        return *this;    // 返回当前对象的引用
    }

    // 使用this指针设置城市
    Person& setCity(std::string c) {
        this->city = c;
        return *this;    // 返回当前对象的引用
    }

    // 获取姓名（const成员函数）
    std::string getName() const {
        return this->name;  // this指针在const成员函数中是const Person*
    }

    // 获取年龄（const成员函数）
    int getAge() const {
        return this->age;
    }

    // 获取城市（const成员函数）
    std::string getCity() const {
        return this->city;
    }

    // 显示信息（const成员函数）
    void displayInfo() const {
        std::cout << "姓名：" << this->name
                  << "，年龄：" << this->age
                  << "，城市：" << this->city << std::endl;
    }

    // 比较两个Person对象是否相同
    bool isEqual(const Person& other) const {
        // this指向当前对象，other是传入的参数
        return (this->name == other.name) &&
               (this->age == other.age) &&
               (this->city == other.city);
    }
};

// 链式调用演示类
class Calculator {
private:
    double value;

public:
    Calculator(double initial = 0.0) : value(initial) {}

    // 链式加法
    Calculator& add(double x) {
        this->value += x;
        return *this;
    }

    // 链式减法
    Calculator& subtract(double x) {
        this->value -= x;
        return *this;
    }

    // 链式乘法
    Calculator& multiply(double x) {
        this->value *= x;
        return *this;
    }

    // 链式除法
    Calculator& divide(double x) {
        if (x != 0) {
            this->value /= x;
        }
        return *this;
    }

    // 获取当前值
    double getValue() const {
        return this->value;
    }

    // 重置为初始值
    Calculator& reset(double initial = 0.0) {
        this->value = initial;
        return *this;
    }
};

// 使用示例
int main() {
    std::cout << "=== this指针与链式调用演示 ===" << std::endl;

    // Person类的链式调用
    Person person;
    person.setName("李四")
          .setAge(25)
          .setCity("北京");

    std::cout << "创建的人员信息：" << std::endl;
    person.displayInfo();

    // 使用链式调用创建新对象
    Person person2("王五", 30, "上海");
    std::cout << "\n直接创建的人员信息：" << std::endl;
    person2.displayInfo();

    // 比较两个对象
    if (person.isEqual(person2)) {
        std::cout << "\n两个人员信息相同" << std::endl;
    } else {
        std::cout << "\n两个人员信息不同" << std::endl;
    }

    // Calculator类的链式调用
    std::cout << "\n=== 计算器链式调用演示 ===" << std::endl;
    Calculator calc;
    double result = calc.add(10)
                       .multiply(2)
                       .subtract(5)
                       .divide(3)
                       .getValue();

    std::cout << "计算结果：((0 + 10) * 2 - 5) / 3 = " << result << std::endl;

    // 重置并进行新的计算
    result = calc.reset(100)
                 .multiply(2)
                 .add(50)
                 .getValue();

    std::cout << "新计算结果：(100 * 2) + 50 = " << result << std::endl;

    return 0;
}