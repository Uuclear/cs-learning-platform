import java.util.*;

public class Example02 {
    public static void main(String[] args) {
        // 演示 HashMap 词频统计

        System.out.println("=== HashMap 词频统计示例 ===\n");

        String text = "Java is great Java is powerful Java collections are amazing " +
                     "Collections framework makes programming easier Collections are useful " +
                     "HashMap HashSet ArrayList LinkedList all are part of collections";

        Map<String, Integer> wordCount = countWords(text);

        System.out.println("原始文本: " + text);
        System.out.println("\n词频统计结果:");
        wordCount.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .forEach(entry -> System.out.println(entry.getKey() + ": " + entry.getValue()));

        // 演示其他 HashMap 操作
        System.out.println("\n=== 其他 HashMap 操作 ===");
        Map<String, String> phoneBook = new HashMap<>();

        // 添加联系人
        phoneBook.put("张三", "13800138001");
        phoneBook.put("李四", "13800138002");
        phoneBook.put("王五", "13800138003");

        System.out.println("电话簿内容:");
        for (Map.Entry<String, String> entry : phoneBook.entrySet()) {
            System.out.println(entry.getKey() + " -> " + entry.getValue());
        }

        // 查找联系人
        System.out.println("\n查找张三的电话: " + phoneBook.get("张三"));
        System.out.println("查找赵六的电话: " + phoneBook.getOrDefault("赵六", "未找到"));

        // 检查是否存在
        System.out.println("是否存在李四: " + phoneBook.containsKey("李四"));
        System.out.println("是否存在赵六: " + phoneBook.containsKey("赵六"));

        // 删除联系人
        phoneBook.remove("王五");
        System.out.println("删除王五后，电话簿大小: " + phoneBook.size());
    }

    /**
     * 统计文本中每个单词的出现次数
     * @param text 输入文本
     * @return 单词到出现次数的映射
     */
    public static Map<String, Integer> countWords(String text) {
        Map<String, Integer> wordCount = new HashMap<>();

        // 转换为小写并按空格分割
        String[] words = text.toLowerCase().split("\\s+");

        for (String word : words) {
            // 如果单词已存在，计数加1；否则设为1
            wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
        }

        return wordCount;
    }
}