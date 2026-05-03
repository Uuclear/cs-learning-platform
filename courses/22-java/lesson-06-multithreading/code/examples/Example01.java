// Example01.java - 线程创建与 Runnable vs Thread
public class Example01 {
    public static void main(String[] args) {
        System.out.println("=== Java 多线程示例 1: 线程创建方式 ===");

        // 方式1: 继承 Thread 类
        Thread thread1 = new MyThread("继承Thread");
        thread1.start();

        // 方式2: 实现 Runnable 接口
        Thread thread2 = new Thread(new MyRunnable("实现Runnable"));
        thread2.start();

        // 方式3: 使用 Lambda 表达式 (Java 8+)
        Thread thread3 = new Thread(() -> {
            for (int i = 0; i < 3; i++) {
                System.out.println("Lambda线程执行: " + i);
                try {
                    Thread.sleep(500);
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
        });
        thread3.start();

        // 主线程等待所有子线程完成
        try {
            thread1.join();
            thread2.join();
            thread3.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("所有线程执行完毕！");
    }
}

// 继承 Thread 类的方式
class MyThread extends Thread {
    private String name;

    public MyThread(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 0; i < 3; i++) {
            System.out.println(name + " 执行: " + i);
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}

// 实现 Runnable 接口的方式
class MyRunnable implements Runnable {
    private String name;

    public MyRunnable(String name) {
        this.name = name;
    }

    @Override
    public void run() {
        for (int i = 0; i < 3; i++) {
            System.out.println(name + " 执行: " + i);
            try {
                Thread.sleep(800);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}