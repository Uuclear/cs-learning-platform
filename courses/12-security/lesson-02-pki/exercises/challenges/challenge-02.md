# 挑战 2：PKI 信任链模拟器 ⭐⭐⭐⭐

## 背景
理解 PKI 信任模型的最佳方式是亲手构建一个简化版本。虽然 Python 标准库不支持证书生成，但我们可以创建一个概念验证工具来模拟整个 PKI 信任链的工作流程。

## 任务要求
创建一个交互式 PKI 模拟器 `pki_simulator.py`，能够：

1. **模拟根 CA 创建**：生成根 CA 的密钥对和自签名证书（概念性表示）
2. **模拟中间 CA 签发**：使用根 CA 签发中间 CA 证书
3. **模拟终端证书签发**：使用中间 CA 签发终端实体证书
4. **模拟证书链验证**：演示从终端证书到根 CA 的完整验证过程
5. **模拟证书撤销**：实现简单的证书撤销机制

## 具体实现步骤

### 步骤 1：数据结构设计
设计适当的数据结构来表示：
- **证书对象**：包含主题、颁发者、公钥、有效期、序列号、扩展等字段
- **CA 对象**：包含私钥（概念性）、签发能力、已签发证书列表
- **证书撤销列表**：存储已撤销证书的序列号

### 步骤 2：核心功能实现

#### 根 CA 创建
```python
class RootCA:
    def __init__(self, common_name):
        # 生成密钥对（这里用字符串模拟）
        self.private_key = f"root_ca_private_key_{common_name}"
        self.public_key = f"root_ca_public_key_{common_name}"
        # 创建自签名证书
        self.certificate = Certificate(
            subject=common_name,
            issuer=common_name,
            public_key=self.public_key,
            is_ca=True,
            path_length=1
        )
```

#### 证书签发
实现签发函数，模拟 CA 使用私钥对证书进行签名的过程：
```python
def issue_certificate(self, subject_name, is_ca=False, path_length=None):
    # 创建新证书
    cert = Certificate(
        subject=subject_name,
        issuer=self.certificate.subject,
        public_key=f"public_key_{subject_name}",
        is_ca=is_ca,
        path_length=path_length
    )
    # 模拟签名过程
    cert.signature = f"signed_by_{self.certificate.subject}"
    return cert
```

#### 证书链验证
实现验证函数，检查：
- 证书链是否能追溯到受信任的根 CA
- 每个证书的签名是否有效
- 基本约束是否正确
- 证书是否在有效期内

### 步骤 3：交互式界面
创建简单的命令行界面，允许用户：
- 创建根 CA
- 创建中间 CA
- 签发终端证书
- 验证证书链
- 撤销证书
- 查看证书详情

### 步骤 4：错误场景模拟
实现常见错误场景的演示：
- 证书链断裂（缺少中间 CA）
- 无效签名
- 过期证书
- 不正确的基本约束

## 测试场景
你的模拟器应该能够处理以下场景：

1. **正常场景**：根 CA → 中间 CA → 终端证书（验证成功）
2. **链断裂**：只有终端证书和根 CA，缺少中间 CA（验证失败）
3. **撤销场景**：签发证书后撤销，验证应该失败
4. **约束违规**：终端证书被错误地标记为 CA（验证失败）

## 提交要求
- 代码文件：`pki_simulator.py`
- 必须使用面向对象设计
- 包含详细的中文注释和文档字符串
- 实现完整的交互式功能
- 包含至少 4 个测试场景的演示

## 评估标准
- **正确性**：准确模拟 PKI 信任链的核心概念
- **完整性**：覆盖证书生命周期的主要阶段
- **用户体验**：交互界面清晰易用
- **错误处理**：能够正确识别和报告各种错误场景

> 💡 提示：重点在于概念的准确性而非加密实现的细节。使用字符串和简单数据结构来模拟复杂的密码学操作，但确保逻辑流程符合真实的 PKI 工作原理。