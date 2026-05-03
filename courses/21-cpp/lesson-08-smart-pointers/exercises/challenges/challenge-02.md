# 挑战 2：实现资源池管理器

## 目标
使用 `std::shared_ptr` 和 `std::weak_ptr` 实现一个线程安全的资源池管理器，支持资源共享和自动回收。

## 要求
1. 创建一个 `ResourcePool` 模板类，管理某种类型资源的池
2. 实现以下功能：
   - `std::shared_ptr<T> acquire()` - 获取一个资源的共享指针
   - 如果池中有可用资源，返回该资源
   - 如果池中没有可用资源，创建新资源
   - `size_t getActiveCount() const` - 返回当前活跃（被引用）的资源数量
   - `size_t getTotalCount() const` - 返回池中总的资源数量
3. 使用 `std::weak_ptr` 跟踪所有创建的资源，以便在资源不再被外部引用时能够回收到池中
4. 确保线程安全性（可以使用 `std::mutex`）

## 提示
- 维护两个容器：一个存储活跃资源的 `weak_ptr`，另一个存储可用资源的 `shared_ptr`
- 在 `acquire()` 方法中，首先清理过期的 `weak_ptr`，然后检查可用资源
- 使用 `lock()` 方法检查 `weak_ptr` 是否仍然有效

## 测试代码
```cpp
#include <iostream>
#include <thread>
#include <vector>

class ExpensiveResource {
public:
    ExpensiveResource(int id) : id_(id) {
        std::cout << "Creating resource " << id_ << std::endl;
    }
    
    ~ExpensiveResource() {
        std::cout << "Destroying resource " << id_ << std::endl;
    }
    
    int getId() const { return id_; }

private:
    int id_;
};

int main() {
    ResourcePool<ExpensiveResource> pool;
    
    // 获取资源
    auto res1 = pool.acquire();
    auto res2 = pool.acquire();
    
    std::cout << "Active: " << pool.getActiveCount() 
              << ", Total: " << pool.getTotalCount() << std::endl;
    
    // 释放一个资源
    res1.reset();
    
    // 再次获取资源（应该重用之前释放的资源）
    auto res3 = pool.acquire();
    
    std::cout << "Active: " << pool.getActiveCount() 
              << ", Total: " << pool.getTotalCount() << std::endl;
    
    std::cout << "All tests completed!" << std::endl;
    return 0;
}
```

## 扩展挑战
- 添加资源最大数量限制
- 实现资源的初始化回调函数
- 添加资源使用时间统计
- 支持自定义资源创建策略
