# 挑战任务 2：多文件项目实践

## 目标
创建一个包含多个源文件和头文件的C项目，理解模块化编程的概念。

## 任务步骤

1. **设计项目结构**
   - 创建以下文件：
     - `main.c`：主程序文件
     - `math_utils.h`：数学工具函数头文件
     - `math_utils.c`：数学工具函数实现文件

2. **实现功能**
   - 在 `math_utils.h` 中声明以下函数：
     - `int factorial(int n)`：计算阶乘
     - `int is_prime(int n)`：判断是否为质数
     - `double power(double base, int exp)`：计算幂运算
   
   - 在 `math_utils.c` 中实现这些函数

3. **编写主程序**
   - 在 `main.c` 中包含 `math_utils.h`
   - 编写测试代码，调用所有三个函数并输出结果
   - 示例输出：
     ```
     5! = 120
     17 是质数: true
     2.5^3 = 15.625
     ```

4. **编译多文件项目**
   - 使用单条命令编译所有文件：
     ```bash
     gcc main.c math_utils.c -o math_program
     ```
   - 或者分步编译：
     ```bash
     gcc -c math_utils.c
     gcc -c main.c
     gcc main.o math_utils.o -o math_program
     ```

## 进阶挑战（可选）
- 添加错误处理：阶乘函数对负数输入返回-1
- 优化质数判断算法，提高大数判断效率
- 添加更多的数学函数到工具库中

## 提交要求
- 提交所有三个源文件（main.c, math_utils.h, math_utils.c）
- 截图显示程序运行结果
- 简要说明你在实现过程中遇到的挑战和解决方案