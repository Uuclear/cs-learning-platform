# 编程挑战 2：DNS 安全防护

## 背景
DNS 劫持是常见的网络安全威胁，攻击者可能篡改 DNS 响应将用户引导到恶意网站。

## 任务
实现一个安全的 DNS 解析器，具备以下功能：

1. **响应验证**：验证 DNS 响应的合法性
2. **缓存污染防护**：防止恶意 DNS 记录污染本地缓存  
3. **多源验证**：向多个 DNS 服务器查询并比较结果
4. **异常检测**：检测可疑的 DNS 响应（如 TTL 异常短、IP 地址可疑等）

## 要求
- 实现 `SecureDNSResolver` 类
- 支持配置多个可信 DNS 服务器（如 8.8.8.8, 1.1.1.1）
- 实现基本的安全检查逻辑
- 提供详细的日志记录功能

## 安全检查规则
1. TTL 小于 60 秒的记录需要额外验证
2. 私有 IP 地址范围（10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16）在公共域名中可能是可疑的
3. 同一域名在不同 DNS 服务器返回的结果应该一致
4. 权威服务器返回的记录应该与预期的域名匹配

## 测试场景
```python
resolver = SecureDNSResolver(trusted_servers=["8.8.8.8", "1.1.1.1"])
result = resolver.resolve("google.com")

# 正常情况应该返回有效 IP
assert result is not None
assert is_valid_public_ip(result)

# 模拟恶意响应（私有 IP）
malicious_response = {"google.com": "192.168.1.100"}
# 系统应该拒绝或标记为可疑
```

## 扩展思考
- 如何集成 DNSSEC 验证？
- 如何处理 CDN 返回的不同地理位置 IP？
- 如何平衡安全性和性能？