# 编程挑战 2：文本编辑器的撤销/重做功能

## 题目描述

实现一个支持撤销（undo）和重做（redo）操作的简单文本编辑器。

编辑器需要支持以下操作：
- `insert(pos, text)`: 在指定位置插入文本
- `delete(pos, length)`: 从指定位置删除指定长度的文本
- `undo()`: 撤销上一次操作
- `redo()`: 重做上一次被撤销的操作

## 要求

实现 `TextEditor` 类，包含以下方法：

```python
class TextEditor:
    def __init__(self, initial_text: str = ""):
        """初始化编辑器"""
        pass
    
    def insert(self, pos: int, text: str) -> None:
        """在位置pos插入text"""
        pass
    
    def delete(self, pos: int, length: int) -> str:
        """删除从pos开始length个字符，返回删除的文本"""
        pass
    
    def undo(self) -> bool:
        """撤销上一次操作，成功返回True，否则False"""
        pass
    
    def redo(self) -> bool:
        """重做上一次撤销的操作，成功返回True，否则False"""
        pass
    
    def get_text(self) -> str:
        """获取当前文本"""
        pass
```

## 示例

```python
editor = TextEditor("Hello")
editor.insert(5, " World")      # "Hello World"
editor.delete(5, 6)             # "Hello"
editor.undo()                   # "Hello World"
editor.redo()                   # "Hello"
print(editor.get_text())        # "Hello"
```

## 约束条件

- 所有位置参数都是有效的（0 <= pos <= len(current_text)）
- 删除长度不会超过剩余文本长度
- 支持连续多次undo/redo操作
- 操作历史应该有限制（比如最多保存100个操作）

## 提示

💡 **使用两个栈**：
- 一个栈存储undo操作（操作历史）
- 另一个栈存储redo操作（被撤销的操作）
- 每次执行新操作时，清空redo栈

💡 **操作表示**：
- 可以将每个操作表示为字典或命名元组
- 包含操作类型、参数、以及逆操作所需的信息