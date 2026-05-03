#include <stdio.h>

/**
 * 解决方案3：二维数组指针操作
 * 计算二维数组所有元素的和
 */

// 方法1：使用数组指针
int sum_2d_array_v1(int (*matrix)[5], int rows) {
    int total = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < 5; j++) {
            total += matrix[i][j];
        }
    }
    return total;
}

// 方法2：使用普通指针遍历整个内存块
int sum_2d_array_v2(int *matrix, int rows, int cols) {
    int total = 0;
    for (int i = 0; i < rows * cols; i++) {
        total += matrix[i];
    }
    return total;
}

// 方法3：使用指针算术（更复杂但展示了指针技巧）
int sum_2d_array_v3(int rows, int cols, ...) {
    // 这种方法不太实用，仅作演示
    // 实际中我们通常知道列数或使用其他方式
    return -1;
}

// 通用版本：适用于任何大小的二维数组
int sum_2d_generic(int **matrix, int rows, int cols) {
    int total = 0;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            total += matrix[i][j];
        }
    }
    return total;
}

int main() {
    // 定义一个3x5的二维数组
    int matrix[3][5] = {
        {1, 2, 3, 4, 5},
        {6, 7, 8, 9, 10},
        {11, 12, 13, 14, 15}
    };

    printf("二维数组内容:\n");
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 5; j++) {
            printf("%3d ", matrix[i][j]);
        }
        printf("\n");
    }

    // 方法1：使用数组指针
    int sum1 = sum_2d_array_v1(matrix, 3);
    printf("\n方法1结果（数组指针）: %d\n", sum1);

    // 方法2：使用普通指针
    int sum2 = sum_2d_array_v2(&matrix[0][0], 3, 5);
    printf("方法2结果（普通指针）: %d\n", sum2);

    // 验证结果
    if (sum1 == sum2) {
        printf("两种方法结果一致！总和为: %d\n", sum1);
    } else {
        printf("结果不一致，请检查代码！\n");
    }

    // 演示如何传递给通用函数（需要额外的指针数组）
    int *row_pointers[3] = {matrix[0], matrix[1], matrix[2]};
    int sum3 = sum_2d_generic(row_pointers, 3, 5);
    printf("通用方法结果: %d\n", sum3);

    return 0;
}