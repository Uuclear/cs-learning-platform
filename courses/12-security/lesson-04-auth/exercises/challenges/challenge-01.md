# 挑战 1: 实现安全的 JWT 验证中间件 ⭐⭐⭐

## 背景
你正在开发一个 Web API，需要验证传入请求中的 JWT 令牌。你需要实现一个中间件函数来处理 JWT 验证。

## 要求
1. 创建一个 `validate_jwt_middleware` 函数，接收请求对象和密钥
2. 从 Authorization 头中提取 Bearer 令牌
3. 验证 JWT 的签名、过期时间和受众
4. 如果验证成功，将用户信息附加到请求对象
5. 如果验证失败，抛出适当的错误（401 Unauthorized 或 403 Forbidden）

## 具体步骤
1. 检查 Authorization 头是否存在且格式正确（Bearer <token>）
2. 解码头部和载荷，验证签名
3. 检查 `exp` 声明是否已过期
4. 验证 `aud` 声明是否匹配预期的受众（例如 "my-api"）
5. 验证 `iss` 声明是否来自可信的签发者
6. 将解码后的用户信息（sub, name, email）添加到请求对象

## 安全考虑
- 防止时序攻击（使用恒定时间比较）
- 正确处理各种错误情况
- 不要在错误消息中泄露敏感信息

## 测试用例
```python
# 测试有效令牌
valid_token = JWT.encode({
    "sub": "user123",
    "name": "张三", 
    "email": "zhangsan@example.com",
    "aud": "my-api",
    "iss": "auth-server.example.com",
    "exp": int(time.time()) + 300
}, "secret-key")

# 测试过期令牌
expired_token = JWT.encode({
    "sub": "user123",
    "exp": int(time.time()) - 300
}, "secret-key")

# 测试无效签名
tampered_token = valid_token[:-5] + "abcde"
```

## 提示
- 使用之前学到的 JWT 编码/解码函数
- 考虑使用 try-catch 处理各种验证错误
- 返回适当的 HTTP 状态码和错误消息