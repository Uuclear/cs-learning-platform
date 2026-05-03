import java.util.*;

public class Solution03 {
    public static void main(String[] args) {
        // 去重电话号码解决方案

        List<String> phoneNumbers = Arrays.asList(
            "138-0013-8001",
            "139-0013-8002",
            "138-0013-8001", // 重复
            "137-0013-8003",
            "136-0013-8004",
            "139-0013-8002", // 重复
            "135-0013-8005",
            "138-0013-8001"  // 重复
        );

        System.out.println("=== 去重电话号码 ===\n");
        System.out.println("原始电话号码列表:");
        for (String number : phoneNumbers) {
            System.out.println("  " + number);
        }

        List<String> uniqueSortedNumbers = removeDuplicatesAndSort(phoneNumbers);

        System.out.println("\n去重并排序后的电话号码:");
        for (String number : uniqueSortedNumbers) {
            System.out.println("  " + number);
        }

        System.out.println("\n总共去除了 " + (phoneNumbers.size() - uniqueSortedNumbers.size()) + " 个重复号码");
    }

    /**
     * 去除电话号码列表中的重复项，并按字母顺序排序
     * @param phoneNumbers 原始电话号码列表
     * @return 去重并排序后的电话号码列表
     */
    public static List<String> removeDuplicatesAndSort(List<String> phoneNumbers) {
        if (phoneNumbers == null || phoneNumbers.isEmpty()) {
            return new ArrayList<>();
        }

        // 使用 TreeSet 自动去重并排序
        Set<String> uniqueNumbers = new TreeSet<>(phoneNumbers);

        // 转换为列表返回
        return new ArrayList<>(uniqueNumbers);
    }

    /**
     * 另一种实现方式：先用 HashSet 去重，再用 Collections.sort() 排序
     */
    public static List<String> removeDuplicatesAndSortAlternative(List<String> phoneNumbers) {
        if (phoneNumbers == null || phoneNumbers.isEmpty()) {
            return new ArrayList<>();
        }

        // 使用 HashSet 去重
        Set<String> uniqueNumbers = new HashSet<>(phoneNumbers);

        // 转换为列表并排序
        List<String> result = new ArrayList<>(uniqueNumbers);
        Collections.sort(result);

        return result;
    }
}