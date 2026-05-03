#include <stdio.h>
#include <stdint.h>

// 联合体示例：不同类型的数据共享内存
union Data {
    int integer;
    float floating;
    char string[20];
};

// 位域示例：紧凑存储标志位
struct Flags {
    unsigned int is_valid : 1;      // 1 bit
    unsigned int is_active : 1;     // 1 bit
    unsigned int priority : 3;      // 3 bits (0-7)
    unsigned int category : 4;      // 4 bits (0-15)
    unsigned int reserved : 23;     // 剩余的23位
};

// 联合体示例：IP地址的不同表示方式
union IPAddress {
    uint8_t bytes[4];               // 4个字节
    uint32_t value;                 // 作为一个32位整数
};

int main() {
    printf("=== 联合体演示 ===\n");

    // 联合体Data的使用
    union Data data;

    // 存储整数
    data.integer = 12345;
    printf("存储整数后: integer=%d, floating=%.2f\n",
           data.integer, data.floating);

    // 存储浮点数（会覆盖整数）
    data.floating = 3.14159f;
    printf("存储浮点数后: integer=%d, floating=%.2f\n",
           data.integer, data.floating);

    // 存储字符串（会覆盖前面的数据）
    strcpy(data.string, "Hello");
    printf("存储字符串后: string=\"%s\", integer=%d\n",
           data.string, data.integer);

    printf("\n=== 位域演示 ===\n");

    // 位域Flags的使用
    struct Flags flags = {1, 1, 5, 10, 0};
    printf("Flags - valid: %u, active: %u, priority: %u, category: %u\n",
           flags.is_valid, flags.is_active, flags.priority, flags.category);

    // 修改位域值
    flags.priority = 7;  // 最大值为7（3位）
    flags.category = 15; // 最大值为15（4位）
    printf("修改后 - priority: %u, category: %u\n",
           flags.priority, flags.category);

    printf("\n=== IP地址联合体演示 ===\n");

    // IP地址联合体的使用
    union IPAddress ip;
    ip.value = 0x12345678;  // 设置为十六进制值

    printf("IP作为整数: 0x%08X\n", ip.value);
    printf("IP作为字节: %d.%d.%d.%d\n",
           ip.bytes[0], ip.bytes[1], ip.bytes[2], ip.bytes[3]);

    // 注意字节序：在小端系统中，最低有效字节存储在最低地址
    printf("注意：字节序可能因系统而异！\n");

    return 0;
}