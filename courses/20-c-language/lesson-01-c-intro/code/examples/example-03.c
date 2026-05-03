#include <stdio.h>
#define MESSAGE "编译过程分步演示"

/**
 * 编译过程分步演示程序
 *
 * 这个程序用于演示C语言的完整编译流程：
 * 1. 预处理 (gcc -E): 处理宏定义、头文件包含等
 * 2. 编译 (gcc -S): 将C代码转换为汇编代码
 * 3. 汇编 (gcc -c): 将汇编代码转换为目标文件
 * 4. 链接 (gcc): 将目标文件链接成可执行文件
 *
 * 使用方法：
 * - gcc -E example-03.c -o example-03.i     # 预处理
 * - gcc -S example-03.c -o example-03.s     # 编译到汇编
 * - gcc -c example-03.c -o example-03.o     # 汇编到目标文件
 * - gcc example-03.c -o example-03          # 完整编译链接
 */

int main() {
    printf("%s\n", MESSAGE);
    printf("这是展示C语言编译流程的示例程序！\n");

    return 0;
}