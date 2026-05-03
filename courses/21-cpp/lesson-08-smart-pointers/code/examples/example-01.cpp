#include <memory>
#include <iostream>

class Resource {
public:
    Resource(int id) : id_(id) {
        std::cout << "Resource " << id_ << " constructed" << std::endl;
    }
    
    ~Resource() {
        std::cout << "Resource " << id_ << " destructed" << std::endl;
    }
    
    void doWork() const {
        std::cout << "Resource " << id_ << " is working" << std::endl;
    }

private:
    int id_;
};

void demonstrateUniquePtr() {
    std::cout << "=== unique_ptr 独占所有权演示 ===" << std::endl;
    
    // 创建unique_ptr - 独占所有权
    std::unique_ptr<Resource> ptr1 = std::make_unique<Resource>(1);
    ptr1->doWork();
    
    // 不能复制unique_ptr（编译错误）
    // std::unique_ptr<Resource> ptr2 = ptr1;
    
    // 可以移动unique_ptr - 转移所有权
    std::unique_ptr<Resource> ptr2 = std::move(ptr1);
    ptr2->doWork();
    
    // ptr1现在为空
    if (!ptr1) {
        std::cout << "ptr1 is null after move" << std::endl;
    }
    
    // ptr2离开作用域时自动析构Resource对象
    std::cout << "Exiting function..." << std::endl;
}

int main() {
    demonstrateUniquePtr();
    return 0;
}
