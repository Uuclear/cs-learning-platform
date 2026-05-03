import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.charset.StandardCharsets;

/**
 * 示例2: BufferedReader 逐行处理
 * 演示如何高效处理大文件，逐行读取避免内存溢出
 */
public class Example02 {
    public static void main(String[] args) {
        // 首先创建一个示例文件用于演示
        Path sampleFile = Paths.get("example02_sample.txt");
        try {
            String sampleContent = "第一行：普通信息\n" +
                                 "第二行：包含ERROR的错误信息\n" +
                                 "第三行：又是一条普通信息\n" +
                                 "第四行：另一个WARN警告信息\n" +
                                 "第五行：最后一条信息";
            Files.writeString(sampleFile, sampleContent, StandardCharsets.UTF_8);
            System.out.println("✅ 创建示例文件成功！");
        } catch (IOException e) {
            System.err.println("❌ 创建示例文件失败: " + e.getMessage());
            return;
        }

        // 使用BufferedReader逐行读取处理
        try (BufferedReader reader = new BufferedReader(new FileReader(sampleFile.toFile(), StandardCharsets.UTF_8))) {
            String line;
            int lineNumber = 0;
            int errorCount = 0;
            int warnCount = 0;

            System.out.println("\n🔍 开始逐行分析文件内容：");

            // 逐行读取
            while ((line = reader.readLine()) != null) {
                lineNumber++;
                System.out.println("第" + lineNumber + "行: " + line);

                // 分析日志级别
                if (line.contains("ERROR")) {
                    errorCount++;
                    System.out.println("   ⚠️  发现ERROR级别日志！");
                } else if (line.contains("WARN")) {
                    warnCount++;
                    System.out.println("   ⚠️  发现WARN级别日志！");
                }
            }

            System.out.println("\n📊 分析结果：");
            System.out.println("总行数: " + lineNumber);
            System.out.println("ERROR数量: " + errorCount);
            System.out.println("WARN数量: " + warnCount);

        } catch (IOException e) {
            System.err.println("❌ 读取文件失败: " + e.getMessage());
        }
    }
}