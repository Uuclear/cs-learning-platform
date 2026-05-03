import java.util.*;

public class Solution01 {
    public static void main(String[] args) {
        // 购物车实现解决方案

        ShoppingCart cart = new ShoppingCart();

        // 添加商品
        cart.addItem("苹果", 3);
        cart.addItem("香蕉", 2);
        cart.addItem("橙子", 5);
        cart.addItem("苹果", 2); // 增加苹果数量

        System.out.println("购物车内容:");
        cart.displayCart();

        System.out.println("总价: $" + cart.getTotalPrice());

        // 删除商品
        cart.removeItem("香蕉");
        System.out.println("\n删除香蕉后:");
        cart.displayCart();

        // 更新商品数量
        cart.updateQuantity("橙子", 3);
        System.out.println("\n更新橙子数量为3后:");
        cart.displayCart();
    }
}

class ShoppingCart {
    // 商品名 -> 数量
    private Map<String, Integer> items;
    // 商品价格表（简化示例）
    private static final Map<String, Double> PRICES = Map.of(
        "苹果", 1.5,
        "香蕉", 0.8,
        "橙子", 2.0
    );

    public ShoppingCart() {
        this.items = new HashMap<>();
    }

    public void addItem(String itemName, int quantity) {
        if (quantity <= 0) {
            System.out.println("数量必须大于0");
            return;
        }

        if (!PRICES.containsKey(itemName)) {
            System.out.println("商品 " + itemName + " 不存在");
            return;
        }

        items.put(itemName, items.getOrDefault(itemName, 0) + quantity);
    }

    public void removeItem(String itemName) {
        items.remove(itemName);
    }

    public void updateQuantity(String itemName, int quantity) {
        if (quantity <= 0) {
            removeItem(itemName);
        } else {
            if (PRICES.containsKey(itemName)) {
                items.put(itemName, quantity);
            }
        }
    }

    public double getTotalPrice() {
        double total = 0.0;
        for (Map.Entry<String, Integer> entry : items.entrySet()) {
            String itemName = entry.getKey();
            int quantity = entry.getValue();
            double price = PRICES.get(itemName);
            total += price * quantity;
        }
        return total;
    }

    public void displayCart() {
        if (items.isEmpty()) {
            System.out.println("购物车为空");
            return;
        }

        for (Map.Entry<String, Integer> entry : items.entrySet()) {
            String itemName = entry.getKey();
            int quantity = entry.getValue();
            double price = PRICES.get(itemName);
            double itemTotal = price * quantity;
            System.out.printf("%s x %d @ $%.2f = $%.2f%n",
                itemName, quantity, price, itemTotal);
        }
    }
}