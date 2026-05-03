package solutions;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 解决方案3: 分组统计（Collectors.groupingBy）
 * 这是 Example03.java 的完整解决方案，包含所有练习的答案
 */
public class Solution03 {
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

        // 练习1：按客户分组统计订单数量和总金额
        System.out.println("\n=== 练习1：按客户分组统计 ===");
        Map<String, CustomerStats> customerStats = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCustomer,
                Collectors.collectingAndThen(
                    Collectors.toList(),
                    orderList -> new CustomerStats(
                        orderList.size(),
                        orderList.stream().mapToDouble(Order::getAmount).sum(),
                        orderList.stream().mapToDouble(Order::getAmount).average().orElse(0.0)
                    )
                )
            ));

        customerStats.forEach((customer, stats) -> {
            System.out.printf("%s: %d orders, total=$%.2f, avg=$%.2f%n",
                customer, stats.getOrderCount(), stats.getTotalAmount(), stats.getAverageAmount());
        });

        // 练习2：按类别和状态进行多级分组
        System.out.println("\n=== 练习2：多级分组（类别 -> 状态） ===");
        Map<String, Map<String, List<Order>>> categoryStatusGrouping = orders.stream()
            .collect(Collectors.groupingBy(
                Order::getCategory,
                Collectors.groupingBy(Order::getStatus)
            ));

        categoryStatusGrouping.forEach((category, statusMap) -> {
            System.out.println(category + ":");
            statusMap.forEach((status, ordersList) -> {
                double totalAmount = ordersList.stream().mapToDouble(Order::getAmount).sum();
                System.out.printf("  %s: %d orders, total=$%.2f%n",
                    status, ordersList.size(), totalAmount);
            });
        });

        // 练习3：找出每个客户的最高价值订单（已完成状态）
        System.out.println("\n=== 练习3：每个客户的最高价值已完成订单 ===");
        Map<String, Optional<Order>> highestValueCompletedOrderByCustomer = orders.stream()
            .filter(order -> "completed".equals(order.getStatus()))
            .collect(Collectors.groupingBy(
                Order::getCustomer,
                Collectors.maxBy(Comparator.comparing(Order::getAmount))
            ));

        highestValueCompletedOrderByCustomer.forEach((customer, highestOrder) -> {
            if (highestOrder.isPresent()) {
                Order order = highestOrder.get();
                System.out.printf("%s: 最高价值订单 - %s ($%.2f)%n",
                    customer, order.getProduct(), order.getAmount());
            } else {
                System.out.println(customer + ": 没有已完成的订单");
            }
        });

        // 额外练习：计算每个类别的销售占比
        System.out.println("\n=== 额外练习：销售占比分析 ===");
        double totalRevenue = orders.stream()
            .filter(order -> "completed".equals(order.getStatus()))
            .mapToDouble(Order::getAmount)
            .sum();

        if (totalRevenue > 0) {
            Map<String, Double> revenueByCategory = orders.stream()
                .filter(order -> "completed".equals(order.getStatus()))
                .collect(Collectors.groupingBy(
                    Order::getCategory,
                    Collectors.summingDouble(Order::getAmount)
                ));

            revenueByCategory.forEach((category, revenue) -> {
                double percentage = (revenue / totalRevenue) * 100;
                System.out.printf("%s: $%.2f (%.1f%%)%n", category, revenue, percentage);
            });
        }

        // 高级练习：使用自定义收集器进行复杂统计
        System.out.println("\n=== 高级练习：自定义收集器 ===");
        OrderStatistics allStats = orders.stream()
            .collect(Collectors.collectingAndThen(
                Collectors.toList(),
                orderList -> {
                    long completedCount = orderList.stream()
                        .filter(o -> "completed".equals(o.getStatus()))
                        .count();
                    long pendingCount = orderList.stream()
                        .filter(o -> "pending".equals(o.getStatus()))
                        .count();
                    long cancelledCount = orderList.stream()
                        .filter(o -> "cancelled".equals(o.getStatus()))
                        .count();

                    double totalCompletedRevenue = orderList.stream()
                        .filter(o -> "completed".equals(o.getStatus()))
                        .mapToDouble(Order::getAmount)
                        .sum();

                    Map<String, Long> topCustomers = orderList.stream()
                        .filter(o -> "completed".equals(o.getStatus()))
                        .collect(Collectors.groupingBy(
                            Order::getCustomer,
                            Collectors.counting()
                        ))
                        .entrySet().stream()
                        .sorted(Map.Entry.<String, Long>comparingByValue().reversed())
                        .limit(3)
                        .collect(Collectors.toMap(
                            Map.Entry::getKey,
                            Map.Entry::getValue,
                            (e1, e2) -> e1,
                            LinkedHashMap::new
                        ));

                    return new OrderStatistics(
                        completedCount, pendingCount, cancelledCount,
                        totalCompletedRevenue, topCustomers
                    );
                }
            ));

        System.out.println("订单统计摘要:");
        System.out.println("  已完成: " + allStats.getCompletedCount());
        System.out.println("  待处理: " + allStats.getPendingCount());
        System.out.println("  已取消: " + allStats.getCancelledCount());
        System.out.printf("  已完成订单总收入: $%.2f%n", allStats.getTotalCompletedRevenue());
        System.out.println("  前3名客户: " + allStats.getTopCustomers());
    }

    // 辅助类：客户统计
    static class CustomerStats {
        private int orderCount;
        private double totalAmount;
        private double averageAmount;

        public CustomerStats(int orderCount, double totalAmount, double averageAmount) {
            this.orderCount = orderCount;
            this.totalAmount = totalAmount;
            this.averageAmount = averageAmount;
        }

        public int getOrderCount() { return orderCount; }
        public double getTotalAmount() { return totalAmount; }
        public double getAverageAmount() { return averageAmount; }
    }

    // 辅助类：订单统计摘要
    static class OrderStatistics {
        private long completedCount;
        private long pendingCount;
        private long cancelledCount;
        private double totalCompletedRevenue;
        private Map<String, Long> topCustomers;

        public OrderStatistics(long completedCount, long pendingCount, long cancelledCount,
                              double totalCompletedRevenue, Map<String, Long> topCustomers) {
            this.completedCount = completedCount;
            this.pendingCount = pendingCount;
            this.cancelledCount = cancelledCount;
            this.totalCompletedRevenue = totalCompletedRevenue;
            this.topCustomers = topCustomers;
        }

        public long getCompletedCount() { return completedCount; }
        public long getPendingCount() { return pendingCount; }
        public long getCancelledCount() { return cancelledCount; }
        public double getTotalCompletedRevenue() { return totalCompletedRevenue; }
        public Map<String, Long> getTopCustomers() { return topCustomers; }
    }
}