#include <stdio.h>

// 使用位域表示一周的工作日安排（练习3的解决方案）
struct WorkSchedule {
    unsigned int monday : 1;    // 1 = 工作, 0 = 休息
    unsigned int tuesday : 1;
    unsigned int wednesday : 1;
    unsigned int thursday : 1;
    unsigned int friday : 1;
    unsigned int saturday : 1;
    unsigned int sunday : 1;
    unsigned int reserved : 25; // 填充到32位
};

// 设置特定工作日的状态
void set_day(struct WorkSchedule *schedule, int day_index, int is_work) {
    switch (day_index) {
        case 0: schedule->monday = is_work; break;
        case 1: schedule->tuesday = is_work; break;
        case 2: schedule->wednesday = is_work; break;
        case 3: schedule->thursday = is_work; break;
        case 4: schedule->friday = is_work; break;
        case 5: schedule->saturday = is_work; break;
        case 6: schedule->sunday = is_work; break;
        default: printf("错误：星期几必须是0-6\n");
    }
}

// 获取特定工作日的状态
int get_day(const struct WorkSchedule *schedule, int day_index) {
    switch (day_index) {
        case 0: return schedule->monday;
        case 1: return schedule->tuesday;
        case 2: return schedule->wednesday;
        case 3: return schedule->thursday;
        case 4: return schedule->friday;
        case 5: return schedule->saturday;
        case 6: return schedule->sunday;
        default: return -1;
    }
}

// 打印完整的工作安排
void print_schedule(const struct WorkSchedule *schedule) {
    const char* weekdays[] = {"周一", "周二", "周三", "周四", "周五", "周六", "周日"};

    printf("工作安排详情:\n");
    for (int i = 0; i < 7; i++) {
        printf("%s: %s\n", weekdays[i], get_day(schedule, i) ? "工作" : "休息");
    }
}

// 计算总工作天数
int count_workdays(const struct WorkSchedule *schedule) {
    return schedule->monday + schedule->tuesday + schedule->wednesday +
           schedule->thursday + schedule->friday + schedule->saturday +
           schedule->sunday;
}

int main() {
    printf("=== 位域应用：工作日安排系统 ===\n\n");

    // 标准朝九晚五工作制
    struct WorkSchedule standard = {1, 1, 1, 1, 1, 0, 0, 0};
    printf("标准工作制:\n");
    print_schedule(&standard);
    printf("每周工作 %d 天\n\n", count_workdays(&standard));

    // 灵活工作制示例
    struct WorkSchedule flexible = {0}; // 初始化所有为0（休息）

    // 设置工作日：周一、周三、周五、周日工作
    set_day(&flexible, 0, 1); // 周一
    set_day(&flexible, 2, 1); // 周三
    set_day(&flexible, 4, 1); // 周五
    set_day(&flexible, 6, 1); // 周日

    printf("灵活工作制:\n");
    print_schedule(&flexible);
    printf("每周工作 %d 天\n\n", count_workdays(&flexible));

    // 内存效率展示
    printf("=== 内存效率对比 ===\n");
    printf("位域结构体大小: %zu 字节\n", sizeof(struct WorkSchedule));
    printf("布尔数组大小: %zu 字节\n", 7 * sizeof(char)); // 最小可能
    printf("实际节省空间，且语义更清晰！\n");

    return 0;
}