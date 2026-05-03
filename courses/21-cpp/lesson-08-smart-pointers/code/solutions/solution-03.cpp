#include <memory>
#include <iostream>
#include <vector>

// 观察者模式实现 - 使用weak_ptr避免循环引用

class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(int value) = 0;
};

class Subject {
private:
    std::vector<std::weak_ptr<Observer>> observers_;
    int state_ = 0;
    
public:
    void attach(std::shared_ptr<Observer> observer) {
        observers_.push_back(observer);
    }
    
    void notify() {
        // 清理过期的观察者并通知有效的观察者
        for (auto it = observers_.begin(); it != observers_.end();) {
            if (auto obs = it->lock()) {
                obs->update(state_);
                ++it;
            } else {
                // 观察者已经被销毁，移除weak_ptr
                it = observers_.erase(it);
            }
        }
    }
    
    void setState(int newState) {
        state_ = newState;
        notify();
    }
    
    int getState() const { return state_; }
};

class ConcreteObserver : public Observer {
private:
    std::string name_;
    
public:
    ConcreteObserver(const std::string& name) : name_(name) {
        std::cout << "Observer " << name_ << " created" << std::endl;
    }
    
    ~ConcreteObserver() {
        std::cout << "Observer " << name_ << " destroyed" << std::endl;
    }
    
    void update(int value) override {
        std::cout << "Observer " << name_ << " received update: " << value << std::endl;
    }
};

void demonstrateWeakPtrSolution() {
    std::cout << "=== weak_ptr 解决方案演示（观察者模式）===" << std::endl;
    
    Subject subject;
    
    // 创建观察者
    auto observer1 = std::make_shared<ConcreteObserver>("Observer1");
    auto observer2 = std::make_shared<ConcreteObserver>("Observer2");
    
    // 附加观察者到主题
    subject.attach(observer1);
    subject.attach(observer2);
    
    // 发送更新
    subject.setState(42);
    
    // 让observer1离开作用域
    observer1.reset();
    
    // 再次发送更新 - 应该只通知observer2
    std::cout << "\nAfter removing observer1:" << std::endl;
    subject.setState(100);
    
    // observer2离开作用域时自动清理
    std::cout << "All resources cleaned up properly!" << std::endl;
}

int main() {
    demonstrateWeakPtrSolution();
    return 0;
}
