// Solution02.java - synchronized 同步块与线程安全计数器 (完整解决方案)
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.ReentrantLock;

public class Solution02 {
    public static void main(String[] args) throws InterruptedException {
        System.out.println("=== Java 多线程解决方案 2: 线程安全的多种实现方式 ===");

        // 测试1: synchronized 方法
        testSynchronizedCounter();

        // 测试2: synchronized 块
        testSynchronizedBlockCounter();

        // 测试3: volatile + AtomicInteger
        testAtomicCounter();

        // 测试4: ReentrantLock
        testReentrantLockCounter();

        System.out.println("=== 所有测试完成！ ===");
    }

    private static void testSynchronizedCounter() throws InterruptedException {
        System.out.println("\n--- 测试 synchronized 方法 ---");
        SynchronizedCounter counter = new SynchronizedCounter();
        Thread[] threads = createThreads(counter, 10, 1000);
        waitForThreads(threads);
        System.out.println("synchronized 方法结果: " + counter.getValue() +
                          " (期望: 10000, 正确: " + (counter.getValue() == 10000) + ")");
    }

    private static void testSynchronizedBlockCounter() throws InterruptedException {
        System.out.println("\n--- 测试 synchronized 块 ---");
        SynchronizedBlockCounter counter = new SynchronizedBlockCounter();
        Thread[] threads = createThreads(counter, 10, 1000);
        waitForThreads(threads);
        System.out.println("synchronized 块结果: " + counter.getValue() +
                          " (期望: 10000, 正确: " + (counter.getValue() == 10000) + ")");
    }

    private static void testAtomicCounter() throws InterruptedException {
        System.out.println("\n--- 测试 AtomicInteger ---");
        AtomicCounter counter = new AtomicCounter();
        Thread[] threads = createThreads(counter, 10, 1000);
        waitForThreads(threads);
        System.out.println("AtomicInteger 结果: " + counter.getValue() +
                          " (期望: 10000, 正确: " + (counter.getValue() == 10000) + ")");
    }

    private static void testReentrantLockCounter() throws InterruptedException {
        System.out.println("\n--- 测试 ReentrantLock ---");
        ReentrantLockCounter counter = new ReentrantLockCounter();
        Thread[] threads = createThreads(counter, 10, 1000);
        waitForThreads(threads);
        System.out.println("ReentrantLock 结果: " + counter.getValue() +
                          " (期望: 10000, 正确: " + (counter.getValue() == 10000) + ")");
    }

    private static Thread[] createThreads(Incrementable counter, int threadCount, int incrementsPerThread) {
        Thread[] threads = new Thread[threadCount];
        for (int i = 0; i < threadCount; i++) {
            threads[i] = new Thread(() -> {
                for (int j = 0; j < incrementsPerThread; j++) {
                    counter.increment();
                }
            });
            threads[i].start();
        }
        return threads;
    }

    private static void waitForThreads(Thread[] threads) throws InterruptedException {
        for (Thread thread : threads) {
            thread.join();
        }
    }
}

// 接口定义
interface Incrementable {
    void increment();
    long getValue();
}

// synchronized 方法实现
class SynchronizedCounter implements Incrementable {
    private long value = 0;

    @Override
    public synchronized void increment() {
        value++;
    }

    @Override
    public long getValue() {
        return value;
    }
}

// synchronized 块实现
class SynchronizedBlockCounter implements Incrementable {
    private long value = 0;
    private final Object lock = new Object();

    @Override
    public void increment() {
        synchronized (lock) {
            value++;
        }
    }

    @Override
    public long getValue() {
        synchronized (lock) {
            return value;
        }
    }
}

// AtomicInteger 实现
class AtomicCounter implements Incrementable {
    private final AtomicInteger value = new AtomicInteger(0);

    @Override
    public void increment() {
        value.incrementAndGet();
    }

    @Override
    public long getValue() {
        return value.get();
    }
}

// ReentrantLock 实现
class ReentrantLockCounter implements Incrementable {
    private long value = 0;
    private final ReentrantLock lock = new ReentrantLock();

    @Override
    public void increment() {
        lock.lock();
        try {
            value++;
        } finally {
            lock.unlock();
        }
    }

    @Override
    public long getValue() {
        lock.lock();
        try {
            return value;
        } finally {
            lock.unlock();
        }
    }
}