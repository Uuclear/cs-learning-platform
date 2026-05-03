import java.util.WeakHashMap;
import java.util.Map;

public class Solution01 {
    // 使用WeakHashMap避免内存泄漏，当对象没有其他强引用时会被自动移除
    private static Map<String, String> cache = new WeakHashMap<>();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("初始可用内存: " + getFreeMemoryMB() + " MB");

        // 创建临时对象并放入缓存
        for (int i = 0; i < 100000; i++) {
            String key = "key-" + i;
            String value = "This is a very long string to consume memory #" + i;
            cache.put(key, value);

            // 不保留对value的强引用，让GC可以回收
            if (i % 10000 == 0) {
                System.gc(); // 建议GC，清理WeakHashMap中的条目
                Thread.sleep(100);
                System.out.println("处理了 " + i + " 条记录，当前可用内存: " + getFreeMemoryMB() + " MB");
            }
        }

        System.out.println("最终可用内存: " + getFreeMemoryMB() + " MB");
    }

    private static long getFreeMemoryMB() {
        return Runtime.getRuntime().freeMemory() / (1024 * 1024);
    }
}