import java.util.ArrayList;
import java.util.List;

public class Example01 {
    // 静态集合会一直持有对象引用，导致内存泄漏
    private static List<String> cache = new ArrayList<>();

    public static void main(String[] args) throws InterruptedException {
        System.out.println("初始可用内存: " + getFreeMemoryMB() + " MB");

        // 不断向静态集合添加数据
        for (int i = 0; i < 100000; i++) {
            cache.add("This is a very long string to consume memory #" + i);

            if (i % 10000 == 0) {
                System.out.println("添加了 " + i + " 条记录，当前可用内存: " + getFreeMemoryMB() + " MB");
                Thread.sleep(100); // 给GC一些时间
            }
        }

        System.out.println("最终可用内存: " + getFreeMemoryMB() + " MB");
    }

    private static long getFreeMemoryMB() {
        return Runtime.getRuntime().freeMemory() / (1024 * 1024);
    }
}