# 编程挑战1: HTTP头部分析器

## 背景
在HTTP通信中，请求头和响应头包含了重要的元数据信息。作为网络工程师，你需要能够解析和分析这些头部信息。

## 任务
编写一个函数 `parse_http_headers(header_text)`，该函数接收一个HTTP头部文本（字符串格式），并返回一个字典，其中键是头部字段名，值是对应的字段值。

## 要求
- 处理标准的HTTP头部格式（字段名: 字段值）
- 忽略空行和只包含空白字符的行
- 字段名应该转换为小写（因为HTTP头部字段名不区分大小写）
- 处理字段值前后的空白字符
- 如果输入为空或无效，返回空字典

## 示例
```python
header_text = """Content-Type: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: */*
Host: example.com

"""

result = parse_http_headers(header_text)
print(result)
# 输出: {
#   'content-type': 'application/json',
#   'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#   'accept': '*/*',
#   'host': 'example.com'
# }
```

## 提示
- 使用字符串的 `split()` 方法按行分割
- 对每一行使用 `split(':', 1)` 分割字段名和字段值
- 注意处理字段值前后的空白字符