# 挑战1：内存泄漏检测与修复

## 背景
你正在维护一个电商网站的购物车功能，最近用户反馈网站运行一段时间后变得非常慢，甚至出现OutOfMemoryError错误。

## 问题代码
```java
public class ShoppingCart {
    // 静态购物车列表，存储所有用户的购物车
    private static List<CartItem> cartItems = new ArrayList<>();
    
    public void addItem(String userId, String productId, int quantity) {
        CartItem item = new CartItem(userId, productId, quantity);
        cartItems.add(item);
    }
    
    public List<CartItem> getCartItems(String userId) {
        return cartItems.stream()
                .filter(item -> item.getUserId().equals(userId))
                .collect(Collectors.toList());
    }
    
    // 缺少清理过期购物车项的逻辑
}
```

## 任务要求
1. **分析问题**：解释为什么这段代码会导致内存泄漏
2. **修复方案**：提供至少两种不同的解决方案
3. **实现修复**：选择其中一种方案实现完整的修复代码
4. **验证测试**：编写测试代码验证修复效果

## 提交内容
- 问题分析文档（说明内存泄漏的原因）
- 修复后的完整代码
- 测试代码和运行结果截图

## 提示
- 考虑使用WeakHashMap、定期清理机制或基于时间的过期策略
- 注意线程安全性问题
- 可以使用JVM监控工具验证修复效果