# 挑战 2：实现泛型事件总线

## 背景
事件总线（Event Bus）是一种常用的设计模式，用于在应用程序的不同组件之间传递消息。现在你需要实现一个**类型安全的泛型事件总线**，确保发布者和订阅者之间的类型匹配。

## 要求

### 基本功能
实现 `GenericEventBus` 类，包含以下方法：

1. **订阅**: `<T> void subscribe(Class<T> eventType, Consumer<T> listener)` - 订阅特定类型的事件
2. **发布**: `<T> void publish(T event)` - 发布事件给所有订阅了该类型的监听器
3. **取消订阅**: `<T> void unsubscribe(Class<T> eventType, Consumer<T> listener)` - 取消特定监听器的订阅

### 高级功能（可选）
4. **异步发布**: 支持异步事件处理（使用线程池）
5. **优先级**: 支持监听器优先级（高优先级先执行）
6. **事件过滤**: 支持基于条件的事件过滤

## 提示

- 使用 `Map<Class<?>, List<Consumer<?>>>` 存储监听器
- 利用泛型和通配符确保类型安全
- 注意线程安全问题（如果实现异步功能）
- 考虑内存泄漏问题（监听器的生命周期管理）

## 测试用例

```java
// 定义事件类
class UserCreatedEvent {
    private String userId;
    private String username;
    
    public UserCreatedEvent(String userId, String username) {
        this.userId = userId;
        this.username = username;
    }
    
    // getters...
}

class OrderPlacedEvent {
    private String orderId;
    private double amount;
    
    public OrderPlacedEvent(String orderId, double amount) {
        this.orderId = orderId;
        this.amount = amount;
    }
    
    // getters...
}

// 使用事件总线
GenericEventBus eventBus = new GenericEventBus();

// 订阅用户创建事件
eventBus.subscribe(UserCreatedEvent.class, event -> {
    System.out.println("User created: " + event.getUsername());
});

// 订阅订单放置事件
eventBus.subscribe(OrderPlacedEvent.class, event -> {
    System.out.println("Order placed: $" + event.getAmount());
});

// 发布事件
eventBus.publish(new UserCreatedEvent("123", "john_doe"));
eventBus.publish(new OrderPlacedEvent("ORD-001", 99.99));
```

## 评估标准

- **类型安全**: 确保只有正确类型的事件被发送给对应的监听器
- **泛型设计**: 合理使用泛型、通配符和类型擦除的 workaround
- **功能完整性**: 所有基本功能必须正常工作
- **代码质量**: 设计合理、代码清晰、考虑边界情况

## 扩展思考

1. 如何处理事件监听器抛出的异常？
2. 如何实现事件的父子类型关系（例如订阅 Exception 能接收 RuntimeException）？
3. 如何优化性能，避免频繁的类型检查？
4. 如何与现有的事件框架（如 Guava EventBus）进行对比？

## 进阶挑战

尝试实现一个支持**事件继承层次结构**的版本，使得订阅父类事件的监听器也能接收到子类事件。