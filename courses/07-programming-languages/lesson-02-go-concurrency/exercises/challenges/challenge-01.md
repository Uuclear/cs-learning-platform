# 挑战1: 并发安全的缓存实现

## 背景
在高并发场景下，缓存是提升性能的重要手段。但是简单的map在并发读写时会出现数据竞争问题。

## 任务
实现一个并发安全的缓存，支持以下操作：
- `Get(key string) (interface{}, bool)` - 获取缓存值
- `Set(key string, value interface{})` - 设置缓存值
- `Delete(key string)` - 删除缓存项

## 要求
1. 使用Go标准库实现，不允许使用第三方包
2. 必须保证并发安全性
3. 支持任意类型的值存储
4. 提供完整的测试用例验证并发安全性

## 提示
- 考虑使用`sync.RWMutex`来优化读性能
- 可以使用`map[string]interface{}`作为底层存储
- 测试时可以使用`go test -race`来检测数据竞争

## 验收标准
- 代码通过所有测试用例
- `go test -race`不报告数据竞争
- API设计合理，易于使用