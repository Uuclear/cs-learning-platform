// Example03.java - 线程池（ExecutorService）提交任务
import java.util.concurrent.*;
import java.util.List;
import java.util.ArrayList;

public class Example03 {
    public static void main(String[] args) {
        System.out.println("=== Java 多线程示例 3: 线程池使用 ===");

        // 创建固定大小的线程池（4个线程）
        ExecutorService executor = Executors.newFixedThreadPool(4);

        // 提交 Runnable 任务
        System.out.println("提交 Runnable 任务:");
        for (int i = 0; i < 5; i++) {
            final int taskId = i;
            executor.submit(() -> {
                System.out.println("Runnable 任务 " + taskId + " 在线程 " +
                    Thread.currentThread().getName() + " 中执行");
                try {
                    Thread.sleep(1000);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                System.out.println("Runnable 任务 " + taskId + " 完成");
            });
        }

        // 提交 Callable 任务（有返回值）
        System.out.println("\n提交 Callable 任务:");
        List<Future<String>> futures = new ArrayList<>();
        for (int i = 0; i < 3; i++) {
            final int taskId = i;
            Future<String> future = executor.submit(() -> {
                String result = "Callable 任务 " + taskId + " 的结果";
                System.out.println(result + " 在线程 " +
                    Thread.currentThread().getName() + " 中执行");
                Thread.sleep(1500);
                return result;
            });
            futures.add(future);
        }

        // 获取 Callable 任务的结果
        try {
            for (int i = 0; i < futures.size(); i++) {
                String result = futures.get(i).get(); // 阻塞直到任务完成
                System.out.println("获取到结果: " + result);
            }
        } catch (InterruptedException | ExecutionException e) {
            e.printStackTrace();
        }

        // 关闭线程池
        executor.shutdown();
        try {
            // 等待所有任务完成，最多等待60秒
            if (!executor.awaitTermination(60, TimeUnit.SECONDS)) {
                executor.shutdownNow(); // 强制关闭
            }
        } catch (InterruptedException e) {
            executor.shutdownNow();
        }

        System.out.println("线程池已关闭，所有任务完成！");
    }
}