# 挑战2：多线程网页下载器

## 难度
⭐⭐⭐⭐

## 描述
实现一个多线程网页下载器，模拟并发下载多个URL。

要求：
1. 创建一个URL列表（可用模拟URL）
2. 使用ThreadPoolExecutor实现并发下载
3. 统计每个URL的下载时间
4. 实现超时处理（超过3秒的URL标记为失败）
5. 输出下载结果统计

## 提示
- 使用 `concurrent.futures.ThreadPoolExecutor`
- 使用 `time.sleep()` 模拟网络延迟
- 使用 `future.result(timeout=3)` 实现超时处理
