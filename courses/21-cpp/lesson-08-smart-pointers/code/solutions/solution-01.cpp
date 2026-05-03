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

// 工厂函数返回unique_ptr
std::unique_ptr<Resource> createResource(int id) {
    return std::make_unique<Resource>(id);
}

void demonstrateUniquePtrSolution() {
    std::cout << "=== unique_ptr 解决方案演示 ===" << std::endl;
    
    // 使用工厂函数创建资源
    auto resource = createResource(100);
    resource->doWork();
    
    // 可以安全地传递给其他函数（通过移动语义）
    auto another_resource = std::move(resource);
    another_resource->doWork();
    
    // 资源在离开作用域时自动清理
    std::cout << "Resources will be automatically cleaned up" << std::endl;
}

int main() {
    demonstrateUniquePtrSolution();
    return 0;
}
