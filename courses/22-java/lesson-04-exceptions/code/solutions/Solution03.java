/**
 * Solution03: 受检异常 vs 非受检异常完整解决方案
 * 演示文件操作中的异常处理最佳实践
 */
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class Solution03 {
    public static void main(String[] args) {
        System.out.println("=== Solution 3: 文件操作异常处理最佳实践 ===");
        
        String filename = "test-data.txt";
        
        // 写入测试数据
        try {
            writeTestData(filename);
            System.out.println("测试数据写入成功");
        } catch (IOException e) {
            System.err.println("写入文件失败: " + e.getMessage());
            return;
        }
        
        // 读取并处理文件
        try {
            processFileWithCheckedExceptions(filename);
        } catch (IOException e) {
            System.err.println("处理文件时发生IO异常: " + e.getMessage());
        }
        
        // 使用try-with-resources的现代方式
        try {
            processFileWithTryWithResources(filename);
        } catch (IOException e) {
            System.err.println("使用try-with-resources处理文件失败: " + e.getMessage());
        }
        
        // 清理测试文件
        cleanupTestFile(filename);
    }
    
    /**
     * 写入测试数据到文件（受检异常）
     */
    public static void writeTestData(String filename) throws IOException {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            writer.println("10");
            writer.println("20");
            writer.println("abc"); // 这行会导致NumberFormatException
            writer.println("30");
        }
    }
    
    /**
     * 使用传统try-catch-finally处理文件（受检异常）
     */
    public static void processFileWithCheckedExceptions(String filename) throws IOException {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(filename));
            String line;
            int lineNumber = 0;
            
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                try {
                    int number = Integer.parseInt(line.trim());
                    System.out.println("第" + lineNumber + "行: " + number + " (有效数字)");
                } catch (NumberFormatException e) {
                    // 非受检异常：处理无效数字
                    System.out.println("第" + lineNumber + "行: '" + line + "' (无效数字，跳过)");
                }
            }
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    System.err.println("关闭文件读取器失败: " + e.getMessage());
                }
            }
        }
    }
    
    /**
     * 使用try-with-resources处理文件（Java 7+推荐方式）
     */
    public static void processFileWithTryWithResources(String filename) throws IOException {
        try (BufferedReader reader = Files.newBufferedReader(Paths.get(filename))) {
            String line;
            int lineNumber = 0;
            
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                try {
                    double number = Double.parseDouble(line.trim());
                    System.out.println("第" + lineNumber + "行: " + number + " (有效数字)");
                } catch (NumberFormatException e) {
                    // 非受检异常：处理无效数字
                    System.out.println("第" + lineNumber + "行: '" + line + "' (无效数字，跳过)");
                }
            }
        }
        // try-with-resources自动关闭资源，无需finally块
    }
    
    /**
     * 清理测试文件（非受检异常处理）
     */
    public static void cleanupTestFile(String filename) {
        try {
            Files.deleteIfExists(Paths.get(filename));
            System.out.println("测试文件已清理");
        } catch (IOException e) {
            // 虽然Files.deleteIfExists通常不会抛出异常，
            // 但为了演示，我们仍然处理可能的IOException
            System.err.println("清理测试文件失败: " + e.getMessage());
        }
    }
}
