/**
 * Example01: try-catch-finally 基础示例
 * 演示基本的异常处理结构和finally块的执行
 */
public class Example01 {
    public static void main(String[] args) {
        System.out.println("=== Example 1: try-catch-finally 基础 ===");
        
        // 测试正常情况
        System.out.println("\n测试正常情况:");
        try {
            int result = divide(10, 2);
            System.out.println("10 ÷ 2 = " + result);
        } catch (ArithmeticException e) {
            System.out.println("捕获到算术异常: " + e.getMessage());
        } finally {
            System.out.println("finally块总是执行!");
        }
        
        // 测试异常情况
        System.out.println("\n测试异常情况:");
        try {
            int result = divide(10, 0);
            System.out.println("这行不会执行");
        } catch (ArithmeticException e) {
            System.out.println("捕获到算术异常: " + e.getMessage());
        } finally {
            System.out.println("finally块仍然执行!");
        }
        
        // 测试return语句中的finally
        System.out.println("\n测试return语句中的finally:");
        int returnValue = testFinallyWithReturn();
        System.out.println("方法返回值: " + returnValue);
    }
    
    /**
     * 除法运算，可能抛出ArithmeticException
     */
    public static int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("除数不能为零");
        }
        return a / b;
    }
    
    /**
     * 测试finally块在return语句中的行为
     */
    public static int testFinallyWithReturn() {
        try {
            System.out.println("try块中，准备返回10");
            return 10;
        } finally {
            System.out.println("finally块执行，但不影响返回值");
            // 注意：这里不能改变返回值
        }
    }
}
