# 编程挑战 1: 首次适应内存分配器 ⭐

## 背景
首次适应（First Fit）是一种简单的内存分配算法，它从内存的开始处查找第一个足够大的空闲块进行分配。

## 任务
实现一个 `FirstFitMemoryManager` 类，支持以下功能：
- `__init__(size: int)`: 初始化指定大小的内存池
- `allocate(size: int) -> int`: 分配指定大小的内存块，返回起始地址
- `deallocate(address: int)`: 释放指定地址的内存块

## 要求
- 使用列表存储空闲块信息 `(start_address, size)`
- 实现相邻空闲块的合并
- 当内存不足时抛出 `MemoryError` 异常
- 确保分配和释放操作的时间复杂度合理

## 测试用例
```python
mm = FirstFitMemoryManager(100)
addr1 = mm.allocate(30)  # 应该返回 0
addr2 = mm.allocate(20)  # 应该返回 30  
addr3 = mm.allocate(40)  # 应该返回 50
mm.deallocate(addr2)     # 释放地址30的块
addr4 = mm.allocate(25)  # 应该返回 30（使用刚释放的空间）
```

> 💡 **提示**: 维护一个按地址排序的空闲块列表，这样便于合并相邻块。