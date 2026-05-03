# 挑战 2：实现一个配置文件解析器

## 目标
使用枚举和结构体创建一个简单的配置文件解析器，能够处理不同类型的配置值。

## 要求

### 1. 定义配置值类型枚举
创建一个 `ConfigValue` 枚举，支持以下变体：
- `String(String)`
- `Integer(i64)`
- `Boolean(bool)`
- `Float(f64)`
- `Array(Vec<ConfigValue>)`
- `Object(std::collections::HashMap<String, ConfigValue>)`

### 2. 定义配置错误枚举
创建一个 `ConfigError` 枚举，包含以下变体：
- `ParseError(String)`
- `TypeError(String)`
- `NotFoundError(String)`
- `IoError(std::io::Error)`

### 3. 实现配置解析函数
实现以下函数：

```rust
fn parse_config_value(input: &str) -> Result<ConfigValue, ConfigError>
```

这个函数应该能够解析简单的配置值，例如：
- `"hello"` → `ConfigValue::String("hello".to_string())`
- `"42"` → `ConfigValue::Integer(42)`
- `"true"` → `ConfigValue::Boolean(true)`
- `"3.14"` → `ConfigValue::Float(3.14)`

### 4. 实现配置访问方法
为 `ConfigValue` 实现以下方法：

- `as_string(&self) -> Option<&String>`
- `as_integer(&self) -> Option<&i64>`
- `as_boolean(&self) -> Option<&bool>`
- `as_float(&self) -> Option<&f64>`

这些方法应该使用模式匹配来安全地提取值。

### 5. 创建配置管理器结构体
创建一个 `ConfigManager` 结构体：
```rust
struct ConfigManager {
    config: std::collections::HashMap<String, ConfigValue>,
}
```

并实现以下方法：
- `new() -> ConfigManager`
- `set_value(&mut self, key: String, value: ConfigValue)`
- `get_value(&self, key: &str) -> Option<&ConfigValue>`
- `get_string(&self, key: &str) -> Result<&String, ConfigError>`
- `get_integer(&self, key: &str) -> Result<&i64, ConfigError>`

### 6. 额外挑战
- 实现从文件读取配置的功能
- 支持嵌套配置（如 `database.host` 访问）
- 添加类型转换功能（如将字符串 "42" 转换为整数）

## 提示
- 使用 `Result` 和 `Option` 来处理可能的错误和缺失值
- 考虑使用递归来处理嵌套的对象和数组
- 利用 Rust 的模式匹配来简化类型检查