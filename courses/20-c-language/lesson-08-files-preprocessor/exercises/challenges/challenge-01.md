# 挑战 1：配置文件解析器

## 背景
许多应用程序都需要读取配置文件来设置运行时参数。配置文件通常采用键值对的格式，如：
```
# 数据库配置
database.host=localhost
database.port=5432
database.name=myapp

# 应用设置
app.debug=true
app.max_connections=100
app.log_level=info
```

## 任务要求
编写一个C程序，能够：
1. 读取指定的配置文件
2. 解析键值对（忽略注释行和空行）
3. 提供函数来获取特定配置项的值
4. 支持字符串和整数值的获取

## 具体实现
创建以下函数：
```c
// 初始化配置解析器，读取配置文件
int config_init(const char *filename);

// 获取字符串配置值
const char* config_get_string(const char *key, const char *default_value);

// 获取整数配置值
int config_get_int(const char *key, int default_value);

// 清理配置数据
void config_cleanup(void);
```

## 示例使用
```c
if (config_init("app.conf") == 0) {
    const char *host = config_get_string("database.host", "localhost");
    int port = config_get_int("database.port", 5432);
    int debug = config_get_int("app.debug", 0);
    
    printf("数据库: %s:%d, 调试模式: %s\n", 
           host, port, debug ? "开启" : "关闭");
    
    config_cleanup();
}
```

## 评分标准
- [ ] 正确处理注释行（以#开头）
- [ ] 正确处理空行和只有空白字符的行
- [ ] 正确解析键值对（键和值之间的等号）
- [ ] 支持嵌套键名（如 database.host）
- [ ] 内存管理正确（无内存泄漏）
- [ ] 错误处理完善（文件不存在、格式错误等）
- [ ] 提供合理的默认值机制

## 提示
- 使用 `strchr()` 函数查找等号位置
- 使用 `strdup()` 复制字符串（记得释放内存）
- 考虑使用链表或哈希表存储配置项
- 注意处理值末尾的换行符