// solution-02-main.c
#include <stdio.h>

int calculate_sum(int a, int b) {
    return a + b;
}

int main() {
    int x = 15, y = 25;
    int sum = calculate_sum(x, y);
    printf("计算结果：%d + %d = %d\n", x, y, sum);
    return 0;
}