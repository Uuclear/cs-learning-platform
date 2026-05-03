# 挑战 02: 构建 E2E 测试流程

## 任务描述

在这个挑战中，你需要模拟一个完整的 Cypress E2E 测试流程，涵盖用户注册、登录和基本操作的场景。

## 要求

1. **实现 `Cypress` 类**：
   - `visit(url)`：模拟页面导航
   - `get(selector)`：通过 CSS 选择器获取元素
   - `contains(text)`：查找包含指定文本的元素
   - `intercept(url_pattern, mock_response)`：模拟 API 请求拦截

2. **实现 `Page` 和 `Element` 类**：
   - `Page` 根据 URL 加载不同的页面元素
   - `Element` 支持 `click()`、`type(text)` 和 `should(assertion, expected)` 方法

3. **实现完整的用户流程测试**：
   - 访问首页并导航到注册页面
   - 填写注册表单（用户名、邮箱、密码）
   - 提交注册并验证成功消息
   - 自动跳转到登录页面
   - 使用注册的凭据登录
   - 验证登录后显示欢迎消息

4. **处理错误场景**：
   - 测试无效凭据的登录尝试
   - 验证错误消息正确显示
   - 确保用户仍停留在登录页面

## 页面结构

- `/`：首页，包含"注册"和"登录"链接
- `/register`：注册页面，包含表单字段和提交按钮
- `/login`：登录页面，包含表单字段、提交按钮和错误消息区域
- `/dashboard`：仪表板页面，显示欢迎消息和退出按钮

## API 模拟

- `POST /api/register`：注册 API，成功时返回 `{success: true}`，失败时返回 `{success: false, error: "原因"}`
- `POST /api/login`：登录 API，成功时返回 `{success: true, user: {name: "用户名"}}`，失败时返回 `{success: false, error: "无效凭据"}`

## 示例使用

```python
cy = Cypress()
cy.visit("/")
cy.get("#register-link").click()
cy.visit("/register")

cy.get("#username").type("testuser")
cy.get("#email").type("test@example.com")
cy.get("#password").type("password123")

cy.intercept("/api/register", {"success": True})
cy.get("#submit").click()

# 验证注册成功并跳转到登录页面
cy.visit("/login")
# ... 继续登录流程
```

## 提示

- 使用字典存储页面元素，根据 URL 动态生成
- 元素的 `should` 方法应该支持多种断言类型
- 使用 `time.sleep()` 模拟网络延迟
- 参考 `code/solutions/solution-03.py` 获取完整实现思路

## 验证

运行你的 E2E 测试，确保：

1. 正常用户流程能够完整执行
2. 错误场景能够正确处理
3. 所有断言都能提供清晰的通过/失败反馈
4. API 拦截功能正常工作

完成后，你应该能够看到完整的用户旅程测试输出，包括每个步骤的操作和验证结果。