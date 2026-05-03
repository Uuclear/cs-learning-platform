# 挑战 2：缓存实现与性能测试

## 背景
缓存是提高应用程序性能的重要技术。你需要实现一个简单的内存缓存系统，并比较不同集合类型的性能表现。

## 要求

### 第一部分：LRU 缓存实现
1. 创建一个 `LRUCache<K, V>` 类，实现最近最少使用（LRU）缓存策略
2. 缓存应该有固定的最大容量
3. 当缓存满时，自动移除最近最少使用的条目
4. 支持 `get(K key)` 和 `put(K key, V value)` 操作
5. 使用合适的集合类型组合来实现高效的 LRU 算法

### 第二部分：性能对比测试
1. 实现三种不同的缓存策略：
   - 基于 `LinkedHashMap` 的 LRU 缓存
   - 基于 `HashMap` + `LinkedList` 的自定义 LRU 缓存  
   - 简单的无淘汰策略缓存（只用 `HashMap`）
2. 设计性能测试用例，模拟真实使用场景：
   - 随机访问模式
   - 热点数据访问模式
   - 顺序访问模式
3. 测量并比较三种实现的：
   - 内存使用情况
   - 响应时间
   - 缓存命中率

## 提示
- Java 的 `LinkedHashMap` 可以通过重写 `removeEldestEntry()` 方法实现 LRU
- 对于自定义实现，考虑使用双向链表来维护访问顺序
- 性能测试时使用足够大的数据集（至少 10,000 次操作）
- 使用 `System.nanoTime()` 进行精确的时间测量
- 考虑使用 JMH（Java Microbenchmark Harness）进行更专业的基准测试

## 扩展挑战（可选）
- 实现带过期时间的缓存（TTL - Time To Live）
- 添加线程安全支持
- 实现缓存统计信息（命中率、平均响应时间等）

## 测试框架示例
```java
public class CachePerformanceTest {
    public static void main(String[] args) {
        int capacity = 1000;
        int operations = 100000;
        
        // 测试 LinkedHashMap 实现
        LRUCache<String, String> cache1 = new LinkedHashMapLRUCache<>(capacity);
        long time1 = measurePerformance(cache1, operations);
        
        // 测试自定义实现
        LRUCache<String, String> cache2 = new CustomLRUCache<>(capacity);
        long time2 = measurePerformance(cache2, operations);
        
        System.out.println("LinkedHashMap 实现耗时: " + time1 + " ms");
        System.out.println("自定义实现耗时: " + time2 + " ms");
    }
    
    private static long measurePerformance(LRUCache<String, String> cache, int operations) {
        // 实现性能测试逻辑
        return 0;
    }
}
```