#include <stdio.h>
#include <stdlib.h>

// 解决方案2: 完整的动态数组实现

typedef struct {
    int* data;
    size_t size;      // 当前元素个数
    size_t capacity;  // 当前容量
} DynamicArray;

// 创建动态数组
DynamicArray* create_dynamic_array(size_t initial_capacity) {
    if (initial_capacity == 0) {
        initial_capacity = 1; // 至少分配1个元素
    }

    DynamicArray* arr = (DynamicArray*)malloc(sizeof(DynamicArray));
    if (arr == NULL) {
        return NULL;
    }

    arr->data = (int*)calloc(initial_capacity, sizeof(int)); // 使用calloc确保初始化为0
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

// 获取数组大小
size_t get_size(DynamicArray* arr) {
    return arr ? arr->size : 0;
}

// 获取数组容量
size_t get_capacity(DynamicArray* arr) {
    return arr ? arr->capacity : 0;
}

// 检查数组是否为空
int is_empty(DynamicArray* arr) {
    return arr == NULL || arr->size == 0;
}

// 访问元素（带边界检查）
int* at(DynamicArray* arr, size_t index) {
    if (arr == NULL || index >= arr->size) {
        return NULL;
    }
    return &arr->data[index];
}

// 扩容函数
int resize_array(DynamicArray* arr, size_t new_capacity) {
    if (arr == NULL || new_capacity == 0) {
        return 0;
    }

    if (new_capacity <= arr->size) {
        return 0; // 不能缩小到小于当前大小
    }

    int* new_data = (int*)realloc(arr->data, new_capacity * sizeof(int));
    if (new_data == NULL) {
        return 0; // 扩容失败，原来的内存仍然有效
    }

    // 如果扩容了，初始化新增的部分为0
    if (new_capacity > arr->capacity) {
        for (size_t i = arr->capacity; i < new_capacity; i++) {
            new_data[i] = 0;
        }
    }

    arr->data = new_data;
    arr->capacity = new_capacity;
    return 1;
}

// 添加元素到末尾
int push_back(DynamicArray* arr, int value) {
    if (arr == NULL) {
        return 0;
    }

    if (arr->size >= arr->capacity) {
        // 扩容策略：如果容量为0则设为1，否则翻倍
        size_t new_capacity = (arr->capacity == 0) ? 1 : arr->capacity * 2;
        if (!resize_array(arr, new_capacity)) {
            return 0; // 扩容失败
        }
    }

    arr->data[arr->size] = value;
    arr->size++;
    return 1;
}

// 在指定位置插入元素
int insert(DynamicArray* arr, size_t index, int value) {
    if (arr == NULL || index > arr->size) {
        return 0; // 索引越界
    }

    if (arr->size >= arr->capacity) {
        size_t new_capacity = (arr->capacity == 0) ? 1 : arr->capacity * 2;
        if (!resize_array(arr, new_capacity)) {
            return 0;
        }
    }

    // 将index及之后的元素向后移动
    for (size_t i = arr->size; i > index; i--) {
        arr->data[i] = arr->data[i - 1];
    }

    arr->data[index] = value;
    arr->size++;
    return 1;
}

// 删除最后一个元素
int pop_back(DynamicArray* arr) {
    if (is_empty(arr)) {
        return -1; // 数组为空，返回错误码
    }

    int value = arr->data[arr->size - 1];
    arr->size--;

    // 缩容策略：当使用率低于25%且容量大于初始容量时缩容
    if (arr->capacity > 4 && arr->size < arr->capacity / 4) {
        size_t new_capacity = arr->capacity / 2;
        if (new_capacity >= 4) { // 保持最小容量为4
            resize_array(arr, new_capacity);
        }
    }

    return value;
}

// 删除指定位置的元素
int remove_at(DynamicArray* arr, size_t index) {
    if (arr == NULL || index >= arr->size) {
        return -1; // 索引越界
    }

    int value = arr->data[index];

    // 将index之后的元素向前移动
    for (size_t i = index; i < arr->size - 1; i++) {
        arr->data[i] = arr->data[i + 1];
    }

    arr->size--;

    // 检查是否需要缩容
    if (arr->capacity > 4 && arr->size < arr->capacity / 4) {
        size_t new_capacity = arr->capacity / 2;
        if (new_capacity >= 4) {
            resize_array(arr, new_capacity);
        }
    }

    return value;
}

// 查找元素
int find(DynamicArray* arr, int value) {
    if (arr == NULL) {
        return -1;
    }

    for (size_t i = 0; i < arr->size; i++) {
        if (arr->data[i] == value) {
            return (int)i;
        }
    }
    return -1; // 未找到
}

// 打印数组
void print_array(DynamicArray* arr) {
    if (arr == NULL) {
        printf("NULL array\n");
        return;
    }

    printf("[size=%zu, capacity=%zu]: ", arr->size, arr->capacity);
    for (size_t i = 0; i < arr->size; i++) {
        printf("%d ", arr->data[i]);
    }
    printf("\n");
}

// 清空数组
void clear(DynamicArray* arr) {
    if (arr != NULL) {
        arr->size = 0;
        // 可选：重置容量到初始大小
        // resize_array(arr, 4);
    }
}

int main() {
    printf("=== C语言内存管理解决方案2: 完整动态数组 ===\n\n");

    // 创建动态数组
    DynamicArray* arr = create_dynamic_array(2);
    if (arr == NULL) {
        fprintf(stderr, "创建动态数组失败!\n");
        return 1;
    }

    printf("初始状态:\n");
    print_array(arr);

    // 测试push_back
    printf("\n测试push_back:\n");
    for (int i = 1; i <= 8; i++) {
        if (push_back(arr, i * 10)) {
            printf("添加 %d: ", i * 10);
            print_array(arr);
        } else {
            fprintf(stderr, "添加 %d 失败!\n", i * 10);
        }
    }

    // 测试at和find
    printf("\n测试访问和查找:\n");
    int* val = at(arr, 3);
    if (val != NULL) {
        printf("索引3的值: %d\n", *val);
    }

    int pos = find(arr, 50);
    printf("值50的位置: %d\n", pos);

    // 测试insert
    printf("\n测试insert:\n");
    if (insert(arr, 2, 999)) {
        printf("在索引2插入999: ");
        print_array(arr);
    }

    // 测试remove_at
    printf("\n测试remove_at:\n");
    int removed = remove_at(arr, 2);
    if (removed != -1) {
        printf("删除索引2的元素(%d): ", removed);
        print_array(arr);
    }

    // 测试pop_back
    printf("\n测试pop_back:\n");
    for (int i = 0; i < 3; i++) {
        int popped = pop_back(arr);
        if (popped != -1) {
            printf("弹出 %d: ", popped);
            print_array(arr);
        }
    }

    // 测试clear
    printf("\n测试clear:\n");
    clear(arr);
    printf("清空后: ");
    print_array(arr);

    // 重新添加一些元素
    push_back(arr, 100);
    push_back(arr, 200);
    push_back(arr, 300);
    printf("重新添加后: ");
    print_array(arr);

    // 清理
    destroy_dynamic_array(arr);

    printf("\n=== 解决方案2结束 - 动态数组完整实现! ===\n");
    return 0;
}