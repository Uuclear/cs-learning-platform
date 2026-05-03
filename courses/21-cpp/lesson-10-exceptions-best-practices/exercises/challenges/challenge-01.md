# 挑战 1：实现异常安全的配置文件解析器

## 背景
你正在开发一个应用程序，需要从JSON格式的配置文件中读取设置。配置文件可能包含无效数据、格式错误或缺失必需字段。

## 任务要求

### 1. 异常类设计
创建以下自定义异常类层次结构：
- `ConfigException`（基类，继承自`std::exception`）
  - `FileReadException`（文件读取失败）
  - `JsonParseException`（JSON解析错误）
  - `ValidationException`（配置验证失败）

每个异常类都应该：
- 提供有意义的错误消息
- 正确实现`what()`方法（`const noexcept`）
- 包含相关的上下文信息（如文件名、字段名等）

### 2. 配置解析器实现
实现`ConfigParser`类，包含以下功能：

```cpp
class ConfigParser {
public:
    // 从文件加载配置
    void loadFromFile(const std::string& filename);
    
    // 从字符串加载配置  
    void loadFromString(const std::string& json_string);
    
    // 获取配置值（模板方法）
    template<typename T>
    T getValue(const std::string& key) const;
    
    // 获取必需的配置值，如果不存在则抛出异常
    template<typename T>
    T getRequiredValue(const std::string& key) const;
    
    // 验证配置完整性
    void validate() const;
    
private:
    std::map<std::string, std::any> config_data;
};
```

### 3. 异常安全保证
- **强异常安全保证**：所有修改操作（loadFromFile, loadFromString）必须提供强异常安全保证
- **不抛出保证**：所有查询操作（getValue）应该是`noexcept`的，但`getRequiredValue`可以抛出异常
- **RAII**：正确管理文件资源，确保即使发生异常文件也会被正确关闭

### 4. 使用示例
编写一个`main()`函数演示以下场景：
1. 成功加载有效配置文件
2. 处理文件不存在的情况
3. 处理JSON格式错误
4. 处理必需字段缺失
5. 处理类型转换错误

## 评估标准
- 异常类设计的合理性和完整性
- 异常安全级别的正确实现
- 代码的健壮性和可维护性
- 错误消息的清晰度和有用性
- 是否遵循现代C++最佳实践（智能指针、移动语义等）

## 提示
- 可以使用简单的JSON解析逻辑，重点在于异常处理
- 考虑使用`std::optional`来区分"值不存在"和"值存在但为空"
- 记住析构函数必须是`noexcept`的
- 移动构造函数和移动赋值运算符应该声明为`noexcept`
