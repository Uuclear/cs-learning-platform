// Solution01.java - 线程创建与 Runnable vs Thread (完整解决方案)
public class Solution01 {
    public static void main(String[] args) {
        System.out.println("=== Java 多线程解决方案 1: 线程创建的完整示例 ===");

        // 方式1: 继承 Thread 类（适用于简单场景）
        Thread thread1 = new MyThreadSolution("继承Thread方式");
        thread1.start();

        // 方式2: 实现 Runnable 接口（推荐方式，更灵活）
        Thread thread2 = new Thread(new MyRunnableSolution("实现Runnable方式"));
        thread2.start();

        // 方式3: 使用 Lambda 表达式（最简洁）
        Thread thread3 = new Thread(() -> {
            System.out.println("Lambda线程开始执行...");
            for (int i = 0; i < 5; i++) {
                System.out.println("Lambda线程 - 步骤 " + (i + 1));
                try {
                    Thread.sleep(300);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt(); // 恢复中断状态
                    System.out.println("Lambda线程被中断");
                    return;
                }
            }
            System.out.println("Lambda线程执行完毕");
        });
        thread3.start();

        // 方式4: 使用匿名内部类
        Thread thread4 = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("匿名内部类线程开始执行...");
                for (int i = 0; i < 3; i++) {
                    System.out.println("匿名内部类线程 - 循环 " + i);
                    try {
                        Thread.sleep(400);
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        return;
                    }
                }
                System.out.println("匿名内部类线程执行完毕");
            }
        });
        thread4.start();

        // 主线程等待所有子线程完成
        try {
            thread1.join();
            thread2.join();
            thread3.join();
            thread4.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            System.out.println("主线程被中断");
        }

        System.out.println("=== 所有线程执行完毕！ ===");

        // 最佳实践说明：
        // 1. 优先使用 Runnable 接口而不是继承 Thread
        // 2. 使用 Lambda 表达式简化代码
        // 3. 正确处理 InterruptedException
        // 4. 使用 join() 等待线程完成
    }
}

// 继承 Thread 类的完整实现
class MyThreadSolution extends Thread {
    private String threadName;

    public MyThreadSolution(String name) {
        this.threadName = name;
    }

    @Override
    public void run() {
        System.out.println(threadName + " 开始执行...");
        for (int i = 0; i < 4; i++) {
            System.out.println(threadName + " - 执行第 " + (i + 1) + " 次");
            try {
                Thread.sleep(600);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt(); // 恢复中断状态
                System.out.println(threadName + " 被中断，提前退出");
                return;
            }
        }
        System.out.println(threadName + " 执行完毕");
    }
}

// 实现 Runnable 接口的完整实现
class MyRunnableSolution implements Runnable {
    private String taskName;

    public MyRunnableSolution(String name) {
        this.taskName = name;
    }

    @Override
    public void run() {
        System.out.println(taskName + " 开始执行...");
        for (int i = 0; i < 4; i++) {
            System.out.println(taskName + " - 处理任务 " + (i + 1));
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                System.out.println(taskName + " 被中断，停止执行");
                return;
            }
        }
        System.out.println(taskName + " 执行完毕");
    }
}