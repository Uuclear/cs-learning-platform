# 编程挑战 1：用户信息验证器 ⭐⭐

## 背景
在实际开发中，我们经常需要验证用户输入的数据。使用 TypeScript 的类型系统可以帮助我们在编译时就发现潜在的问题。

## 任务
创建一个用户信息验证函数，要求如下：

### 接口定义
定义一个 `User` 接口，包含以下属性：
- `id`: number（必需）
- `name`: string（必需）
- `email`: string（必需）  
- `age`: number（必需）

### 验证函数
实现 `validateUser(user: User)` 函数，返回验证结果对象：
```typescript
{
  isValid: boolean;
  errors: string[];
}
```

### 验证规则
1. **姓名验证**：不能为空，且长度不超过50个字符
2. **邮箱验证**：必须符合基本的邮箱格式（包含@和.）
3. **年龄验证**：必须在0-150之间
4. **ID验证**：必须是正整数

### 示例
```typescript
const user = {
  id: 1,
  name: "张三",
  email: "zhang@example.com", 
  age: 25
};

const result = validateUser(user);
// { isValid: true, errors: [] }
```

## 提示
- 使用正则表达式验证邮箱格式：`/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- 对于可选的错误信息，可以使用数组的 `push` 方法收集
- 记得处理边界情况（如空字符串、负数等）