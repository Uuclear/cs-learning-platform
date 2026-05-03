# 编程挑战 2：用户管理系统

## 任务描述
创建一个用户管理系统，利用ES6+的各种现代语法特性来实现用户数据的管理和操作。

### 基本要求
1. 创建一个 `User` 基类，包含 `id`、`username`、`email`、`createdAt` 属性
2. 使用 getter 和 setter 实现对用户名和邮箱的验证（用户名长度3-20，邮箱格式验证）
3. 创建两个子类：
   - `AdminUser` 继承 `User`，添加 `permissions` 数组和 `grantPermission(permission)` 方法
   - `RegularUser` 继承 `User`，添加 `profile` 对象和 `updateProfile(newProfile)` 方法
4. 使用 `Symbol` 创建一个私有方法用于内部验证

### 进阶要求
5. 实现一个 `UserManager` 类，使用 `Set` 来存储所有用户，确保用户ID唯一
6. 在 `UserManager` 中实现以下方法：
   - `addUser(user)` - 添加用户
   - `findUserById(id)` - 根据ID查找用户
   - `getUsersByType(type)` - 根据类型获取用户（'admin' 或 'regular'）
   - `removeUser(id)` - 删除用户
7. 使用模板字符串和标签函数创建用户信息的格式化输出
8. 实现静态方法 `User.isValidEmail(email)` 进行邮箱验证

### 示例用法
```javascript
const userManager = new UserManager();

const admin = new AdminUser(1, 'admin_user', 'admin@example.com');
admin.grantPermission('delete_users');

const regular = new RegularUser(2, 'john_doe', 'john@example.com');
regular.updateProfile({ age: 25, city: '北京' });

userManager.addUser(admin);
userManager.addUser(regular);

console.log(userManager.getUsersByType('admin'));
console.log(userManager.findUserById(2).profile);
```

## 提交要求
- 使用class继承和多态
- 使用Symbol实现私有方法
- 使用Set确保用户唯一性
- 使用getter/setter进行属性验证
- 包含完整的中文注释

## 评估标准
- 正确实现继承和多态（30分）
- 正确使用Symbol和私有方法（20分）
- UserManager功能完整性（30分）
- 代码结构和注释质量（20分）