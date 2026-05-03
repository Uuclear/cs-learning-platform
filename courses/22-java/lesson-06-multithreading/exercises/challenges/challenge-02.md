# 挑战 2：并发Web爬虫实现

## 背景
在实际开发中，我们经常需要同时处理多个网络请求以提高效率。并发Web爬虫是一个很好的多线程应用场景。

## 任务要求
实现一个简单的并发URL下载器，能够同时下载多个网页内容并保存到本地文件。

### 基本要求
1. 创建一个`ConcurrentDownloader`类，使用线程池管理下载任务
2. 实现`downloadUrl(String url, String filename)`方法，下载指定URL的内容并保存到文件
3. 使用`ExecutorService`创建固定大小的线程池（建议4个线程）
4. 处理网络异常和文件IO异常
5. 实现任务超时机制（单个下载任务最多等待10秒）

### 进阶要求（选做）
1. 添加下载进度显示功能
2. 实现重试机制：如果下载失败，自动重试最多3次
3. 添加速率限制：每秒最多发起5个请求，避免对服务器造成压力
4. 使用`CompletableFuture`重构代码，支持异步链式调用

### 测试数据
使用以下URL进行测试（这些是公开的、安全的测试URL）：
- https://httpbin.org/delay/1
- https://httpbin.org/delay/2  
- https://httpbin.org/html
- https://httpbin.org/json

### 提示
- 使用`java.net.URL`或`java.net.http.HttpClient`（Java 11+）进行HTTP请求
- 使用`java.nio.file.Files`进行文件操作
- 考虑使用`Future.get(timeout, TimeUnit)`实现超时控制
- 正确关闭线程池和释放资源

### 验证标准
- 能够同时下载多个URL而不会阻塞
- 异常情况下程序不会崩溃
- 超时任务能够被正确取消
- 所有资源都被正确释放（线程池关闭、文件流关闭等）

## 提交内容
请提交完整的Java源代码文件，包含必要的异常处理和资源管理，并附上简短的使用说明。