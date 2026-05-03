public class Solution02 {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("GC前可用内存: " + getFreeMemoryMB() + " MB");

        // 重用对象而不是创建新对象
        reuseObjects();

        System.out.println("重用对象后可用内存: " + getFreeMemoryMB() + " MB");

        // 触发GC清理临时对象
        System.gc();
        Thread.sleep(1000);
        System.out.println("GC后可用内存: " + getFreeMemoryMB() + " MB");
    }

    private static void reuseObjects() {
        // 创建一个可重用的对象
        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < 1000000; i++) {
            sb.setLength(0); // 清空内容，重用StringBuilder
            sb.append("Object-").append(i);
            // 使用sb进行操作...
        }
    }

    private static long getFreeMemoryMB() {
        return Runtime.getRuntime().freeMemory() / (1024 * 1024);
    }
}