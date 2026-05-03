// example-02.c - static 变量与局部变量对比

#include <stdio.h>

// 演示普通局部变量的行为
void normal_counter() {
    int count = 0;  // 每次调用都重新初始化为0
    count++;
    printf("Normal counter: %d\n", count);
}

// 演示static局部变量的行为
void static_counter() {
    static int count = 0;  // 只在第一次调用时初始化
    count++;
    printf("Static counter: %d\n", count);
}

// 全局变量（文件作用域）
int global_var = 100;

// static全局变量（仅限当前文件）
static int file_static_var = 200;

// 普通函数（可被其他文件调用）
void print_global_vars() {
    printf("Global var: %d\n", global_var);
    printf("File static var: %d\n", file_static_var);
}

// static函数（仅限当前文件使用）
static void internal_helper() {
    printf("This is an internal helper function!\n");
    printf("It can access file_static_var: %d\n", file_static_var);
}

int main() {
    printf("=== 局部变量 vs Static局部变量 ===\n");
    normal_counter();  // 输出: Normal counter: 1
    normal_counter();  // 输出: Normal counter: 1
    normal_counter();  // 输出: Normal counter: 1
    
    static_counter();  // 输出: Static counter: 1
    static_counter();  // 输出: Static counter: 2
    static_counter();  // 输出: Static counter: 3
    
    printf("\n=== 全局变量和Static全局变量 ===\n");
    print_global_vars();
    
    printf("\n=== Static函数演示 ===\n");
    internal_helper();  // 可以在当前文件中调用
    
    return 0;
}
