/**
 * Solution01: try-catch-finally 练习解决方案
 * 完整的异常处理示例，包含资源管理和多种异常类型
 */
import java.util.Scanner;

public class Solution01 {
    public static void main(String[] args) {
        System.out.println("=== Solution 1: 完整的try-catch-finally示例 ===");
        
        Scanner scanner = null;
        try {
            scanner = new Scanner(System.in);
            
            System.out.print("请输入第一个数字: ");
            int num1 = Integer.parseInt(scanner.nextLine());
            
            System.out.print("请输入第二个数字: ");
            int num2 = Integer.parseInt(scanner.nextLine());
            
            int result = safeDivide(num1, num2);
            System.out.println("结果: " + num1 + " ÷ " + num2 + " = " + result);
            
        } catch (NumberFormatException e) {
            System.out.println("错误: 请输入有效的整数!");
        } catch (ArithmeticException e) {
            System.out.println("错误: " + e.getMessage());
        } finally {
            // 确保Scanner被正确关闭
            if (scanner != null) {
                scanner.close();
                System.out.println("Scanner已关闭");
            }
            System.out.println("程序执行完毕");
        }
    }
    
    /**
     * 安全的除法运算，处理除零情况
     */
    public static int safeDivide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("除数不能为零，请输入非零值");
        }
        return a / b;
    }
}
