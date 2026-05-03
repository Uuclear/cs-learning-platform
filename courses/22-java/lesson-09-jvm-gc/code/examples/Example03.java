public class Example03 {
    public static void main(String[] args) throws InterruptedException {
        printMemoryInfo("程序开始");

        // 分配大对象
        byte[] bigArray = new byte[100 * 1024 * 1024]; // 100MB
        printMemoryInfo("分配100MB数组后");

        // 让数组变为不可达
        bigArray = null;
        printMemoryInfo("数组引用置空后");

        // 触发GC
        System.gc();
        Thread.sleep(1000);
        printMemoryInfo("GC后");
    }

    private static void printMemoryInfo(String stage) {
        Runtime runtime = Runtime.getRuntime();
        long totalMemory = runtime.totalMemory() / (1024 * 1024);
        long freeMemory = runtime.freeMemory() / (1024 * 1024);
        long usedMemory = totalMemory - freeMemory;

        System.out.println(stage + " - 总内存: " + totalMemory + " MB, " +
                          "已用内存: " + usedMemory + " MB, " +
                          "可用内存: " + freeMemory + " MB");
    }
}