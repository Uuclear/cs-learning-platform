# 挑战 1：实现通用的向量容器

## 目标
实现一个名为 `MyVector` 的类模板，它应该具有以下功能：

- 动态数组存储（使用 `new` 和 `delete[]`）
- 支持任意类型的元素
- 提供基本的操作：`push_back`, `pop_back`, `size`, `capacity`, `operator[]`
- 实现深拷贝语义（拷贝构造函数和赋值操作符）
- 自动内存管理，避免内存泄漏

## 要求
1. 使用模板参数 `T` 表示元素类型
2. 内部使用动态分配的数组存储元素
3. 实现自动扩容机制（当容量不足时，容量翻倍）
4. 提供 const 和 non-const 版本的 `operator[]`
5. 实现异常安全的内存管理

## 提示
- 考虑使用 RAII 原则管理资源
- 注意处理边界情况（如空容器、越界访问等）
- 参考 STL `std::vector` 的接口设计
- 测试你的实现与不同类型的元素（int, string, 自定义类等）

## 扩展挑战（可选）
- 添加迭代器支持（begin(), end()）
- 实现移动语义（C++11 移动构造函数和移动赋值）
- 添加 `reserve()` 和 `shrink_to_fit()` 方法

## 测试代码框架
```cpp
#include <iostream>
#include <string>

// 在这里实现你的 MyVector 类模板

int main() {
    // 测试整数向量
    MyVector<int> intVec;
    intVec.push_back(1);
    intVec.push_back(2);
    intVec.push_back(3);
    
    std::cout << "整数向量大小: " << intVec.size() << std::endl;
    for (size_t i = 0; i < intVec.size(); ++i) {
        std::cout << intVec[i] << " ";
    }
    std::cout << std::endl;
    
    // 测试字符串向量
    MyVector<std::string> strVec;
    strVec.push_back("Hello");
    strVec.push_back("World");
    strVec.push_back("C++");
    
    std::cout << "字符串向量大小: " << strVec.size() << std::endl;
    for (size_t i = 0; i < strVec.size(); ++i) {
        std::cout << strVec[i] << " ";
    }
    std::cout << std::endl;
    
    return 0;
}
```