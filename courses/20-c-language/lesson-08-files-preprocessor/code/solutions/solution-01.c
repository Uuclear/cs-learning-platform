#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

// 统计文件中的单词数和行数
int count_words_and_lines(const char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        perror("无法打开文件");
        return -1;
    }

    int words = 0, lines = 0;
    int in_word = 0;
    char ch;

    while ((ch = fgetc(fp)) != EOF) {
        if (ch == '\n') {
            lines++;
        }

        if (isspace(ch)) {
            if (in_word) {
                words++;
                in_word = 0;
            }
        } else {
            in_word = 1;
        }
    }

    // 处理文件末尾没有换行符的情况
    if (in_word) {
        words++;
    }

    // 如果文件不为空但没有换行符，至少有一行
    if (lines == 0 && (words > 0)) {
        lines = 1;
    }

    fclose(fp);
    printf("文件 '%s' 包含 %d 行和 %d 个单词\n", filename, lines, words);
    return 0;
}

int main() {
    // 创建一个测试文件
    FILE *test_file = fopen("test.txt", "w");
    if (test_file == NULL) {
        perror("无法创建测试文件");
        return 1;
    }

    fprintf(test_file, "Hello world!\n");
    fprintf(test_file, "This is a test file for word counting.\n");
    fprintf(test_file, "C语言文件操作很有趣。\n");
    fclose(test_file);

    // 统计单词和行数
    count_words_and_lines("test.txt");

    return 0;
}