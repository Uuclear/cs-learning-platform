import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;
import java.nio.charset.StandardCharsets;

/**
 * 示例1: 文件读写（Files.readString/writeString 现代方式）
 * 演示Java 11+中最新的文件读写API
 */
public class Example01 {
    public static void main(String[] args) {
        Path filePath = Paths.get("example01_output.txt");

        // 写入文件 - 超级简单！
        try {
            Files.writeString(filePath, "Hello, Java I/O!\n这是第二行内容。", StandardCharsets.UTF_8);
            System.out.println("✅ 文件写入成功！");
        } catch (IOException e) {
            System.err.println("❌ 写入文件失败: " + e.getMessage());
            return;
        }

        // 读取文件 - 同样简单！
        try {
            String content = Files.readString(filePath, StandardCharsets.UTF_8);
            System.out.println("📄 文件内容:");
            System.out.println(content);
        } catch (IOException e) {
            System.err.println("❌ 读取文件失败: " + e.getMessage());
        }
    }
}