# 挑战 1：实现代码审查检查清单

## 难度：⭐⭐

### 背景
你的团队正在建立自动化的代码审查流程。你需要实现一个简单的代码审查检查器，能够分析Python代码并识别常见的问题。

### 任务要求
创建一个 `CodeReviewChecker` 类，包含以下功能：

1. **命名规范检查**：
   - 函数名应使用 snake_case（小写字母和下划线）
   - 类名应使用 PascalCase（首字母大写）
   - 变量名应使用 snake_case

2. **文档字符串检查**：
   - 计算函数的文档字符串覆盖率
   - 如果覆盖率低于80%，报告问题

3. **复杂度检查**：
   - 计算每个函数的圈复杂度
   - 如果复杂度超过10，报告问题

### 输入输出
- **输入**：Python代码字符串
- **输出**：包含问题列表、总问题数和文档字符串覆盖率的字典

### 示例
```python
code = '''
def calculate_user_score(user_data):
    score = 0
    if user_data.get("active", False):
        score += 10
    return score

class userDataProcessor:
    def process(self, data):
        return {"score": calculate_user_score(data)}
'''

# 期望输出应包含命名不规范的问题
```

### 提示
- 使用 `ast` 模块解析Python代码
- 圈复杂度 = 1 + 控制流语句数量（if、for、while、try等）
- 文档字符串是函数体中的第一个字符串字面量

### 评估标准
- ✅ 正确识别命名规范问题
- ✅ 准确计算文档字符串覆盖率
- ✅ 正确计算圈复杂度
- ✅ 返回格式符合要求
- ✅ 代码具有良好的可读性和结构