#include <iostream>

// 错误的基类设计 - 没有虚析构函数
class BadBase {
public:
    BadBase() {
        std::cout << "BadBase constructor called" << std::endl;
    }

    // 错误：没有virtual析构函数
    ~BadBase() {
        std::cout << "BadBase destructor called" << std::endl;
    }

    virtual void doSomething() {
        std::cout << "BadBase::doSomething()" << std::endl;
    }
};

class BadDerived : public BadBase {
private:
    int* data; // 动态分配的资源

public:
    BadDerived() : data(new int[100]) {
        std::cout << "BadDerived constructor called" << std::endl;
    }

    ~BadDerived() {
        delete[] data; // 清理资源
        std::cout << "BadDerived destructor called" << std::endl;
    }

    void doSomething() override {
        std::cout << "BadDerived::doSomething()" << std::endl;
    }
};

// 正确的基类设计 - 有虚析构函数
class GoodBase {
public:
    GoodBase() {
        std::cout << "GoodBase constructor called" << std::endl;
    }

    // 正确：virtual析构函数
    virtual ~GoodBase() {
        std::cout << "GoodBase destructor called" << std::endl;
    }

    virtual void doSomething() {
        std::cout << "GoodBase::doSomething()" << std::endl;
    }
};

class GoodDerived : public GoodBase {
private:
    int* data; // 动态分配的资源

public:
    GoodDerived() : data(new int[100]) {
        std::cout << "GoodDerived constructor called" << std::endl;
    }

    ~GoodDerived() override {
        delete[] data; // 清理资源
        std::cout << "GoodDerived destructor called" << std::endl;
    }

    void doSomething() override {
        std::cout << "GoodDerived::doSomething()" << std::endl;
    }
};

void demonstrateBadCase() {
    std::cout << "\n=== 错误案例演示（内存泄漏） ===" << std::endl;

    // 通过基类指针创建派生类对象
    BadBase* ptr = new BadDerived();

    ptr->doSomething();

    // 删除基类指针 - 只会调用BadBase的析构函数！
    // BadDerived的析构函数不会被调用，导致data内存泄漏
    delete ptr;

    std::cout << "注意：BadDerived的析构函数没有被调用，造成内存泄漏！" << std::endl;
}

void demonstrateGoodCase() {
    std::cout << "\n=== 正确案例演示（无内存泄漏） ===" << std::endl;

    // 通过基类指针创建派生类对象
    GoodBase* ptr = new GoodDerived();

    ptr->doSomething();

    // 删除基类指针 - 由于virtual析构函数，会正确调用GoodDerived的析构函数
    delete ptr;

    std::cout << "正确：GoodDerived的析构函数被正确调用，无内存泄漏！" << std::endl;
}

// 更安全的现代C++方式：使用智能指针
#include <memory>

void demonstrateModernCpp() {
    std::cout << "\n=== 现代C++最佳实践（智能指针） ===" << std::endl;

    // 使用unique_ptr自动管理内存
    std::unique_ptr<GoodBase> ptr = std::make_unique<GoodDerived>();

    ptr->doSomething();

    // 不需要手动delete，unique_ptr会在作用域结束时自动清理
    // 即使没有virtual析构函数，智能指针也会正确工作（但仍然推荐使用virtual析构函数）

    std::cout << "使用智能指针，内存自动管理，更加安全！" << std::endl;
}

int main() {
    std::cout << "=== 内存泄漏修复解决方案 ===" << std::endl;

    demonstrateBadCase();
    demonstrateGoodCase();
    demonstrateModernCpp();

    std::cout << "\n=== 关键要点总结 ===" << std::endl;
    std::cout << "1. 如果类可能被继承，必须声明virtual析构函数" << std::endl;
    std::cout << "2. virtual析构函数确保通过基类指针删除对象时，派生类析构函数也被调用" << std::endl;
    std::cout << "3. 现代C++推荐使用智能指针（unique_ptr, shared_ptr）来自动管理内存" << std::endl;
    std::cout << "4. 即使使用智能指针，也建议保留virtual析构函数以保持接口一致性" << std::endl;

    return 0;
}