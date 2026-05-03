# TypeScript类型挑战2：高级类型操作

在这个挑战中，你将实现更复杂的TypeScript类型模式，包括联合类型、交叉类型和条件类型。

## 任务要求

1. **实现API响应包装器**
   - 创建泛型类 `ApiResponse[T]` 
   - 包含 `success: bool`, `data: Optional[T]`, `error: Optional[str]` 属性
   - 实现 `map(func: Callable[[T], V]) -> ApiResponse[V]` 方法（成功时转换数据）
   - 实现 `flat_map(func: Callable[[T], ApiResponse[V]]) -> ApiResponse[V]` 方法

2. **实现类型守卫函数**
   - `is_string(value: Any) -> bool`: 检查是否为字符串
   - `is_number(value: Any) -> bool`: 检查是否为数字（int或float）
   - `has_property(obj: Any, prop: str) -> bool`: 检查对象是否有指定属性

3. **创建配置管理器**
   - 使用Protocol定义 `ConfigProvider` 接口，包含 `get(key: str) -> Any` 方法
   - 实现 `DictConfigProvider` 类，使用字典存储配置
   - 实现 `JsonConfigProvider` 类，从JSON文件读取配置
   - 创建函数 `get_config_value(provider: ConfigProvider, key: str, default: T) -> T`

4. **测试所有功能**
   - 测试API响应的map和flat_map操作
   - 测试类型守卫函数
   - 测试两种配置提供者

## 提示

- 使用 `from typing import Protocol, runtime_checkable, Callable, Any`
- 对于条件类型，使用if/else语句结合类型守卫
- API响应的map方法只在success=True时应用转换函数
- flat_map方法用于处理返回另一个ApiResponse的转换函数

## 预期输出示例

```
🎯 API响应测试
原始响应: 成功: {'id': 1, 'name': 'Alice'}
Map结果: 成功: Alice
FlatMap结果: 成功: USER_ALICE

🎯 类型守卫测试
"hello" 是字符串: True
42 是数字: True
[] 有 length 属性: True

🎯 配置提供者测试
字典配置: value1
JSON配置: json_value
```

这个挑战将帮助你深入理解TypeScript的高级类型系统！