# 编程挑战 2：实现API请求重试机制

## 要求

创建一个函数 `fetchWithRetry(url, options)`，能够在请求失败时自动重试：

1. **支持最大重试次数**：默认3次，可通过参数配置
2. **实现指数退避**：每次重试的延迟时间应该是 `baseDelay * 2^(attempt-1)`
3. **可自定义重试条件**：不是所有错误都需要重试（比如404错误可能不需要重试）
4. **提供重试回调**：允许用户监听重试过程

## 具体实现要求

函数签名：
```javascript
async function fetchWithRetry(url, {
  maxRetries = 3,
  baseDelay = 1000,
  shouldRetry = (error, attempt) => attempt <= maxRetries,
  onRetry = (error, attempt, delay) => {}
})
```

- `maxRetries`: 最大重试次数
- `baseDelay`: 基础延迟时间（毫秒）
- `shouldRetry`: 函数，决定是否应该重试，接收错误对象和当前尝试次数
- `onRetry`: 回调函数，在每次重试前调用，用于日志记录或其他操作

## 测试场景

1. **网络不稳定场景**：前几次请求失败，后面成功
2. **永久性错误场景**：所有请求都失败，最终抛出错误
3. **自定义重试条件**：只对特定类型的错误进行重试

## 示例使用

```javascript
// 基本使用
const data = await fetchWithRetry('/api/data');

// 自定义重试逻辑
const data = await fetchWithRetry('/api/data', {
  maxRetries: 5,
  baseDelay: 500,
  shouldRetry: (error, attempt) => {
    // 只在网络错误时重试，不重试404等客户端错误
    return error.message.includes('网络') && attempt <= 5;
  },
  onRetry: (error, attempt, delay) => {
    console.log(`重试 #${attempt}，延迟 ${delay}ms`);
  }
});
```

## 提示

- 使用`for`循环配合`await`来实现重试逻辑
- 在每次重试前使用`setTimeout`实现延迟
- 确保在所有重试都失败后抛出最后一个错误
- 考虑如何包装实际的fetch调用（可以使用mock函数进行测试）

这个挑战将帮助你理解如何在生产环境中处理不可靠的网络请求！