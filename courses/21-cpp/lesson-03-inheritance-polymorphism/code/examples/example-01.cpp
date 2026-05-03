#include <iostream>
#include <string>

// 基类：动物
class Animal {
protected:
    std::string name;
    int age;

public:
    // 构造函数
    Animal(const std::string& n, int a) : name(n), age(a) {
        std::cout << "Animal constructor called for " << name << std::endl;
    }

    // 虚析构函数（重要！）
    virtual ~Animal() {
        std::cout << "Animal destructor called for " << name << std::endl;
    }

    // 普通成员函数（非虚函数）
    void sleep() {
        std::cout << name << " is sleeping." << std::endl;
    }

    // 虚函数，可以被派生类重写
    virtual void makeSound() {
        std::cout << name << " makes a generic animal sound." << std::endl;
    }

    // 获取信息的函数
    std::string getName() const { return name; }
    int getAge() const { return age; }
};

// 派生类：狗
class Dog : public Animal {
private:
    std::string breed;

public:
    Dog(const std::string& n, int a, const std::string& b)
        : Animal(n, a), breed(b) {
        std::cout << "Dog constructor called for " << name << std::endl;
    }

    ~Dog() override {
        std::cout << "Dog destructor called for " << name << std::endl;
    }

    // 重写基类的虚函数
    void makeSound() override {
        std::cout << name << " barks: Woof! Woof!" << std::endl;
    }

    // 狗特有的函数
    void wagTail() {
        std::cout << name << " wags its tail happily." << std::endl;
    }

    std::string getBreed() const { return breed; }
};

// 派生类：猫
class Cat : public Animal {
private:
    bool isIndoor;

public:
    Cat(const std::string& n, int a, bool indoor)
        : Animal(n, a), isIndoor(indoor) {
        std::cout << "Cat constructor called for " << name << std::endl;
    }

    ~Cat() override {
        std::cout << "Cat destructor called for " << name << std::endl;
    }

    void makeSound() override {
        std::cout << name << " meows: Meow! Meow!" << std::endl;
    }

    void purr() {
        std::cout << name << " purrs contentedly." << std::endl;
    }

    bool getIsIndoor() const { return isIndoor; }
};

int main() {
    std::cout << "=== 基础继承演示 ===" << std::endl;

    // 创建具体的对象
    Dog myDog("Buddy", 3, "Golden Retriever");
    Cat myCat("Whiskers", 2, true);

    std::cout << "\n--- 使用具体类型 ---" << std::endl;
    myDog.sleep();
    myDog.makeSound();
    myDog.wagTail();

    myCat.sleep();
    myCat.makeSound();
    myCat.purr();

    std::cout << "\n--- 访问继承的成员 ---" << std::endl;
    std::cout << "Dog: " << myDog.getName() << ", " << myDog.getAge() << " years old, "
              << myDog.getBreed() << std::endl;
    std::cout << "Cat: " << myCat.getName() << ", " << myCat.getAge() << " years old, "
              << (myCat.getIsIndoor() ? "indoor" : "outdoor") << std::endl;

    return 0;
}