# 挑战 1：个人计算器

## 目标
创建一个简单的命令行计算器程序，支持基本的四则运算（加、减、乘、除）。

## 要求
1. 使用 C++ 风格的输入输出（iostream）
2. 将不同的运算函数放在名为 `calculator` 的命名空间中
3. 程序应该能够处理用户输入错误（如除零错误）
4. 支持连续计算，直到用户选择退出

## 示例交互
```
欢迎使用 C++ 计算器！
请输入第一个数字: 10
请输入运算符 (+, -, *, /): +
请输入第二个数字: 5
结果: 15

是否继续计算？(y/n): y
请输入第一个数字: 15
请输入运算符 (+, -, *, /): /
请输入第二个数字: 3
结果: 5

是否继续计算？(y/n): n
谢谢使用！
```

## 提示
- 使用 `std::cin` 和 `std::cout` 进行输入输出
- 考虑使用循环来支持连续计算
- 对于除零错误，可以使用条件判断或异常处理
- 函数声明示例：
  ```cpp
  namespace calculator {
      double add(double a, double b);
      double subtract(double a, double b);
      double multiply(double a, double b);
      double divide(double a, double b);
  }
  ```