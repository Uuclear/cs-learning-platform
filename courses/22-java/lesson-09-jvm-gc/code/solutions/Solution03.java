public class Solution03 {
    public static void main(String[] args) throws InterruptedException {
        printMemoryInfo("程序开始");

        // 使用try-with-resources确保资源正确释放
        try (MemoryIntensiveOperation operation = new MemoryIntensiveOperation()) {
            operation.perform();
            printMemoryInfo("执行内存密集操作后");
        } catch (Exception e) {
            System.err.println("操作失败: " + e.getMessage());
        }

        // 对象超出作用域，可以被GC回收
        System.gc();
        Thread.sleep(1000);
        printMemoryInfo("GC后");
    }

    private static void printMemoryInfo(String stage) {
        Runtime runtime = Runtime.getRuntime();
        long maxMemory = runtime.maxMemory() / (1024 * 1024);
        long totalMemory = runtime.totalMemory() / (1024 * 1024);
        long freeMemory = runtime.freeMemory() / (1024 * 1024);
        long usedMemory = totalMemory - freeMemory;

        System.out.println(stage + " - 最大内存: " + maxMemory + " MB, " +
                          "总内存: " + totalMemory + " MB, " +
                          "已用内存: " + usedMemory + " MB, " +
                          "可用内存: " + freeMemory + " MB");
    }

    // 模拟需要显式清理的资源
    static class MemoryIntensiveOperation implements AutoCloseable {
        private byte[] data;

        public void perform() {
            data = new byte[100 * 1024 * 1024]; // 100MB
            // 模拟一些处理...
        }

        @Override
        public void close() {
            // 显式清理资源
            data = null;
        }
    }
}