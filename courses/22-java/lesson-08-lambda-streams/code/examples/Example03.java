package examples;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 示例3: 分组统计（Collectors.groupingBy）
 * 演示 Stream API 的分组、统计和收集操作
 */
public class Example03 {
    // 辅助类：订单
    static class Order {
        private String customer;
        private String product;
        private String category;
        private double amount;
        private int quantity;
        private String status;

        public Order(String customer, String product, String category,
                    double amount, int quantity, String status) {
            this.customer = customer;
            this.product = product;
            this.category = category;
            this.amount = amount;
            this.quantity = quantity;
            this.status = status;
        }

        // Getters
        public String getCustomer() { return customer; }
        public String getProduct() { return product; }
        public String getCategory() { return category; }
        public double getAmount() { return amount; }
        public int getQuantity() { return quantity; }
        public String getStatus() { return status; }

        @Override
        public String toString() {
            return String.format("Order{customer='%s', product='%s', category='%s', amount=%.2f, quantity=%d, status='%s'}",
                               customer, product, category, amount, quantity, status);
        }
    }

    public static void main(String[] args) {
        List<Order> orders = Arrays.asList(
            new Order("Alice", "Laptop", "Electronics", 1200.0, 1, "completed"),
            new Order("Bob", "Mouse", "Electronics", 25.5, 2, "completed"),
            new Order("Alice", "Keyboard", "Electronics", 75.0, 1, "pending"),
            new Order("Charlie", "Book", "Books", 15.99, 3, "completed"),
            new Order("Bob", "Monitor", "Electronics", 300.0, 1, "completed"),
            new Order("Diana", "Headphones", "Electronics", 89.99, 1, "cancelled"),
            new Order("Alice", "Novel", "Books", 12.5, 2, "completed"),
            new Order("Charlie", "Tablet", "Electronics", 450.0, 1, "completed")
        );

        System.out.println("=== 原始订单列表 ===");
        orders.forEach(System.out::println);

        // 1. 简单分组：按客户分组
        System.out.println("\n=== 1. 按客户分组 ===");
        Map<String, List<Order>> ordersByCustomer = orders.stream()
            .collect(Collectors.groupingBy(Order::getCustomer));

        ordersByCustomer.forEach((customer, customerOrders) -> {
            System.out.println(customer + ":");
            customerOrders.forEach(order -> System.out.println("  " + order));
        });

        // 2. 分组并计数
        System.out.println("\n=== 2. 每个客户的订单数量 ===");
        Map<String, Long> orderCountByCustomer = orders.stream()
            .collect(Collectors.groupingBy(Order::getCustomer, Collectors.counting()));

        orderCountByCustomer.forEach((customer, count) ->
            System.out.println(customer + ": " + count + " orders"));

        // 3. 分组并求和
        System.out.println("\n=== 3. 每个客户的总消费金额 ===");
        Map<String, Double> totalAmountByCustomer = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCustomer,
                Collectors.summingDouble(Order::getAmount)
            ));

        totalAmountByCustomer.forEach((customer, total) ->
            System.out.printf("%s: $%.2f%n", customer, total));

        // 4. 多级分组：先按类别，再按客户
        System.out.println("\n=== 4. 多级分组（类别 -> 客户） ===");
        Map<String, Map<String, List<Order>>> multiLevelGrouping = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCategory,
                Collectors.groupingBy(Order::getCustomer)
            ));

        multiLevelGrouping.forEach((category, customerMap) -> {
            System.out.println(category + ":");
            customerMap.forEach((customer, ordersList) -> {
                System.out.println("  " + customer + ": " + ordersList.size() + " orders");
            });
        });

        // 5. 分组并计算平均值
        System.out.println("\n=== 5. 每个类别的平均订单金额 ===");
        Map<String, Double> avgAmountByCategory = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCategory,
                Collectors.averagingDouble(Order::getAmount)
            ));

        avgAmountByCategory.forEach((category, avg) ->
            System.out.printf("%s: $%.2f average%n", category, avg));

        // 6. 分组并找到最大值/最小值
        System.out.println("\n=== 6. 每个客户的最高和最低订单金额 ===");
        Map<String, Optional<Order>> maxOrderByCustomer = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCustomer,
                Collectors.maxBy(Comparator.comparing(Order::getAmount))
            ));

        Map<String, Optional<Order>> minOrderByCustomer = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCustomer,
                Collectors.minBy(Comparator.comparing(Order::getAmount))
            ));

        maxOrderByCustomer.forEach((customer, maxOrder) -> {
            if (maxOrder.isPresent()) {
                System.out.printf("%s - 最高订单: $%.2f (%s)%n",
                    customer, maxOrder.get().getAmount(), maxOrder.get().getProduct());
            }
        });

        // 7. 过滤分组结果
        System.out.println("\n=== 7. 只显示已完成的订单（按客户分组） ===");
        Map<String, List<Order>> completedOrdersByCustomer = orders.stream()
            .filter(order -> "completed".equals(order.getStatus()))
            .collect(Collectors.groupingBy(Order::getCustomer));

        completedOrdersByCustomer.forEach((customer, completedOrders) -> {
            System.out.println(customer + " (completed only):");
            completedOrders.forEach(order -> System.out.println("  " + order));
        });

        // 8. 自定义收集器：按状态分组并统计各种指标
        System.out.println("\n=== 8. 按状态分组的综合统计 ===");
        Map<String, Map<String, Object>> statsByStatus = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getStatus,
                Collectors.collectingAndThen(
                    Collectors.toList(),
                    orderList -> {
                        Map<String, Object> stats = new HashMap<>();
                        stats.put("count", (long) orderList.size());
                        stats.put("totalAmount", orderList.stream()
                                .mapToDouble(Order::getAmount).sum());
                        stats.put("avgAmount", orderList.stream()
                                .mapToDouble(Order::getAmount).average().orElse(0.0));
                        stats.put("products", orderList.stream()
                                .map(Order::getProduct).collect(Collectors.toList()));
                        return stats;
                    }
                )
            ));

        statsByStatus.forEach((status, stats) -> {
            System.out.println("Status: " + status);
            System.out.println("  Count: " + stats.get("count"));
            System.out.printf("  Total Amount: $%.2f%n", stats.get("totalAmount"));
            System.out.printf("  Average Amount: $%.2f%n", stats.get("avgAmount"));
            System.out.println("  Products: " + stats.get("products"));
        });
    }
}