# 挑战 2：实现类型特征和条件编译

## 目标
实现一个通用的算法，能够根据类型特征自动选择最优的实现方式。

## 具体任务
1. 实现类型特征（Type Traits）来检测类型是否具有特定属性：
   - `is_integral_v<T>`：检查类型是否为整数类型
   - `has_begin_end_v<T>`：检查类型是否具有 begin() 和 end() 成员函数

2. 实现一个通用的 `printContainer` 函数模板，它能够：
   - 对于支持迭代器的容器（如 vector, list, array），使用范围 for 循环打印所有元素
   - 对于整数类型，直接打印值
   - 对于其他类型，打印 "Unsupported type"

3. 使用 SFINAE 或 C++17 的 `if constexpr` 来实现条件编译

## 要求
- 使用模板元编程技术
- 不要使用预处理器宏
- 确保代码在 C++17 或更高版本下编译通过
- 提供清晰的错误信息（如果可能）

## 提示
- 可以参考 `<type_traits>` 头文件中的标准类型特征
- 对于检测成员函数，可以使用 SFINAE 技术
- `if constexpr` 在编译时进行条件判断，只编译满足条件的分支

## 测试代码框架
```cpp
#include <iostream>
#include <vector>
#include <list>
#include <array>

// 在这里实现你的类型特征和 printContainer 函数

int main() {
    // 测试整数类型
    printContainer(42);
    
    // 测试标准容器
    std::vector<int> vec = {1, 2, 3, 4, 5};
    printContainer(vec);
    
    std::list<std::string> lst = {"Hello", "World", "C++"};
    printContainer(lst);
    
    std::array<double, 3> arr = {1.1, 2.2, 3.3};
    printContainer(arr);
    
    // 测试不支持的类型
    printContainer("This is a string literal");
    
    return 0;
}
```

## 预期输出
```
42
1 2 3 4 5 
Hello World C++ 
1.1 2.2 3.3 
Unsupported type
```

## 扩展挑战（可选）
- 添加对 C 风格数组的支持
- 实现自定义分隔符功能
- 支持嵌套容器（如 vector<vector<int>>）