#include <stdio.h>
#include <string.h>

// 结构体定义：学生信息
struct Student {
    char name[50];
    int age;
    float gpa;
    char major[30];
};

// 结构体定义：点坐标
struct Point {
    int x;
    int y;
};

// 嵌套结构体：矩形
struct Rectangle {
    struct Point topLeft;
    struct Point bottomRight;
};

int main() {
    // 示例1：直接初始化结构体
    struct Student alice = {"Alice Johnson", 20, 3.8, "Computer Science"};

    // 示例2：逐个成员赋值
    struct Student bob;
    strcpy(bob.name, "Bob Smith");
    bob.age = 22;
    bob.gpa = 3.5;
    strcpy(bob.major, "Mathematics");

    // 示例3：嵌套结构体初始化
    struct Rectangle rect = {{0, 0}, {100, 50}};

    // 打印学生信息
    printf("=== 学生信息 ===\n");
    printf("学生1: %s, 年龄: %d, GPA: %.2f, 专业: %s\n",
           alice.name, alice.age, alice.gpa, alice.major);
    printf("学生2: %s, 年龄: %d, GPA: %.2f, 专业: %s\n",
           bob.name, bob.age, bob.gpa, bob.major);

    // 打印矩形信息
    printf("\n=== 矩形信息 ===\n");
    printf("左上角: (%d, %d)\n", rect.topLeft.x, rect.topLeft.y);
    printf("右下角: (%d, %d)\n", rect.bottomRight.x, rect.bottomRight.y);

    // 示例4：结构体数组
    struct Point points[3] = {{1, 2}, {3, 4}, {5, 6}};
    printf("\n=== 点坐标数组 ===\n");
    for (int i = 0; i < 3; i++) {
        printf("点%d: (%d, %d)\n", i+1, points[i].x, points[i].y);
    }

    return 0;
}