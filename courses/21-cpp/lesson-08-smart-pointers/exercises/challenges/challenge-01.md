# 挑战 1：实现安全的链表类

## 目标
使用 `std::unique_ptr` 实现一个简单的单向链表类，确保内存安全且无内存泄漏。

## 要求
1. 创建一个 `Node` 类，包含整数值和指向下一个节点的 `std::unique_ptr`
2. 创建一个 `SafeList` 类，管理链表的操作
3. 实现以下方法：
   - `void push_front(int value)` - 在链表头部插入元素
   - `void pop_front()` - 删除链表头部元素
   - `bool empty() const` - 检查链表是否为空
   - `int front() const` - 返回头部元素的值（如果链表为空则抛出异常）
4. 确保所有内存都能正确释放，即使在异常情况下

## 提示
- 使用 `std::make_unique` 创建新节点
- 利用 `std::unique_ptr` 的移动语义来转移所有权
- 考虑异常安全性

## 测试代码
```cpp
#include <iostream>
#include <cassert>

int main() {
    SafeList list;
    
    // 测试空链表
    assert(list.empty());
    
    // 测试插入
    list.push_front(3);
    list.push_front(2);
    list.push_front(1);
    
    assert(!list.empty());
    assert(list.front() == 1);
    
    // 测试删除
    list.pop_front();
    assert(list.front() == 2);
    
    list.pop_front();
    list.pop_front();
    assert(list.empty());
    
    std::cout << "All tests passed!" << std::endl;
    return 0;
}
```

## 扩展挑战
- 添加 `size()` 方法返回链表长度
- 实现迭代器支持范围 for 循环
- 添加异常安全保证（强异常安全保证）
