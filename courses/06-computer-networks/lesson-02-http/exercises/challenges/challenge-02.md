# 编程挑战2: HTTP缓存模拟器

## 背景
HTTP缓存是Web性能优化的重要机制。通过缓存，浏览器可以避免重复下载相同的资源，从而提高页面加载速度。

## 任务
创建一个简单的HTTP缓存模拟器类 `HTTPCacheSimulator`，模拟浏览器的缓存行为。

## 要求
实现以下方法：

1. **`get(url)`**: 获取URL对应的资源
   - 如果URL在缓存中且未过期，返回缓存的资源和状态码304（Not Modified）
   - 如果不在缓存中或已过期，模拟从服务器获取资源，返回状态码200和资源内容
   - 将新获取的资源存储到缓存中，并设置过期时间（假设所有资源的缓存时间为60秒）

2. **`clear()`**: 清空所有缓存

3. **`get_cache_info()`**: 返回缓存统计信息，包括缓存项数量和总大小

## 资源模拟
- 使用字典模拟服务器资源：`{'https://example.com/page1': 'Page 1 content', ...}`
- 资源内容可以是简单的字符串
- 使用时间戳记录缓存时间

## 示例使用
```python
cache = HTTPCacheSimulator()

# 第一次访问 - 从服务器获取
status, content = cache.get('https://example.com/page1')
print(f"状态: {status}, 内容: {content}")  # 状态: 200, 内容: Page 1 content

# 立即再次访问 - 从缓存获取
status, content = cache.get('https://example.com/page1')
print(f"状态: {status}, 内容: {content}")  # 状态: 304, 内容: Page 1 content

# 查看缓存信息
info = cache.get_cache_info()
print(info)  # {'items': 1, 'total_size': 16}
```

## 提示
- 使用 `time.time()` 获取当前时间戳
- 缓存数据结构可以包含：资源内容、缓存时间和过期时间
- 注意处理缓存过期的逻辑