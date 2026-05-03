# 编程挑战 1：购物车系统

## 任务描述
使用ES6+现代语法创建一个简单的购物车系统，要求实现以下功能：

### 基本要求
1. 创建一个 `Product` 类，包含 `id`、`name`、`price` 属性
2. 创建一个 `ShoppingCart` 类，使用 `Map` 来存储商品和数量
3. 实现 `addItem(product, quantity)` 方法添加商品到购物车
4. 实现 `removeItem(productId)` 方法从购物车移除商品
5. 实现 `getTotal()` 方法计算购物车总价格
6. 实现 `getItems()` 方法返回购物车中的所有商品信息

### 进阶要求
7. 使用私有字段保护购物车的内部数据结构
8. 实现 `clear()` 方法清空整个购物车
9. 添加错误处理：当添加无效商品或数量时给出适当提示

### 示例用法
```javascript
const cart = new ShoppingCart();
const apple = new Product(1, '苹果', 5.0);
const banana = new Product(2, '香蕉', 3.5);

cart.addItem(apple, 3);
cart.addItem(banana, 2);
console.log(cart.getTotal()); // 22
console.log(cart.getItems()); // [{product: apple, quantity: 3}, {product: banana, quantity: 2}]
```

## 提交要求
- 使用ES6 class语法
- 使用Map数据结构存储商品
- 使用模板字符串格式化输出
- 包含适当的错误处理
- 代码要有中文注释说明关键逻辑

## 评估标准
- 正确实现所有基本功能（60分）
- 完成进阶要求（20分）
- 代码质量和可读性（10分）
- 错误处理完整性（10分）