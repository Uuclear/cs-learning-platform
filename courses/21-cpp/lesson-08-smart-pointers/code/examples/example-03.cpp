#include <memory>
#include <iostream>

class Node {
public:
    int data;
    std::shared_ptr<Node> next;
    std::weak_ptr<Node> prev; // 使用weak_ptr避免循环引用
    
    Node(int value) : data(value) {
        std::cout << "Node " << data << " created" << std::endl;
    }
    
    ~Node() {
        std::cout << "Node " << data << " destroyed" << std::endl;
    }
};

void demonstrateWeakPtr() {
    std::cout << "=== weak_ptr 打破循环引用演示 ===" << std::endl;
    
    // 创建两个节点
    auto node1 = std::make_shared<Node>(1);
    auto node2 = std::make_shared<Node>(2);
    
    // 建立双向链接 - next使用shared_ptr，prev使用weak_ptr
    node1->next = node2;
    node2->prev = node1;
    
    // 检查引用计数
    std::cout << "node1 reference count: " << node1.use_count() << std::endl;
    std::cout << "node2 reference count: " << node2.use_count() << std::endl;
    
    // 使用weak_ptr访问prev节点
    if (auto prev_node = node2->prev.lock()) {
        std::cout << "node2's prev data: " << prev_node->data << std::endl;
    } else {
        std::cout << "node2's prev is expired" << std::endl;
    }
    
    // 测试weak_ptr的过期情况
    auto weak_copy = node1; // 这是一个shared_ptr
    std::weak_ptr<Node> weak_ref = node1; // 这是一个weak_ptr
    
    // 让shared_ptr离开作用域
    weak_copy.reset(); // 释放shared_ptr
    
    // 检查weak_ptr是否过期
    if (weak_ref.expired()) {
        std::cout << "weak_ref is expired" << std::endl;
    } else {
        std::cout << "weak_ref is still valid" << std::endl;
    }
    
    std::cout << "Exiting function..." << std::endl;
    // 两个节点都能正确析构，因为没有循环引用！
}

int main() {
    demonstrateWeakPtr();
    return 0;
}
