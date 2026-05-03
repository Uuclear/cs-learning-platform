#include <stdio.h>
#include <string.h>

// 定义数据类型枚举（用于跟踪当前存储的数据类型）
typedef enum {
    TYPE_INT,
    TYPE_FLOAT,
    TYPE_STRING
} DataType;

// 联合体：可以存储整数、浮点数或字符串
typedef union {
    int integer;
    float floating;
    char string[21];  // 最多20个字符的字符串 + null终止符
} DataUnion;

// 主结构体：包含类型标签和联合体数据
typedef struct {
    DataType type;      // 当前存储的数据类型
    DataUnion data;     // 实际数据
} TypedData;

// 设置整数值
void set_int(TypedData *td, int value) {
    td->type = TYPE_INT;
    td->data.integer = value;
}

// 设置浮点数值
void set_float(TypedData *td, float value) {
    td->type = TYPE_FLOAT;
    td->data.floating = value;
}

// 设置字符串值
void set_string(TypedData *td, const char* value) {
    td->type = TYPE_STRING;
    strncpy(td->data.string, value, sizeof(td->data.string) - 1);
    td->data.string[sizeof(td->data.string) - 1] = '\0'; // 确保安全终止
}

// 打印数据（根据类型安全地打印）
void print_data(const TypedData *td) {
    switch (td->type) {
        case TYPE_INT:
            printf("整数: %d\n", td->data.integer);
            break;
        case TYPE_FLOAT:
            printf("浮点数: %.3f\n", td->data.floating);
            break;
        case TYPE_STRING:
            printf("字符串: \"%s\"\n", td->data.string);
            break;
        default:
            printf("错误：未知数据类型！\n");
    }
}

int main() {
    printf("=== 联合体处理不同类型数据的解决方案 ===\n\n");

    // 创建TypedData实例
    TypedData myData;

    // 测试整数
    set_int(&myData, 42);
    printf("存储整数 42:\n");
    print_data(&myData);

    // 测试浮点数
    set_float(&myData, 3.14159f);
    printf("\n存储浮点数 3.14159:\n");
    print_data(&myData);

    // 测试字符串
    set_string(&myData, "Hello, C!");
    printf("\n存储字符串 \"Hello, C!\":\n");
    print_data(&myData);

    // 创建混合数据数组
    printf("\n=== 混合数据数组演示 ===\n");
    TypedData dataArray[5];

    set_int(&dataArray[0], 100);
    set_float(&dataArray[1], 2.718f);
    set_string(&dataArray[2], "Programming");
    set_int(&dataArray[3], -999);
    set_float(&dataArray[4], 0.0f);

    for (int i = 0; i < 5; i++) {
        printf("数组[%d]: ", i);
        print_data(&dataArray[i]);
    }

    // 显示内存使用情况
    printf("\n=== 内存使用分析 ===\n");
    printf("联合体大小: %zu 字节\n", sizeof(DataUnion));
    printf("完整结构体大小: %zu 字节\n", sizeof(TypedData));
    printf("字符串缓冲区大小: %zu 字节\n", sizeof(((DataUnion*)0)->string));

    return 0;
}