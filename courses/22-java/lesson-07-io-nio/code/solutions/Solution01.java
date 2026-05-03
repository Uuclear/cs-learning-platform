import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * 解决方案1: 文件内容统计
 * 统计文件的总行数、单词数和字符数
 */
public class Solution01 {
    public static void main(String[] args) {
        Path inputPath = Paths.get("input.txt");

        // 创建测试文件
        createTestFile(inputPath);

        try {
            // 读取文件内容
            String content = Files.readString(inputPath, StandardCharsets.UTF_8);

            // 统计字符数（包括空格和换行符）
            long charCount = content.length();

            // 统计行数
            long lineCount = content.lines().count();

            // 统计单词数
            long wordCount = content.trim().isEmpty() ? 0 :
                           content.trim().split("\\s+").length;

            System.out.println("📊 文件统计结果:");
            System.out.println("字符数: " + charCount);
            System.out.println("行数: " + lineCount);
            System.out.println("单词数: " + wordCount);

        } catch (IOException e) {
            System.err.println("处理文件失败: " + e.getMessage());
        }
    }

    private static void createTestFile(Path path) {
        try {
            String testContent = "这是第一行文本。\n" +
                               "这是第二行，包含多个单词。\n" +
                               "第三行结束。";
            Files.writeString(path, testContent, StandardCharsets.UTF_8);
            System.out.println("✅ 创建测试文件成功！");
        } catch (IOException e) {
            System.err.println("创建测试文件失败: " + e.getMessage());
        }
    }
}