# 挑战 2：跨平台日志系统

## 背景
在实际开发中，我们需要一个灵活的日志系统，能够：
- 在不同平台上正常工作
- 支持不同的日志级别（DEBUG, INFO, WARN, ERROR）
- 可以在编译时控制日志级别（减少发布版本的开销）
- 支持同时输出到文件和控制台

## 任务要求
创建一个头文件 `logger.h` 和实现文件 `logger.c`，实现以下功能：

### 头文件接口
```c
// 日志级别定义
#define LOG_LEVEL_DEBUG 0
#define LOG_LEVEL_INFO  1  
#define LOG_LEVEL_WARN  2
#define LOG_LEVEL_ERROR 3

// 默认日志级别（可通过编译参数覆盖）
#ifndef LOG_LEVEL
#define LOG_LEVEL LOG_LEVEL_INFO
#endif

// 日志宏（自动包含文件名和行号）
#define LOG_DEBUG(fmt, ...)   log_message(LOG_LEVEL_DEBUG, __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define LOG_INFO(fmt, ...)    log_message(LOG_LEVEL_INFO,  __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define LOG_WARN(fmt, ...)    log_message(LOG_LEVEL_WARN,  __FILE__, __LINE__, fmt, ##__VA_ARGS__)
#define LOG_ERROR(fmt, ...)   log_message(LOG_LEVEL_ERROR, __FILE__, __LINE__, fmt, ##__VA_ARGS__)

// 初始化日志系统
int logger_init(const char *logfile);

// 设置是否同时输出到控制台
void logger_set_console_output(int enable);

// 关闭日志系统
void logger_close(void);

// 内部函数（不应直接调用）
void log_message(int level, const char *file, int line, const char *fmt, ...);
```

### 功能要求
1. **条件编译**：只有当日志级别 >= 编译时设置的 `LOG_LEVEL` 时，才会生成日志代码
2. **跨平台时间格式**：正确获取当前时间并格式化
3. **文件输出**：将日志写入指定的文件
4. **控制台输出**：可选择性地同时输出到控制台
5. **线程安全**：使用互斥锁保护文件写入操作（如果支持多线程）

## 示例使用
```c
#include "logger.h"

int main() {
    // 初始化日志系统
    if (logger_init("app.log") != 0) {
        fprintf(stderr, "无法初始化日志系统\n");
        return 1;
    }
    
    logger_set_console_output(1); // 同时输出到控制台
    
    LOG_INFO("应用程序启动");
    LOG_DEBUG("调试信息: 用户ID=%d", 12345);
    LOG_WARN("警告: 磁盘空间不足");
    LOG_ERROR("错误: 数据库连接失败");
    
    logger_close();
    return 0;
}
```

## 编译测试
测试不同编译配置：
```bash
# 调试版本（包含所有日志）
gcc -DLOG_LEVEL=0 -o app_debug main.c logger.c

# 发布版本（只包含WARN和ERROR）
gcc -DLOG_LEVEL=2 -o app_release main.c logger.c

# Windows编译
cl /DLOG_LEVEL=1 /Feapp.exe main.c logger.c
```

## 评分标准
- [ ] 正确实现条件编译，高级别日志在低级别编译时不会产生代码
- [ ] 跨平台兼容性（Windows/Linux/macOS）
- [ ] 时间戳格式正确且可读
- [ ] 文件和控制台输出功能正常
- [ ] 内存和资源管理正确（无泄漏）
- [ ] 错误处理完善
- [ ] 代码结构清晰，注释充分

## 提示
- 使用 `#if LOG_LEVEL <= LOG_LEVEL_DEBUG` 进行条件编译
- Windows使用 `_WIN32` 宏，Unix-like系统使用 `__unix__` 或特定系统宏
- 使用 `localtime()` 和 `strftime()` 格式化时间
- 考虑使用 `flockfile()`/`funlockfile()` 或平台特定的互斥锁实现线程安全