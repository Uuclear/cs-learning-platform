# 挑战 2：实现异常安全的网络客户端

## 背景
你需要实现一个简单的HTTP客户端，能够发送请求并处理各种网络错误。网络操作天生具有不确定性，可能因为连接失败、超时、服务器错误等原因失败。

## 任务要求

### 1. 异常类层次结构
设计完整的网络异常类层次：

- `NetworkException`（基类）
  - `ConnectionException`（连接相关错误）
    - `TimeoutException`（连接或读取超时）
    - `HostException`（主机解析失败）
    - `ConnectionRefusedException`（连接被拒绝）
  - `ProtocolException`（协议错误）
    - `HttpException`（HTTP协议错误）
      - `HttpClientException`（4xx客户端错误）
      - `HttpServerException`（5xx服务器错误）

每个异常类应该包含：
- HTTP状态码（如果适用）
- 原始错误信息
- 请求URL上下文
- 时间戳

### 2. 网络客户端实现
实现`HttpClient`类：

```cpp
class HttpClient {
public:
    struct Request {
        std::string url;
        std::string method; // GET, POST, etc.
        std::map<std::string, std::string> headers;
        std::string body;
        int timeout_seconds = 30;
    };
    
    struct Response {
        int status_code;
        std::map<std::string, std::string> headers;
        std::string body;
        std::chrono::steady_clock::time_point request_time;
        std::chrono::steady_clock::time_point response_time;
    };
    
    // 发送HTTP请求
    Response sendRequest(const Request& request);
    
    // 异步请求（可选高级功能）
    std::future<Response> sendRequestAsync(const Request& request);
    
    // 批量请求
    std::vector<Response> sendBatchRequests(const std::vector<Request>& requests);
    
private:
    // 连接池管理（简化版）
    void establishConnection(const std::string& host, int port);
    void closeConnection();
    
    // 异常安全的资源管理
    class ConnectionGuard {
        // RAII连接管理器
    };
};
```

### 3. 异常安全和性能要求

#### 异常安全保证
- **基本保证**：所有公共方法必须提供基本异常安全保证
- **强保证**：`sendRequest`应该提供强异常安全保证
- **不抛出保证**：析构函数、移动操作必须是`noexcept`

#### 性能优化
- 使用移动语义避免不必要的拷贝
- 连接复用以减少开销
- 超时机制防止无限等待

### 4. 错误处理策略
实现以下错误处理策略：

1. **重试机制**：对于临时性错误（如网络抖动），自动重试最多3次
2. **优雅降级**：在网络不可用时提供缓存数据（如果有）
3. **详细日志**：记录所有错误的详细信息用于调试
4. **用户友好**：向调用者提供清晰的错误信息

### 5. 测试场景
编写测试代码覆盖以下场景：

1. 成功的GET请求
2. 连接超时
3. 主机不存在
4. HTTP 404错误
5. HTTP 500错误  
6. 无效的URL格式
7. 大文件下载（内存管理测试）
8. 并发请求（线程安全性，如果实现了异步功能）

## 评估标准
- 异常类设计的完整性和实用性
- 异常安全级别的正确实现
- 资源管理的正确性（RAII原则）
- 错误恢复策略的有效性
- 代码的可扩展性和可维护性
- 是否遵循现代C++最佳实践

## 提示
- 可以使用伪网络操作（模拟而不是真实网络调用）
- 重点在于异常处理架构，而不是网络协议实现细节
- 考虑使用工厂模式创建不同类型的异常
- 记住异常对象应该可以被拷贝（用于重新抛出）
- 在构造函数中获取资源，在析构函数中释放资源
