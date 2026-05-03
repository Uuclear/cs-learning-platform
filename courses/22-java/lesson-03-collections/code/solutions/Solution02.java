import java.util.*;
import java.util.stream.Collectors;

public class Solution02 {
    public static void main(String[] args) {
        // 单词频率分析器解决方案

        String text = "Java collections framework is powerful and flexible. " +
                     "The collections framework provides many useful data structures. " +
                     "HashMap, HashSet, ArrayList, and LinkedList are commonly used collections. " +
                     "Understanding when to use each collection type is important for performance. " +
                     "Java programming becomes easier with the collections framework.";

        System.out.println("=== 单词频率分析器 ===\n");
        System.out.println("输入文本:");
        System.out.println(text);

        List<Map.Entry<String, Integer>> topWords = getTopWords(text, 5);

        System.out.println("\n出现频率最高的前5个单词:");
        for (int i = 0; i < topWords.size(); i++) {
            Map.Entry<String, Integer> entry = topWords.get(i);
            System.out.printf("%d. %s: %d次%n", i + 1, entry.getKey(), entry.getValue());
        }
    }

    /**
     * 获取文本中出现频率最高的前N个单词
     * @param text 输入文本
     * @param topN 返回前N个单词
     * @return 按频率降序排列的单词列表
     */
    public static List<Map.Entry<String, Integer>> getTopWords(String text, int topN) {
        if (text == null || text.trim().isEmpty()) {
            return new ArrayList<>();
        }

        // 统计词频
        Map<String, Integer> wordCount = countWords(text);

        // 按频率排序并返回前topN个
        return wordCount.entrySet().stream()
                .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
                .limit(topN)
                .collect(Collectors.toList());
    }

    /**
     * 统计文本中每个单词的出现次数（忽略大小写和标点符号）
     * @param text 输入文本
     * @return 单词到出现次数的映射
     */
    private static Map<String, Integer> countWords(String text) {
        Map<String, Integer> wordCount = new HashMap<>();

        // 转换为小写，移除标点符号，按空格分割
        String[] words = text.toLowerCase()
                            .replaceAll("[^a-zA-Z\\s]", "")
                            .split("\\s+");

        for (String word : words) {
            if (!word.isEmpty()) {
                wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
            }
        }

        return wordCount;
    }
}