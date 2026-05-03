package solutions;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * 解决方案2: Stream filter/map/collect 链式操作
 * 这是 Example02.java 的完整解决方案，包含所有练习的答案
 */
public class Solution02 {
    // 辅助类：学生
    static class Student {
        private String name;
        private int age;
        private double score;
        private String major;
        private boolean married;

        public Student(String name, int age, double score, String major, boolean married) {
            this.name = name;
            this.age = age;
            this.score = score;
            this.major = major;
            this.married = married;
        }

        // Getters
        public String getName() { return name; }
        public int getAge() { return age; }
        public double getScore() { return score; }
        public String getMajor() { return major; }
        public boolean isMarried() { return married; }

        @Override
        public String toString() {
            return String.format("Student{name='%s', age=%d, score=%.1f, major='%s', married=%b}",
                               name, age, score, major, married);
        }
    }

    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Alice", 20, 85.5, "Computer Science", true),
            new Student("Bob", 19, 78.0, "Mathematics", false),
            new Student("Charlie", 21, 92.5, "Computer Science", true),
            new Student("Diana", 20, 88.0, "Physics", false),
            new Student("Eve", 22, 95.0, "Computer Science", true),
            new Student("Frank", 18, 72.5, "Mathematics", false),
            new Student("Grace", 23, 89.5, "Physics", true),
            new Student("Henry", 24, 91.0, "Computer Science", true)
        );

        System.out.println("=== 原始学生列表 ===");
        students.forEach(System.out::println);

        // 练习1：找出长度大于5的字符串，并转换为大写
        System.out.println("\n=== 练习1：字符串处理 ===");
        List<String> words = Arrays.asList("apple", "banana", "cat", "dog", "elephant", "fox");
        List<String> longWordsUppercase = words.stream()
            .filter(word -> word.length() > 5)
            .map(String::toUpperCase)
            .collect(Collectors.toList());
        System.out.println("长度大于5的单词（大写）: " + longWordsUppercase);

        // 练习2：找出工资最高的前5名已婚员工的平均年龄
        // 注意：这里我们用分数代替工资，因为我们的Student类没有工资字段
        System.out.println("\n=== 练习2：已婚学生的平均年龄（按分数排序前5名） ===");
        OptionalDouble averageAgeOfTopMarriedStudents = students.stream()
            .filter(Student::isMarried)                    // 筛选已婚学生
            .sorted(Comparator.comparing(Student::getScore).reversed()) // 按分数降序
            .limit(5)                                      // 取前5名
            .mapToInt(Student::getAge)                     // 获取年龄
            .average();                                    // 计算平均值

        if (averageAgeOfTopMarriedStudents.isPresent()) {
            System.out.printf("前5名已婚学生的平均年龄: %.2f%n", averageAgeOfTopMarriedStudents.getAsDouble());
        } else {
            System.out.println("没有找到符合条件的学生");
        }

        // 练习3：按产品类别分组，并计算每个类别的总销售额和平均单价
        // 我们需要创建一些产品数据来演示
        System.out.println("\n=== 练习3：产品销售统计 ===");
        List<ProductSale> productSales = Arrays.asList(
            new ProductSale("Electronics", "Laptop", 1200.0, 2),
            new ProductSale("Electronics", "Mouse", 25.5, 10),
            new ProductSale("Books", "Novel", 15.99, 5),
            new ProductSale("Electronics", "Keyboard", 75.0, 8),
            new ProductSale("Books", "Textbook", 45.0, 3),
            new ProductSale("Clothing", "T-Shirt", 20.0, 15)
        );

        Map<String, SalesSummary> salesByCategory = productSales.stream()
            .collect(Collectors.groupingBy(
                ProductSale::getCategory,
                Collectors.collectingAndThen(
                    Collectors.toList(),
                    sales -> {
                        double totalRevenue = sales.stream()
                            .mapToDouble(s -> s.getPrice() * s.getQuantity())
                            .sum();
                        double avgPrice = sales.stream()
                            .mapToDouble(ProductSale::getPrice)
                            .average()
                            .orElse(0.0);
                        return new SalesSummary(totalRevenue, avgPrice, sales.size());
                    }
                )
            ));

        salesByCategory.forEach((category, summary) -> {
            System.out.printf("%s: 总销售额=$%.2f, 平均单价=$%.2f, 销售记录数=%d%n",
                category, summary.getTotalRevenue(), summary.getAveragePrice(), summary.getRecordCount());
        });

        // 额外演示：复杂的链式操作
        System.out.println("\n=== 额外演示：复杂链式操作 ===");
        // 找出计算机专业中分数高于平均分的已婚学生的姓名
        double csAverageScore = students.stream()
            .filter(student -> "Computer Science".equals(student.getMajor()))
            .mapToDouble(Student::getScore)
            .average()
            .orElse(0.0);

        System.out.printf("计算机专业平均分: %.2f%n", csAverageScore);

        List<String> highScoringMarriedCsStudents = students.stream()
            .filter(student -> "Computer Science".equals(student.getMajor()))
            .filter(Student::isMarried)
            .filter(student -> student.getScore() > csAverageScore)
            .map(Student::getName)
            .collect(Collectors.toList());

        System.out.println("计算机专业中分数高于平均分的已婚学生: " + highScoringMarriedCsStudents);
    }

    // 辅助类：产品销售记录
    static class ProductSale {
        private String category;
        private String productName;
        private double price;
        private int quantity;

        public ProductSale(String category, String productName, double price, int quantity) {
            this.category = category;
            this.productName = productName;
            this.price = price;
            this.quantity = quantity;
        }

        public String getCategory() { return category; }
        public String getProductName() { return productName; }
        public double getPrice() { return price; }
        public int getQuantity() { return quantity; }
    }

    // 辅助类：销售摘要
    static class SalesSummary {
        private double totalRevenue;
        private double averagePrice;
        private int recordCount;

        public SalesSummary(double totalRevenue, double averagePrice, int recordCount) {
            this.totalRevenue = totalRevenue;
            this.averagePrice = averagePrice;
            this.recordCount = recordCount;
        }

        public double getTotalRevenue() { return totalRevenue; }
        public double getAveragePrice() { return averagePrice; }
        public int getRecordCount() { return recordCount; }
    }
}