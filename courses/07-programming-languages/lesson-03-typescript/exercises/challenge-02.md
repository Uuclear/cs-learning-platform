# 编程挑战 2：泛型缓存实现 ⭐⭐⭐

## 背景
缓存是提高应用性能的重要技术。使用 TypeScript 的泛型可以创建类型安全的缓存系统，适用于各种数据类型。

## 任务
实现一个泛型缓存类 `Cache<T>`，支持以下功能：

### 核心方法
1. **`set(key: string, value: T, ttlSeconds?: number)`**：设置缓存项
   - `ttlSeconds` 是可选参数，表示生存时间（秒）
   - 如果不提供，则缓存项永不过期

2. **`get(key: string): T | undefined`**：获取缓存项
   - 如果缓存项不存在或已过期，返回 `undefined`
   - 自动清理过期的缓存项

3. **`delete(key: string): boolean`**：删除缓存项
   - 成功删除返回 `true`，否则返回 `false`

4. **`has(key: string): boolean`**：检查缓存项是否存在且未过期

5. **`clear(): void`**：清空所有缓存

6. **`size(): number`**：返回当前有效缓存项的数量

### 技术要求
- 使用 `Map<string, CacheItem<T>>` 存储缓存数据
- 定义内部接口 `CacheItem<T>` 包含 `value` 和 `expiry` 属性
- 使用 `Date.now()` 处理时间戳
- 确保类型安全，避免使用 `any`

### 示例用法
```typescript
const cache = new Cache<string>();
cache.set("greeting", "Hello!", 10); // 10秒后过期
cache.set("permanent", "Never expires");

console.log(cache.get("greeting")); // "Hello!"
console.log(cache.has("nonexistent")); // false
```

## 提示
- 过期时间可以用 `Date.now() + (ttlSeconds * 1000)` 计算
- 在 `get` 和 `has` 方法中检查并清理过期项
- 考虑并发访问的情况（虽然 JavaScript 是单线程的）
- 使用泛型确保不同类型缓存的类型安全