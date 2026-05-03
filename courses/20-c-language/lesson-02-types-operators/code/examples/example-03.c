#include <stdio.h>
#include <limits.h>

int main() {
    // 演示整数溢出
    printf("=== 整数溢出演示 ===\n");

    // 有符号整数溢出（未定义行为，但通常会回绕）
    int max_int = INT_MAX;
    printf("INT_MAX = %d\n", max_int);
    printf("INT_MAX + 1 = %d (溢出!)\n", max_int + 1);

    // 无符号整数溢出（定义良好的回绕行为）
    unsigned int max_uint = UINT_MAX;
    printf("\nUINT_MAX = %u\n", max_uint);
    printf("UINT_MAX + 1 = %u (回绕到0)\n", max_uint + 1);

    // 演示浮点精度问题
    printf("\n=== 浮点精度问题演示 ===\n");
    float a = 0.1f;
    float b = 0.2f;
    float sum = a + b;
    float expected = 0.3f;

    printf("0.1f + 0.2f = %.10f\n", sum);
    printf("0.3f = %.10f\n", expected);
    printf("相等吗? %s\n", (sum == expected) ? "是" : "否");

    // 使用double获得更高精度
    double da = 0.1;
    double db = 0.2;
    double dsum = da + db;
    double dexpected = 0.3;

    printf("\n使用double:\n");
    printf("0.1 + 0.2 = %.17f\n", dsum);
    printf("0.3 = %.17f\n", dexpected);
    printf("相等吗? %s\n", (dsum == dexpected) ? "是" : "否");

    // 演示为什么不应该直接比较浮点数
    printf("\n=== 浮点数比较的正确方法 ===\n");
    #define EPSILON 1e-6
    if (fabs(sum - expected) < EPSILON) {
        printf("使用epsilon比较: 认为相等\n");
    } else {
        printf("使用epsilon比较: 不相等\n");
    }

    return 0;
}