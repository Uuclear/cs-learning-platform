/**
 * Example03: 受检异常 vs 非受检异常对比
 * 演示两种异常类型的不同处理方式和编译时行为
 */

import java.io.*;
import java.util.*;

public class Example03 {
    public static void main(String[] args) {
        System.out.println("=== Example 3: 受检异常 vs 非受检异常 ===");
        
        // 第一部分：非受检异常（RuntimeException）
        System.out.println("\n--- 非受检异常示例 ---");
        demonstrateUncheckedException();
        
        // 第二部分：受检异常（必须处理或声明）
        System.out.println("\n--- 受检异常示例 ---");
        try {
            demonstrateCheckedException();
        } catch (IOException e) {
            System.out.println("捕获到IOException: " + e.getMessage());
        }
        
        // 第三部分：方法签名中的throws声明
        System.out.println("\n--- throws声明示例 ---");
        demonstrateThrowsDeclaration();
    }
    
    /**
     * 非受检异常示例 - 不需要在方法签名中声明
     */
    public static void demonstrateUncheckedException() {
        // NullPointerException - 非受检异常
        String str = null;
        try {
            int length = str.length(); // 这里会抛出NullPointerException
        } catch (NullPointerException e) {
            System.out.println("捕获到NullPointerException (非受检异常): " + e.getMessage());
        }
        
        // ArrayIndexOutOfBoundsException - 非受检异常
        int[] arr = {1, 2, 3};
        try {
            int value = arr[10]; // 这里会抛出ArrayIndexOutOfBoundsException
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("捕获到ArrayIndexOutOfBoundsException (非受检异常): " + e.getMessage());
        }
    }
    
    /**
     * 受检异常示例 - 必须在方法签名中声明或在方法内处理
     * @throws IOException 可能抛出的受检异常
     */
    public static void demonstrateCheckedException() throws IOException {
        // FileReader构造函数可能抛出FileNotFoundException（IOException的子类）
        FileReader reader = new FileReader("nonexistent-file.txt");
        reader.close();
    }
    
    /**
     * 演示throws声明的传递性
     */
    public static void demonstrateThrowsDeclaration() {
        try {
            // 调用声明了throws的方法
            methodThatThrowsCheckedException();
        } catch (IOException e) {
            System.out.println("在调用处捕获受检异常: " + e.getMessage());
        }
    }
    
    /**
     * 声明抛出受检异常的方法
     * @throws IOException 受检异常
     */
    public static void methodThatThrowsCheckedException() throws IOException {
        // 模拟可能失败的IO操作
        throw new IOException("模拟IO异常");
    }
    
    /**
     * 对比：如果这个方法抛出的是非受检异常，则不需要throws声明
     */
    public static void methodThatThrowsUncheckedException() {
        // 抛出非受检异常，不需要声明
        throw new IllegalArgumentException("模拟参数异常");
    }
}
