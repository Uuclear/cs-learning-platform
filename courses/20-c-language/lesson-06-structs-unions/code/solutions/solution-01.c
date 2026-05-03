#include <stdio.h>
#include <string.h>

// 定义员工结构体（练习1的解决方案）
typedef struct {
    int id;
    char name[50];
    char department[30];
    float salary;
    int is_manager;  // 使用int作为布尔值：0=false, 1=true
} Employee;

// 函数：初始化员工信息
void init_employee(Employee *emp, int id, const char* name,
                   const char* department, float salary, int is_manager) {
    emp->id = id;
    strncpy(emp->name, name, sizeof(emp->name) - 1);
    emp->name[sizeof(emp->name) - 1] = '\0';  // 确保字符串安全终止

    strncpy(emp->department, department, sizeof(emp->department) - 1);
    emp->department[sizeof(emp->department) - 1] = '\0';

    emp->salary = salary;
    emp->is_manager = is_manager;
}

// 函数：打印员工信息
void print_employee(const Employee *emp) {
    printf("员工ID: %d\n", emp->id);
    printf("姓名: %s\n", emp->name);
    printf("部门: %s\n", emp->department);
    printf("薪资: $%.2f\n", emp->salary);
    printf("职位: %s\n", emp->is_manager ? "经理" : "普通员工");
    printf("------------------------\n");
}

// 函数：给员工加薪
void give_raise(Employee *emp, float amount) {
    if (amount > 0) {
        emp->salary += amount;
        printf("✓ 给 %s 成功加薪 $%.2f\n", emp->name, amount);
    } else {
        printf("⚠ 加薪金额必须大于0\n");
    }
}

int main() {
    // 创建并初始化员工
    Employee employees[3];

    init_employee(&employees[0], 1001, "张三", "开发部", 8000.0, 0);
    init_employee(&employees[1], 1002, "李四", "开发部", 12000.0, 1);
    init_employee(&employees[2], 2001, "王五", "市场部", 7500.0, 0);

    printf("=== 初始员工信息 ===\n");
    for (int i = 0; i < 3; i++) {
        print_employee(&employees[i]);
    }

    printf("=== 执行加薪操作 ===\n");
    give_raise(&employees[0], 1000.0);  // 给张三加薪
    give_raise(&employees[2], 800.0);   // 给王五加薪
    give_raise(&employees[1], -500.0);  // 尝试负数加薪（应该失败）

    printf("\n=== 更新后的员工信息 ===\n");
    for (int i = 0; i < 3; i++) {
        print_employee(&employees[i]);
    }

    return 0;
}