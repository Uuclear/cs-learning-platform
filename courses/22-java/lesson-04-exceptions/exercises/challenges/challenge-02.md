# 挑战 2：银行转账系统异常设计

## 任务描述
设计一个完整的银行转账系统，包含适当的异常处理机制和自定义异常类。

## 要求
1. 创建以下自定义异常类：
   - `AccountNotFoundException`（受检异常）：当账户不存在时抛出
   - `InsufficientFundsException`（受检异常）：当余额不足时抛出
   - `InvalidAmountException`（非受检异常）：当转账金额无效（负数、零、非数字）时抛出

2. 创建 `BankAccount` 类，包含：
   - 账户ID、余额字段
   - 构造函数（验证初始余额）
   - `deposit(double amount)` 方法
   - `withdraw(double amount)` 方法（可能抛出 `InsufficientFundsException`）

3. 创建 `BankService` 类，包含：
   - 账户存储（使用 `Map<String, BankAccount>`）
   - `createAccount(String id, double initialBalance)` 方法
   - `getAccount(String id)` 方法（可能抛出 `AccountNotFoundException`）
   - `transfer(String fromId, String toId, double amount)` 方法（可能抛出多种异常）

4. 在 `main` 方法中演示：
   - 正常转账流程
   - 处理账户不存在的情况
   - 处理余额不足的情况
   - 处理无效金额的情况

## 提示
- 考虑异常的继承层次（哪些应该是受检异常，哪些应该是非受检异常）
- 在异常类中包含有用的上下文信息（如当前余额、请求金额等）
- 使用多层catch块来处理不同类型的异常
- 确保转账操作的原子性（要么全部成功，要么全部失败）

## 评估标准
- 异常类型选择合理（受检 vs 非受检）
- 自定义异常类设计良好，包含有用的信息
- 异常处理逻辑完整，覆盖所有边界情况
- 代码结构清晰，符合面向对象设计原则
