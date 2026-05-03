# 挑战 1：证书链分析器 ⭐⭐⭐

## 背景
作为安全工程师，你需要开发一个工具来分析网站的证书链健康状况。许多网站由于配置错误导致证书链不完整，这会影响用户体验和安全性。

## 任务要求
创建一个 Python 脚本 `certificate_chain_analyzer.py`，能够：

1. **获取证书链**：连接到指定的 HTTPS 网站，获取完整的证书链
2. **验证链完整性**：检查证书链是否完整（从终端证书到受信任的根 CA）
3. **检测常见问题**：
   - 证书链断裂（缺少中间 CA 证书）
   - 证书过期或未生效
   - 不正确的基本约束（终端证书被标记为 CA）
   - 弱加密算法（可选）

## 具体实现步骤

### 步骤 1：基础证书链获取
使用 Python 标准库的 `ssl` 和 `socket` 模块获取证书链：
```python
import ssl
import socket

def get_certificate_chain(hostname, port=443):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            return ssock.getpeercert(chain=True)
```

### 步骤 2：证书链验证
实现函数验证证书链的每个环节：
- 检查每个证书的颁发者是否与下一个证书的主题匹配
- 验证所有证书是否在有效期内
- 检查基本约束扩展是否正确设置

### 步骤 3：输出详细报告
生成结构化的分析报告，包含：
- 证书链长度和每个证书的基本信息
- 发现的问题列表（如果有）
- 整体健康状态（绿色/黄色/红色）

## 测试用例
测试你的工具对以下网站的分析结果：
- `www.google.com`（应该显示健康的证书链）
- `github.com`（应该显示健康的证书链）
- 尝试找一个证书链有问题的网站进行测试

## 提交要求
- 代码文件：`certificate_chain_analyzer.py`
- 必须使用 Python 标准库（不能使用第三方库）
- 包含中文注释说明关键逻辑
- 代码应该能够直接运行并产生有意义的输出

## 扩展挑战（可选）
- 添加对 OCSP 响应的支持，检查证书撤销状态
- 实现批量分析功能，可以一次分析多个网站
- 添加 JSON 输出格式选项

> 💡 提示：重点关注证书链的链接验证和基本约束检查，这是最常见的配置错误。