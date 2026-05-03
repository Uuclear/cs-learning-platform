#include <memory>
#include <iostream>
#include <vector>

class DataContainer {
public:
    DataContainer(const std::string& name) : name_(name) {
        std::cout << "DataContainer " << name_ << " created" << std::endl;
    }
    
    ~DataContainer() {
        std::cout << "DataContainer " << name_ << " destroyed" << std::endl;
    }
    
    const std::string& getName() const { return name_; }

private:
    std::string name_;
};

// 资源管理器类，使用shared_ptr管理共享资源
class ResourceManager {
private:
    std::vector<std::shared_ptr<DataContainer>> resources_;
    
public:
    void addResource(const std::string& name) {
        auto resource = std::make_shared<DataContainer>(name);
        resources_.push_back(resource);
    }
    
    std::shared_ptr<DataContainer> getResource(size_t index) {
        if (index < resources_.size()) {
            return resources_[index];
        }
        return nullptr;
    }
    
    size_t getResourceCount() const {
        return resources_.size();
    }
};

void demonstrateSharedPtrSolution() {
    std::cout << "=== shared_ptr 解决方案演示 ===" << std::endl;
    
    ResourceManager manager;
    manager.addResource("Database");
    manager.addResource("Cache");
    manager.addResource("Logger");
    
    std::cout << "Manager has " << manager.getResourceCount() << " resources" << std::endl;
    
    // 获取资源的多个引用
    auto db1 = manager.getResource(0);
    auto db2 = manager.getResource(0);
    
    if (db1 && db2) {
        std::cout << "Both references point to: " << db1->getName() << std::endl;
        std::cout << "Reference count: " << db1.use_count() << std::endl;
    }
    
    // 即使manager离开作用域，只要还有shared_ptr引用，资源就不会被销毁
    std::cout << "Resources remain alive as long as there are references" << std::endl;
}

int main() {
    demonstrateSharedPtrSolution();
    return 0;
}
