// Example02.java - synchronized 同步块与线程安全计数器
public class Example02 {
    public static void main(String[] args) {
        System.out.println("=== Java 多线程示例 2: 线程安全与同步 ===");

        // 创建共享的计数器对象
        SafeCounter safeCounter = new SafeCounter();

        // 创建10个线程同时对计数器进行递增操作
        Thread[] threads = new Thread[10];
        for (int i = 0; i < 10; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < 1000; j++) {
                    safeCounter.increment();
                }
            });
            threads[i].start();
        }

        // 等待所有线程完成
        try {
            for (Thread thread : threads) {
                thread.join();
            }
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("最终计数器值: " + safeCounter.getCount());
        System.out.println("期望值: 10000");
        System.out.println("是否正确: " + (safeCounter.getCount() == 10000));
    }
}

class SafeCounter {
    private int count = 0;

    // 方法级别的 synchronized
    public synchronized void increment() {
        count++;
    }

    // synchronized 块的方式（等效）
    public void incrementBlock() {
        synchronized (this) {
            count++;
        }
    }

    public int getCount() {
        return count;
    }
}

// 对比：不安全的计数器
class UnsafeCounter {
    private int count = 0;

    // 没有同步，可能导致数据竞争
    public void increment() {
        count++; // 这不是原子操作！
    }

    public int getCount() {
        return count;
    }
}