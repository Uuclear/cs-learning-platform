// Solution03.java - 线程池（ExecutorService）提交任务 (完整解决方案)
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;
import java.util.stream.IntStream;

public class Solution03 {
    public static void main(String[] args) {
        System.out.println("=== Java 多线程解决方案 3: 线程池的完整使用示例 ===");

        // 示例1: 固定大小线程池
        demonstrateFixedThreadPool();

        // 示例2: 缓存线程池
        demonstrateCachedThreadPool();

        // 示例3: 单线程线程池
        demonstrateSingleThreadExecutor();

        // 示例4: 自定义线程池
        demonstrateCustomThreadPool();

        System.out.println("=== 所有线程池示例完成！ ===");
    }

    private static void demonstrateFixedThreadPool() {
        System.out.println("\n--- 固定大小线程池示例 ---");
        ExecutorService executor = Executors.newFixedThreadPool(3);

        try {
            // 提交多个任务
            List<Future<String>> futures = new ArrayList<>();
            for (int i = 0; i < 6; i++) {
                final int taskId = i;
                Future<String> future = executor.submit(() -> {
                    String threadName = Thread.currentThread().getName();
                    System.out.println("固定线程池任务 " + taskId + " 在 " + threadName + " 中执行");
                    Thread.sleep(1000);
                    return "固定线程池任务 " + taskId + " 完成";
                });
                futures.add(future);
            }

            // 获取结果
            for (Future<String> future : futures) {
                try {
                    System.out.println("结果: " + future.get());
                } catch (InterruptedException | ExecutionException e) {
                    e.printStackTrace();
                }
            }
        } finally {
            shutdownExecutor(executor);
        }
    }

    private static void demonstrateCachedThreadPool() {
        System.out.println("\n--- 缓存线程池示例 ---");
        ExecutorService executor = Executors.newCachedThreadPool();

        try {
            // 提交短时间任务
            for (int i = 0; i < 5; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    String threadName = Thread.currentThread().getName();
                    System.out.println("缓存线程池任务 " + taskId + " 在 " + threadName + " 中执行");
                    try {
                        Thread.sleep(500); // 短时间任务
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    System.out.println("缓存线程池任务 " + taskId + " 完成");
                });
            }

            // 等待一段时间让线程池清理空闲线程
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        } finally {
            shutdownExecutor(executor);
        }
    }

    private static void demonstrateSingleThreadExecutor() {
        System.out.println("\n--- 单线程线程池示例 ---");
        ExecutorService executor = Executors.newSingleThreadExecutor();

        try {
            // 提交多个任务，会按顺序执行
            for (int i = 0; i < 3; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    String threadName = Thread.currentThread().getName();
                    System.out.println("单线程任务 " + taskId + " 在 " + threadName + " 中开始");
                    try {
                        Thread.sleep(800);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    System.out.println("单线程任务 " + taskId + " 完成");
                });
            }
        } finally {
            shutdownExecutor(executor);
        }
    }

    private static void demonstrateCustomThreadPool() {
        System.out.println("\n--- 自定义线程池示例 ---");
        // 创建自定义线程池：核心线程数2，最大线程数4，队列容量3
        ThreadPoolExecutor executor = new ThreadPoolExecutor(
            2,                           // 核心线程数
            4,                           // 最大线程数
            60L,                         // 空闲线程存活时间
            TimeUnit.SECONDS,           // 时间单位
            new ArrayBlockingQueue<>(3), // 有界队列
            new ThreadPoolExecutor.CallerRunsPolicy() // 拒绝策略
        );

        try {
            // 提交8个任务（超过队列容量）
            for (int i = 0; i < 8; i++) {
                final int taskId = i;
                executor.submit(() -> {
                    String threadName = Thread.currentThread().getName();
                    System.out.println("自定义线程池任务 " + taskId + " 在 " + threadName + " 中执行");
                    try {
                        Thread.sleep(1000);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    }
                    System.out.println("自定义线程池任务 " + taskId + " 完成");
                });
            }

            // 打印线程池状态
            System.out.println("活跃线程数: " + executor.getActiveCount());
            System.out.println("已完成任务数: " + executor.getCompletedTaskCount());
            System.out.println("总任务数: " + executor.getTaskCount());
        } finally {
            shutdownExecutor(executor);
        }
    }

    private static void shutdownExecutor(ExecutorService executor) {
        executor.shutdown();
        try {
            if (!executor.awaitTermination(10, TimeUnit.SECONDS)) {
                executor.shutdownNow();
                if (!executor.awaitTermination(5, TimeUnit.SECONDS)) {
                    System.err.println("线程池无法正常关闭");
                }
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
            Thread.currentThread().interrupt();
        }
    }
}