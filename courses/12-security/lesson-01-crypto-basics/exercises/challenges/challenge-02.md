# 挑战2: 构建端到端加密消息系统

## 难度: ⭐⭐⭐⭐

## 背景知识
端到端加密（E2EE）确保只有通信的双方能够读取消息，即使是服务提供商也无法访问明文内容。现代即时通讯应用如Signal、WhatsApp都使用E2EE来保护用户隐私。

### 核心组件
1. **密钥交换**：安全地协商共享密钥（如Diffie-Hellman）
2. **对称加密**：使用共享密钥加密实际消息（如AES-GCM）
3. **身份验证**：确保通信对方的身份真实（如数字签名）
4. **前向保密**：即使长期密钥泄露，过去的会话仍然安全

## 任务要求

### 第一部分：设计系统架构
创建一个名为 `e2e_messaging.py` 的Python模块，实现以下类：

```python
class User:
    """代表一个用户，管理密钥对"""
    def __init__(self, username: str):
        self.username = username
        # 生成非对称密钥对（RSA或ECC模拟）
        self.private_key = None  
        self.public_key = None
    
    def sign_message(self, message: bytes) -> bytes:
        """使用私钥对消息进行数字签名"""
        pass
    
    def verify_signature(self, message: bytes, signature: bytes, public_key) -> bool:
        """验证消息签名"""
        pass

class SecureChannel:
    """安全通信通道"""
    def __init__(self, user1: User, user2: User):
        self.user1 = user1
        self.user2 = user2
        # 实现密钥交换协议
        self.shared_secret = self._perform_key_exchange()
    
    def encrypt_message(self, sender: User, message: str) -> dict:
        """加密消息，包含密文、认证标签等"""
        pass
    
    def decrypt_message(self, receiver: User, encrypted_data: dict) -> str:
        """解密并验证消息"""
        pass
```

### 第二部分：实现核心功能
1. **密钥生成**：使用`secrets`模块生成密码学安全的密钥
2. **密钥交换**：实现简化的Diffie-Hellman密钥交换模拟
3. **消息加密**：使用AES-GCM概念加密消息（参考solution-03.py）
4. **数字签名**：实现消息签名和验证（使用哈希和私钥模拟）
5. **完整性验证**：确保消息在传输中未被篡改

### 第三部分：构建完整的消息系统
创建一个命令行界面，支持以下功能：

```python
def main():
    # 创建两个用户
    alice = User("Alice")
    bob = User("Bob")
    
    # 建立安全通道
    channel = SecureChannel(alice, bob)
    
    # 发送加密消息
    encrypted_msg = channel.encrypt_message(alice, "Hello Bob!")
    print(f"加密消息: {encrypted_msg}")
    
    # 接收并解密消息
    decrypted_msg = channel.decrypt_message(bob, encrypted_msg)
    print(f"解密消息: {decrypted_msg}")
    
    # 测试篡改检测
    tampered_msg = encrypted_msg.copy()
    tampered_msg['ciphertext'] = tampered_msg['ciphertext'][:-1] + b'X'
    try:
        channel.decrypt_message(bob, tampered_msg)
        print("❌ 篡改未被检测到！")
    except Exception as e:
        print(f"✅ 篡改被成功检测: {e}")
```

### 第四部分：安全增强
实现以下高级特性：
- **前向保密**：每次会话使用不同的临时密钥
- **密钥轮换**：定期更新长期密钥
- **错误处理**：优雅处理各种安全异常
- **性能优化**：处理大消息的分块加密

## 技术要求
- 使用Python 3.10+标准库（`hashlib`, `secrets`, `os`等）
- 如果可用，可以使用`cryptography`库，但必须有回退方案
- 所有随机数必须使用密码学安全的生成器
- 实现恒定时间比较防止时序攻击
- 完整的错误处理和边界情况测试

## 测试场景
1. 正常消息发送和接收
2. 消息篡改检测
3. 错误密钥尝试解密
4. 大消息（>1MB）处理
5. 并发消息处理

## 提交要求
- 完整的Python实现文件
- 详细的中文文档说明设计决策
- 测试脚本和输出结果
- 安全性分析报告（讨论系统的局限性和改进方向）

## 扩展挑战（可选）
- 实现真正的Diffie-Hellman密钥交换
- 添加消息重放攻击防护
- 支持群组消息加密
- 实现密钥备份和恢复机制

记住：安全系统的实现比设计更困难。关注细节，测试边界情况，并始终假设攻击者会尝试各种方式破坏你的系统。