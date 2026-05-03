# TypeScript类型挑战1：实现泛型数据结构

在这个挑战中，你需要使用Python的typing模块来模拟TypeScript的泛型特性。

## 任务要求

1. **创建一个泛型队列类 `Queue[T]`**
   - 实现 `enqueue(item: T)` 方法添加元素到队尾
   - 实现 `dequeue() -> Optional[T]` 方法从队首移除并返回元素
   - 实现 `is_empty() -> bool` 方法检查队列是否为空
   - 实现 `size() -> int` 方法返回队列大小

2. **创建一个泛型字典验证器**
   - 函数 `create_validator(schema: Dict[str, type]) -> callable`
   - 返回的验证器函数接收一个字典并根据schema验证类型
   - 如果所有字段都匹配类型则返回True，否则返回False

3. **测试你的实现**
   - 创建字符串队列和数字队列，测试基本操作
   - 创建用户数据验证器，验证包含name(str)、age(int)、email(str)的用户对象

## 提示

- 使用 `from typing import TypeVar, Generic, Optional, Dict, List`
- 定义类型变量：`T = TypeVar('T')`
- 泛型类继承：`class Queue(Generic[T]):`
- 使用 `isinstance()` 进行运行时类型检查

## 预期输出示例

```
🎯 泛型队列测试
字符串队列: ['apple', 'banana']
数字队列: [1, 2, 3]

🎯 验证器测试  
有效用户: True
无效用户: False
```

祝你好运！记住TypeScript的核心思想：**类型安全 + 开发体验**。