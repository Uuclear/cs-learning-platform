# 挑战 2：设计通用的 API 客户端错误处理

## 背景
你正在构建一个通用的 HTTP API 客户端库，需要处理各种可能的错误情况。这个库将被多个团队使用，因此错误处理必须既灵活又用户友好。

## 要求
1. 创建一个 `ApiError` 枚举，包含以下变体：
   - `NetworkError(reqwest::Error)` - 网络请求错误
   - `JsonError(serde_json::Error)` - JSON 解析错误  
   - `HttpError(u16)` - HTTP 状态码错误（如 404, 500）
   - `ValidationError(String)` - 数据验证错误
   - `AuthenticationError` - 认证失败

2. 为 `ApiError` 实现必要的 trait：
   - `std::error::Error`
   - `std::fmt::Display`
   - 相关的 `From` trait 实现

3. 创建一个 `ApiClient` 结构体，包含方法：
   - `get<T: DeserializeOwned>(&self, url: &str) -> Result<T, ApiError>`
   - `post<T: Serialize, R: DeserializeOwned>(&self, url: &str, data: T) -> Result<R, ApiError>`

4. 实现错误链和上下文信息：
   - 使用 `thiserror` crate 或手动实现来添加错误上下文
   - 确保原始错误信息不会丢失

5. 创建一个错误分类函数：
   ```rust
   fn is_retryable(error: &ApiError) -> bool {
       // 返回 true 如果错误是临时的，可以重试
   }
   ```

## 额外挑战（可选）
- 实现 `Backtrace` 支持以提供完整的调用栈信息
- 添加日志记录功能，在错误发生时记录详细信息
- 实现错误转换函数，将 `ApiError` 转换为其他常见的错误类型

## 提示
- 考虑使用 `thiserror` crate 来简化错误实现（但也要理解手动实现的原理）
- HTTP 错误应该包含状态码和可能的响应体信息
- 网络错误可能是临时的，应该可以重试
- 验证错误和认证错误通常不应该重试

## 验收标准
- 所有错误类型都能被正确创建和处理
- 错误信息包含足够的上下文用于调试
- 错误分类逻辑合理
- API 设计符合 Rust 的错误处理最佳实践
- 代码具有良好的扩展性，易于添加新的错误类型