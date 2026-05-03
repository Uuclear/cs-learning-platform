#include <stdio.h>
#include <stdlib.h>

int main() {
    FILE *fp;
    char buffer[256];

    // 写入文件
    fp = fopen("example.txt", "w");
    if (fp == NULL) {
        printf("无法创建文件！\n");
        return 1;
    }
    fprintf(fp, "Hello, C语言文件操作！\n");
    fprintf(fp, "这是第二行内容。\n");
    fclose(fp);

    // 读取文件
    fp = fopen("example.txt", "r");
    if (fp == NULL) {
        printf("无法打开文件！\n");
        return 1;
    }

    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        printf("读取到: %s", buffer);
    }

    fclose(fp);
    return 0;
}