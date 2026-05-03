public class Example02 {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("GC前可用内存: " + getFreeMemoryMB() + " MB");

        // 创建大量临时对象
        createObjects();

        System.out.println("创建对象后可用内存: " + getFreeMemoryMB() + " MB");

        // 显式建议JVM进行GC（不保证立即执行）
        System.gc();
        Thread.sleep(1000); // 给GC一些时间

        System.out.println("GC后可用内存: " + getFreeMemoryMB() + " MB");
    }

    private static void createObjects() {
        for (int i = 0; i < 1000000; i++) {
            new Object();
        }
    }

    private static long getFreeMemoryMB() {
        return Runtime.getRuntime().freeMemory() / (1024 * 1024);
    }
}