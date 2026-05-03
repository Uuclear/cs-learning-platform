# 挑战 2: 实现完整的 OAuth2 PKCE 客户端 ⭐⭐⭐⭐

## 背景
你需要为一个单页应用 (SPA) 实现完整的 OAuth2 授权码流程，包括 PKCE 支持。由于 SPA 是公共客户端，不能安全存储客户端密钥，因此必须使用 PKCE。

## 要求
1. 实现一个 `OAuth2PKCEClient` 类，处理整个授权流程
2. 自动生成和存储 code_verifier
3. 计算 code_challenge 并发起授权请求
4. 处理授权回调，提取授权码
5. 使用授权码和 code_verifier 交换访问令牌
6. 实现令牌存储和自动刷新功能

## 具体步骤

### 步骤 1: PKCE 代码生成
- 实现 `generateCodeVerifier()` 方法：生成 43-128 字符的 URL 安全随机字符串
- 实现 `generateCodeChallenge(codeVerifier)` 方法：使用 SHA256 哈希并进行 base64url 编码

### 步骤 2: 授权请求
- 实现 `getAuthorizationUrl(scopes, state)` 方法：
  - 生成 code_verifier 并存储（在内存或安全存储中）
  - 计算 code_challenge
  - 构建包含所有必要参数的授权 URL

### 步骤 3: 回调处理
- 实现 `handleCallback(url)` 方法：
  - 从 URL 中解析授权码和状态参数
  - 验证状态参数防止 CSRF
  - 返回授权码用于令牌交换

### 步骤 4: 令牌交换
- 实现 `exchangeCodeForTokens(authorizationCode)` 方法：
  - 向令牌端点发送 POST 请求
  - 包含 client_id、code、redirect_uri、code_verifier 和 grant_type
  - 处理响应并存储访问令牌和刷新令牌

### 步骤 5: 令牌管理
- 实现 `getValidAccessToken()` 方法：
  - 检查当前访问令牌是否有效
  - 如果过期，使用刷新令牌获取新令牌
  - 实现刷新令牌轮换

## 安全要求
- 所有敏感操作必须在 HTTPS 下进行
- 状态参数必须是加密安全的随机值
- code_verifier 必须足够长且随机
- 刷新令牌必须实现轮换机制
- 错误处理不能泄露敏感信息

## 测试场景
1. 完整的授权流程（成功路径）
2. 状态参数不匹配（CSRF 防护）
3. 授权码无效或已使用
4. 刷新令牌轮换验证
5. 令牌过期后的自动刷新

## 提示
- 参考 RFC 7636 (PKCE) 和 RFC 6749 (OAuth2)
- 考虑使用浏览器的 Web Storage API 安全存储令牌
- 实现适当的错误边界和用户反馈
- 考虑添加令牌吊销功能