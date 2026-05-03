#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 图书结构体
struct Book {
    char title[100];
    char author[50];
    int year;
    float price;
};

// 学生结构体（用于动态数组示例）
struct Student {
    int id;
    char name[50];
    float gpa;
};

int main() {
    printf("=== 结构体指针演示 ===\n");

    // 1. 结构体指针的基本使用
    struct Book book1 = {"The C Programming Language", "Kernighan & Ritchie", 1978, 45.99};
    struct Book *bookPtr = &book1;

    printf("书名: %s\n", bookPtr->title);
    printf("作者: %s\n", (*bookPtr).author);  // 等价于 bookPtr->author
    printf("年份: %d, 价格: $%.2f\n", bookPtr->year, bookPtr->price);

    // 2. 动态分配单个结构体
    struct Book *book2 = malloc(sizeof(struct Book));
    if (book2 != NULL) {
        strcpy(book2->title, "Programming in C");
        strcpy(book2->author, "Stephen Kochan");
        book2->year = 2014;
        book2->price = 39.99;

        printf("\n动态分配的书:\n");
        printf("书名: %s\n", book2->title);
        printf("作者: %s\n", book2->author);
        printf("年份: %d, 价格: $%.2f\n", book2->year, book2->price);

        free(book2);  // 记得释放内存
    }

    printf("\n=== 动态结构体数组演示 ===\n");

    // 3. 动态分配结构体数组
    int numStudents = 3;
    struct Student *students = malloc(numStudents * sizeof(struct Student));

    if (students == NULL) {
        printf("内存分配失败！\n");
        return 1;
    }

    // 初始化学生数据
    students[0].id = 1001;
    strcpy(students[0].name, "Alice");
    students[0].gpa = 3.8;

    students[1].id = 1002;
    strcpy(students[1].name, "Bob");
    students[1].gpa = 3.5;

    students[2].id = 1003;
    strcpy(students[2].name, "Charlie");
    students[2].gpa = 3.9;

    // 使用指针遍历数组
    printf("学生列表:\n");
    for (int i = 0; i < numStudents; i++) {
        struct Student *student = &students[i];  // 获取每个学生的指针
        printf("ID: %d, 姓名: %s, GPA: %.2f\n",
               student->id, student->name, student->gpa);
    }

    // 4. 扩展数组大小（模拟动态增长）
    printf("\n=== 扩展数组演示 ===\n");
    struct Student *newStudents = realloc(students, (numStudents + 1) * sizeof(struct Student));
    if (newStudents != NULL) {
        students = newStudents;
        students[3].id = 1004;
        strcpy(students[3].name, "Diana");
        students[3].gpa = 3.7;

        printf("扩展后的学生列表 (4个学生):\n");
        for (int i = 0; i <= 3; i++) {
            printf("ID: %d, 姓名: %s, GPA: %.2f\n",
                   students[i].id, students[i].name, students[i].gpa);
        }
    } else {
        printf("扩展数组失败！\n");
    }

    // 释放内存
    free(students);

    return 0;
}