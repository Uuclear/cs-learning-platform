import java.util.*;

public class Example03 {
    public static void main(String[] args) {
        // 演示 HashSet 去重与迭代器遍历

        System.out.println("=== HashSet 去重与迭代器遍历 ===\n");

        // 创建一个包含重复元素的列表
        List<String> namesWithDuplicates = Arrays.asList(
            "张三", "李四", "王五", "张三", "赵六", "李四", "钱七", "王五"
        );

        System.out.println("原始列表（包含重复）:");
        System.out.println(namesWithDuplicates);

        // 使用 HashSet 自动去重
        Set<String> uniqueNames = new HashSet<>(namesWithDuplicates);
        System.out.println("\n去重后的集合:");
        System.out.println(uniqueNames);
        System.out.println("去重后元素个数: " + uniqueNames.size());

        // 演示不同的遍历方式

        System.out.println("\n=== 遍历方式对比 ===");

        // 1. 使用迭代器遍历
        System.out.println("1. 迭代器遍历:");
        Iterator<String> iterator = uniqueNames.iterator();
        while (iterator.hasNext()) {
            String name = iterator.next();
            System.out.println("  " + name);
        }

        // 2. 使用增强 for 循环（推荐）
        System.out.println("\n2. 增强 for 循环:");
        for (String name : uniqueNames) {
            System.out.println("  " + name);
        }

        // 3. 使用 forEach 和 Lambda 表达式（Java 8+）
        System.out.println("\n3. forEach + Lambda:");
        uniqueNames.forEach(name -> System.out.println("  " + name));

        // 演示在遍历时安全删除元素
        System.out.println("\n=== 安全删除演示 ===");
        Set<String> mutableSet = new HashSet<>(uniqueNames);
        System.out.println("删除前: " + mutableSet);

        // 使用迭代器安全删除
        Iterator<String> safeIterator = mutableSet.iterator();
        while (safeIterator.hasNext()) {
            String name = safeIterator.next();
            if (name.startsWith("张")) {
                safeIterator.remove(); // 安全删除
                System.out.println("删除了: " + name);
            }
        }
        System.out.println("删除后: " + mutableSet);

        // 演示 Set 的其他操作
        System.out.println("\n=== Set 的其他操作 ===");
        Set<Integer> numbers1 = new HashSet<>(Arrays.asList(1, 2, 3, 4, 5));
        Set<Integer> numbers2 = new HashSet<>(Arrays.asList(4, 5, 6, 7, 8));

        System.out.println("集合1: " + numbers1);
        System.out.println("集合2: " + numbers2);

        // 并集
        Set<Integer> union = new HashSet<>(numbers1);
        union.addAll(numbers2);
        System.out.println("并集: " + union);

        // 交集
        Set<Integer> intersection = new HashSet<>(numbers1);
        intersection.retainAll(numbers2);
        System.out.println("交集: " + intersection);

        // 差集
        Set<Integer> difference = new HashSet<>(numbers1);
        difference.removeAll(numbers2);
        System.out.println("差集 (1-2): " + difference);
    }
}