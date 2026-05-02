# 挑战1：生产者-消费者问题

## 难度
⭐⭐⭐

## 描述
使用Python的threading模块实现经典的生产者-消费者问题。

要求：
1. 创建一个共享缓冲区（使用queue.Queue）
2. 实现生产者线程，随机生成数据放入缓冲区
3. 实现消费者线程，从缓冲区取出数据并处理
4. 使用threading.Event来控制线程的启动和停止

## 提示
- 使用 `queue.Queue` 作为线程安全的缓冲区
- 使用 `queue.put()` 和 `queue.get()` 进行生产/消费
- 使用 `threading.Event` 作为停止信号
