# 挑战1: 实现Vigenère密码的加密与破解

## 难度: ⭐⭐⭐

## 背景知识
Vigenère密码是一种多表替换密码，使用一个关键词来决定每个字符使用的替换表。它比简单的凯撒密码更安全，因为相同的明文字母可能被加密为不同的密文字母。

### 加密原理
- 关键词重复扩展到与明文相同长度
- 对于每个字符，使用关键词对应字符作为偏移量进行凯撒密码加密
- 例如：明文 "ATTACK"，关键词 "LEMON" → "LXFOPV"

### 破解方法
Vigenère密码可以通过以下步骤破解：
1. **Kasiski测试**：找出重复模式的距离，推测密钥长度
2. **重合指数分析**：计算不同密钥长度假设下的重合指数
3. **频率分析**：对每个密钥位置分别进行频率分析

## 任务要求

### 第一部分：实现Vigenère加密/解密
创建一个Python脚本 `vigenere_cipher.py`，实现以下功能：

```python
def vigenere_encrypt(plaintext: str, keyword: str) -> str:
    """使用Vigenère密码加密明文"""
    pass

def vigenere_decrypt(ciphertext: str, keyword: str) -> str:
    """使用Vigenère密码解密密文"""
    pass
```

要求：
- 只处理字母字符，保持大小写
- 非字母字符保持不变
- 关键词不区分大小写
- 支持任意长度的关键词

### 第二部分：实现Vigenère密码破解
创建一个函数 `break_vigenere(ciphertext: str) -> Tuple[str, str]`，尝试自动破解Vigenère密码：

```python
def break_vigenere(ciphertext: str) -> Tuple[str, str]:
    """
    自动破解Vigenère密码
    返回: (猜测的关键词, 解密后的明文)
    """
    pass
```

破解策略：
1. 使用重合指数分析确定最可能的密钥长度（尝试1-20）
2. 对每个密钥位置进行频率分析，猜测密钥字符
3. 返回最佳猜测结果

### 第三部分：测试和验证
- 使用已知的明文/密文对测试你的实现
- 尝试破解提供的测试密文
- 分析你的破解算法的成功率和局限性

## 测试数据
- 明文: "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
- 关键词: "CRYPTO"
- 预期密文: "VYC QZMGI FZWBR HCB NXMWS CZZY VYC LBCA GCU"

## 提交要求
- 完整的Python脚本，包含所有函数实现
- 清晰的中文注释
- 测试用例和输出示例
- 简短的破解算法说明文档

## 扩展挑战（可选）
- 实现Kasiski测试作为密钥长度检测的替代方法
- 处理包含空格和标点符号的完整文本
- 优化频率分析算法提高破解准确率

祝你好运！记住，理解密码学的历史和弱点是构建安全系统的基础。