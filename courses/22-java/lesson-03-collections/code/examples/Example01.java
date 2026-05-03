import java.util.*;

public class Example01 {
    public static void main(String[] args) {
        // 演示 ArrayList 和 LinkedList 的基本操作对比

        System.out.println("=== ArrayList vs LinkedList 操作对比 ===\n");

        // 创建 ArrayList 和 LinkedList
        List<Integer> arrayList = new ArrayList<>();
        List<Integer> linkedList = new LinkedList<>();

        // 1. 在末尾添加元素
        System.out.println("1. 在末尾添加元素:");
        long startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            arrayList.add(i);
        }
        long endTime = System.nanoTime();
        System.out.println("ArrayList 添加10000个元素耗时: " + (endTime - startTime) / 1000000.0 + " ms");

        startTime = System.nanoTime();
        for (int i = 0; i < 10000; i++) {
            linkedList.add(i);
        }
        endTime = System.nanoTime();
        System.out.println("LinkedList 添加10000个元素耗时: " + (endTime - startTime) / 1000000.0 + " ms\n");

        // 2. 在开头插入元素
        System.out.println("2. 在开头插入元素:");
        startTime = System.nanoTime();
        arrayList.add(0, -1);
        endTime = System.nanoTime();
        System.out.println("ArrayList 在开头插入耗时: " + (endTime - startTime) / 1000000.0 + " ms");

        startTime = System.nanoTime();
        linkedList.add(0, -1);
        endTime = System.nanoTime();
        System.out.println("LinkedList 在开头插入耗时: " + (endTime - startTime) / 1000000.0 + " ms\n");

        // 3. 随机访问元素
        System.out.println("3. 随机访问元素:");
        startTime = System.nanoTime();
        int value1 = arrayList.get(5000);
        endTime = System.nanoTime();
        System.out.println("ArrayList 随机访问耗时: " + (endTime - startTime) / 1000000.0 + " ms, 值: " + value1);

        startTime = System.nanoTime();
        int value2 = linkedList.get(5000);
        endTime = System.nanoTime();
        System.out.println("LinkedList 随机访问耗时: " + (endTime - startTime) / 1000000.0 + " ms, 值: " + value2);

        // 4. 遍历所有元素
        System.out.println("\n4. 遍历所有元素:");
        startTime = System.nanoTime();
        for (Integer num : arrayList) {
            // 简单访问
            int temp = num;
        }
        endTime = System.nanoTime();
        System.out.println("ArrayList 遍历耗时: " + (endTime - startTime) / 1000000.0 + " ms");

        startTime = System.nanoTime();
        for (Integer num : linkedList) {
            // 简单访问
            int temp = num;
        }
        endTime = System.nanoTime();
        System.out.println("LinkedList 遍历耗时: " + (endTime - startTime) / 1000000.0 + " ms");

        // 5. 删除中间元素
        System.out.println("\n5. 删除中间元素:");
        startTime = System.nanoTime();
        arrayList.remove(5000);
        endTime = System.nanoTime();
        System.out.println("ArrayList 删除中间元素耗时: " + (endTime - startTime) / 1000000.0 + " ms");

        startTime = System.nanoTime();
        linkedList.remove(5000);
        endTime = System.nanoTime();
        System.out.println("LinkedList 删除中间元素耗时: " + (endTime - startTime) / 1000000.0 + " ms");
    }
}