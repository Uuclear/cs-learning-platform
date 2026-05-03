// solution-02.c - static变量与作用域的完整解决方案

#include <stdio.h>

// 全局计数器（整个程序可见）
int global_call_count = 0;

// 文件级static变量（仅当前文件可见）
static int file_call_count = 0;

// 函数原型声明
void demonstrate_local_scope();
void demonstrate_static_local_scope();
void demonstrate_global_scope();
void demonstrate_file_static_scope();
static void internal_function();

int main() {
    printf("=== C语言作用域演示 ===\n\n");
    
    // 演示局部变量作用域
    demonstrate_local_scope();
    printf("\n");
    
    // 演示static局部变量
    demonstrate_static_local_scope();
    printf("\n");
    
    // 演示全局变量
    demonstrate_global_scope();
    printf("\n");
    
    // 演示文件级static变量
    demonstrate_file_static_scope();
    printf("\n");
    
    // 调用内部函数
    internal_function();
    
    return 0;
}

void demonstrate_local_scope() {
    printf("--- 局部变量作用域 ---\n");
    for (int i = 0; i < 3; i++) {
        int local_var = i * 10;  // 每次循环都重新创建
        printf("Loop %d: local_var = %d\n", i, local_var);
    }
    // local_var 在这里不可见（超出作用域）
}

void demonstrate_static_local_scope() {
    printf("--- Static局部变量作用域 ---\n");
    for (int i = 0; i < 3; i++) {
        static int static_local = 100;  // 只初始化一次
        static_local += i;
        printf("Loop %d: static_local = %d\n", i, static_local);
    }
}

void demonstrate_global_scope() {
    printf("--- 全局变量作用域 ---\n");
    global_call_count++;
    printf("Global call count: %d\n", global_call_count);
    
    // 在函数内部也可以修改全局变量
    global_call_count += 5;
    printf("After modification: %d\n", global_call_count);
}

void demonstrate_file_static_scope() {
    printf("--- 文件级Static变量作用域 ---\n");
    file_call_count++;
    printf("File static call count: %d\n", file_call_count);
}

// static函数只能在当前文件中使用
static void internal_function() {
    printf("--- Static函数演示 ---\n");
    printf("This function can only be called within this file.\n");
    printf("It can access both global_call_count (%d) and file_call_count (%d)\n", 
           global_call_count, file_call_count);
}
