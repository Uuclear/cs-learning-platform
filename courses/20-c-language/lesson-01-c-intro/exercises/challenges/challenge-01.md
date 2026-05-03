# 挑战任务 1：环境搭建与编译

## 目标
成功搭建C语言开发环境并编译运行你的第一个程序。

## 任务步骤

1. **安装编译器**
   - 在Linux/macOS上：确保已安装GCC或Clang
     ```bash
     # 检查GCC
     gcc --version
     # 或检查Clang
     clang --version
     ```
   - 在Windows上：安装MinGW-w64或使用WSL

2. **创建Hello World程序**
   - 创建一个名为 `my_first_program.c` 的文件
   - 编写一个简单的Hello World程序，输出你的名字和"欢迎学习C语言！"

3. **编译并运行**
   - 使用以下命令编译程序：
     ```bash
     gcc my_first_program.c -o my_program
     ```
   - 运行生成的可执行文件：
     ```bash
     ./my_program
     ```

4. **探索编译过程**
   - 使用 `-E` 选项查看预处理结果
   - 使用 `-S` 选项查看生成的汇编代码
   - 比较不同编译步骤的输出文件大小

## 提交要求
- 提交你的C源代码文件
- 截图显示程序成功编译和运行的结果
- 简要描述你在编译过程中观察到的现象