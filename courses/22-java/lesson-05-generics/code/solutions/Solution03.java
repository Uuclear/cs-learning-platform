import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Solution03: 泛型工具类
 * 实现 CollectionUtils 类，包含常用的集合操作方法
 */
public class Solution03 {

    public static class CollectionUtils {

        /**
         * 交换列表中两个位置的元素
         */
        public static <T> void swap(List<T> list, int i, int j) {
            if (list == null) {
                throw new IllegalArgumentException("List cannot be null");
            }
            if (i < 0 || i >= list.size() || j < 0 || j >= list.size()) {
                throw new IndexOutOfBoundsException("Index out of bounds");
            }

            T temp = list.get(i);
            list.set(i, list.get(j));
            list.set(j, temp);
        }

        /**
         * 找到列表中的最小元素
         */
        public static <T extends Comparable<T>> T findMin(List<T> list) {
            if (list == null || list.isEmpty()) {
                throw new IllegalArgumentException("List cannot be null or empty");
            }

            T min = list.get(0);
            for (int i = 1; i < list.size(); i++) {
                if (list.get(i).compareTo(min) < 0) {
                    min = list.get(i);
                }
            }
            return min;
        }

        /**
         * 返回原列表的反转副本
         */
        public static <T> List<T> reverse(List<T> original) {
            if (original == null) {
                throw new IllegalArgumentException("List cannot be null");
            }

            List<T> reversed = new ArrayList<>(original);
            Collections.reverse(reversed);
            return reversed;
        }
    }

    public static void main(String[] args) {
        // 测试 swap 方法
        List<String> names = new ArrayList<>(java.util.Arrays.asList("Alice", "Bob", "Charlie", "David"));
        System.out.println("Original: " + names);
        CollectionUtils.swap(names, 0, 3);
        System.out.println("After swap(0,3): " + names);

        // 测试 findMin 方法
        List<Integer> numbers = java.util.Arrays.asList(5, 2, 8, 1, 9);
        Integer min = CollectionUtils.findMin(numbers);
        System.out.println("Minimum number: " + min);

        List<String> words = java.util.Arrays.asList("zebra", "apple", "banana", "cherry");
        String minWord = CollectionUtils.findMin(words);
        System.out.println("Minimum word: " + minWord);

        // 测试 reverse 方法
        List<Integer> originalNumbers = java.util.Arrays.asList(1, 2, 3, 4, 5);
        List<Integer> reversedNumbers = CollectionUtils.reverse(originalNumbers);
        System.out.println("Original numbers: " + originalNumbers);
        System.out.println("Reversed numbers: " + reversedNumbers);
    }
}