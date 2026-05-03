#include <memory>
#include <iostream>

class SharedResource {
public:
    SharedResource(int value) : value_(value) {
        std::cout << "SharedResource " << value_ << " constructed" << std::endl;
    }
    
    ~SharedResource() {
        std::cout << "SharedResource " << value_ << " destructed" << std::endl;
    }
    
    int getValue() const { return value_; }

private:
    int value_;
};

void demonstrateSharedPtr() {
    std::cout << "=== shared_ptr 引用计数演示 ===" << std::endl;
    
    // 创建第一个shared_ptr
    std::shared_ptr<SharedResource> ptr1 = std::make_shared<SharedResource>(42);
    std::cout << "Reference count after creation: " << ptr1.use_count() << std::endl;
    
    // 创建第二个shared_ptr - 共享同一对象
    std::shared_ptr<SharedResource> ptr2 = ptr1;
    std::cout << "Reference count after sharing: " << ptr1.use_count() << std::endl;
    
    // 创建第三个shared_ptr
    {
        std::shared_ptr<SharedResource> ptr3 = ptr2;
        std::cout << "Reference count with 3 pointers: " << ptr1.use_count() << std::endl;
        
        // ptr3离开作用域
    }
    std::cout << "Reference count after ptr3 destroyed: " << ptr1.use_count() << std::endl;
    
    // 访问共享对象
    std::cout << "Value from ptr1: " << ptr1->getValue() << std::endl;
    std::cout << "Value from ptr2: " << ptr2->getValue() << std::endl;
    
    // ptr1和ptr2离开作用域，引用计数变为0，对象被析构
    std::cout << "Exiting function..." << std::endl;
}

int main() {
    demonstrateSharedPtr();
    return 0;
}
