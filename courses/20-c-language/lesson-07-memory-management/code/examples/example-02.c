#include <stdio.h>
#include <stdlib.h>

// 示例2: 动态数组实现（扩容、缩容）

typedef struct {
    int* data;
    size_t size;      // 当前元素个数
    size_t capacity;  // 当前容量
} DynamicArray;

// 创建动态数组
DynamicArray* create_dynamic_array(size_t initial_capacity) {
    DynamicArray* arr = (DynamicArray*)malloc(sizeof(DynamicArray));
    if (arr == NULL) {
        return NULL;
    }

    arr->data = (int*)malloc(initial_capacity * sizeof(int));
    if (arr->data == NULL) {
        free(arr);
        return NULL;
    }

    arr->size = 0;
    arr->capacity = initial_capacity;
    return arr;
}

// 销毁动态数组
void destroy_dynamic_array(DynamicArray* arr) {
    if (arr != NULL) {
        free(arr->data);
        free(arr);
    }
}

// 扩容函数
int resize_array(DynamicArray* arr, size_t new_capacity) {
    if (new_capacity <= arr->size) {
        return 0; // 不能缩小到小于当前大小
    }

    int* new_data = (int*)realloc(arr->data, new_capacity * sizeof(int));
    if (new_data == NULL) {
        return 0; // 扩容失败
    }

    arr->data = new_data;
    arr->capacity = new_capacity;
    return 1; // 成功
}

// 添加元素
int push_back(DynamicArray* arr, int value) {
    if (arr->size >= arr->capacity) {
        // 需要扩容 - 通常是原来的2倍
        size_t new_capacity = arr->capacity * 2;
        if (!resize_array(arr, new_capacity)) {
            return 0; // 扩容失败
        }
    }

    arr->data[arr->size] = value;
    arr->size++;
    return 1; // 成功
}

// 删除最后一个元素
int pop_back(DynamicArray* arr) {
    if (arr->size == 0) {
        return -1; // 数组为空
    }

    arr->size--;

    // 如果使用率低于25%，考虑缩容
    if (arr->size > 0 && arr->size < arr->capacity / 4) {
        size_t new_capacity = arr->capacity / 2;
        if (new_capacity >= arr->size) {
            resize_array(arr, new_capacity);
        }
    }

    return arr->data[arr->size]; // 返回被删除的元素
}

// 打印数组
void print_array(DynamicArray* arr) {
    printf("数组内容 [size=%zu, capacity=%zu]: ", arr->size, arr->capacity);
    for (size_t i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("\n");
}

int main() {
    printf("=== C语言内存管理示例2: 动态数组 ===\n\n");

    // 创建初始容量为2的动态数组
    DynamicArray* arr = create_dynamic_array(2);
    if (arr == NULL) {
        printf("创建动态数组失败!\n");
        return 1;
    }

    printf("初始状态:\n");
    print_array(arr);

    // 添加元素，触发扩容
    printf("\n添加元素并观察扩容:\n");
    for (int i = 1; i <= 10; i++) {
        if (push_back(arr, i * 10)) {
            printf("添加 %d: ", i * 10);
            print_array(arr);
        } else {
            printf("添加 %d 失败!\n", i * 10);
        }
    }

    // 删除元素，观察可能的缩容
    printf("\n删除元素并观察缩容:\n");
    for (int i = 0; i < 7; i++) {
        int popped = pop_back(arr);
        if (popped != -1) {
            printf("删除 %d: ", popped);
            print_array(arr);
        } else {
            printf("数组已空，无法删除!\n");
        }
    }

    // 测试边界情况
    printf("\n边界情况测试:\n");
    DynamicArray* empty_arr = create_dynamic_array(1);
    if (empty_arr != NULL) {
        printf("空数组: ");
        print_array(empty_arr);

        // 尝试从空数组删除
        int result = pop_back(empty_arr);
        if (result == -1) {
            printf("正确处理了空数组删除操作\n");
        }

        destroy_dynamic_array(empty_arr);
    }

    // 清理
    destroy_dynamic_array(arr);

    printf("\n=== 示例2结束 ===\n");
    return 0;
}