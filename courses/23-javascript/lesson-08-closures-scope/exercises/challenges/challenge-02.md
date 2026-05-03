# 编程挑战 2：创建模块化计时器系统

## 题目描述

使用闭包实现一个模块化的计时器系统，支持创建多个独立的计时器实例，每个实例都可以独立启动、停止、重置，并且能够记录运行时间。

## 要求

1. 实现 `createTimer()` 工厂函数，返回计时器对象
2. 每个计时器应该有独立的状态（不会相互影响）
3. 支持以下方法：
   - `start()`: 开始计时
   - `stop()`: 停止计时
   - `reset()`: 重置计时器
   - `getTime()`: 获取当前经过的时间（毫秒）
   - `isRunning()`: 检查计时器是否正在运行
4. 使用闭包来封装私有状态（如开始时间、是否运行等）
5. 提供适当的错误处理（如重复启动、重复停止等）

## 示例用法

```javascript
const timer1 = createTimer();
const timer2 = createTimer();

timer1.start();
setTimeout(() => {
  console.log('Timer 1 time:', timer1.getTime()); // 显示经过的时间
  timer1.stop();
}, 1000);

timer2.start();
setTimeout(() => {
  console.log('Timer 2 time:', timer2.getTime()); // 显示经过的时间  
  timer2.reset();
}, 500);
```

## 提示

- 使用 `Date.now()` 来获取当前时间戳
- 考虑如何存储每个计时器的私有状态
- 注意处理计时器的各种状态转换（启动→停止→启动等）
- 可以使用 `setTimeout` 或 `setInterval` 来实现持续更新，但要注意内存泄漏

## 扩展挑战（可选）

- 添加回调函数支持，在特定时间间隔触发
- 实现倒计时功能
- 支持暂停/恢复功能（而不是完全停止）
- 添加事件监听器模式，允许注册多个回调函数