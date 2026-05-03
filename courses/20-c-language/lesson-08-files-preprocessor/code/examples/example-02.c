#include <stdio.h>
#include <stdlib.h>

typedef struct {
    int id;
    char name[50];
    float score;
} Student;

int main() {
    FILE *fp;
    Student students[] = {
        {1, "张三", 95.5},
        {2, "李四", 87.0},
        {3, "王五", 92.3}
    };
    Student read_student;
    int i;

    // 写入二进制文件
    fp = fopen("students.dat", "wb");
    if (fp == NULL) {
        perror("无法创建二进制文件");
        return 1;
    }

    for (i = 0; i < 3; i++) {
        fwrite(&students[i], sizeof(Student), 1, fp);
    }
    fclose(fp);

    // 读取二进制文件
    fp = fopen("students.dat", "rb");
    if (fp == NULL) {
        perror("无法打开二进制文件");
        return 1;
    }

    printf("读取的学生信息：\n");
    while (fread(&read_student, sizeof(Student), 1, fp) == 1) {
        printf("ID: %d, 姓名: %s, 分数: %.1f\n",
               read_student.id, read_student.name, read_student.score);
    }

    fclose(fp);
    return 0;
}