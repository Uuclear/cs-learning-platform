import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

/**
 * 解决方案2: 日志文件分析
 * 读取日志文件，统计各错误级别的数量，并生成报告
 */
public class Solution02 {
    public static void main(String[] args) {
        Path logPath = Paths.get("application.log");
        Path reportPath = Paths.get("log_report.txt");

        // 创建模拟日志文件
        createSampleLogFile(logPath);

        // 分析日志文件
        Map<String, Integer> logStats = analyzeLogFile(logPath);

        // 生成报告
        generateReport(reportPath, logStats);
    }

    private static void createSampleLogFile(Path logPath) {
        try {
            String logContent = "2026-05-03 10:00:00 INFO  Application started\n" +
                              "2026-05-03 10:01:15 WARN  Low memory warning\n" +
                              "2026-05-03 10:02:30 ERROR Database connection failed\n" +
                              "2026-05-03 10:03:45 INFO  Retry database connection\n" +
                              "2026-05-03 10:04:20 ERROR Authentication failed\n" +
                              "2026-05-03 10:05:10 WARN  High CPU usage detected\n" +
                              "2026-05-03 10:06:00 INFO  System recovered";
            Files.writeString(logPath, logContent, StandardCharsets.UTF_8);
            System.out.println("✅ 创建模拟日志文件成功！");
        } catch (IOException e) {
            System.err.println("创建日志文件失败: " + e.getMessage());
        }
    }

    private static Map<String, Integer> analyzeLogFile(Path logPath) {
        Map<String, Integer> stats = new HashMap<>();
        stats.put("INFO", 0);
        stats.put("WARN", 0);
        stats.put("ERROR", 0);

        try {
            Files.lines(logPath, StandardCharsets.UTF_8)
                 .forEach(line -> {
                     if (line.contains("INFO")) stats.put("INFO", stats.get("INFO") + 1);
                     if (line.contains("WARN")) stats.put("WARN", stats.get("WARN") + 1);
                     if (line.contains("ERROR")) stats.put("ERROR", stats.get("ERROR") + 1);
                 });

            System.out.println("🔍 日志分析完成:");
            stats.forEach((level, count) ->
                System.out.println(level + " 级别日志: " + count + " 条"));

        } catch (IOException e) {
            System.err.println("分析日志文件失败: " + e.getMessage());
        }

        return stats;
    }

    private static void generateReport(Path reportPath, Map<String, Integer> stats) {
        try {
            StringBuilder report = new StringBuilder();
            report.append("=== 日志分析报告 ===\n");
            report.append("生成时间: ").append(java.time.LocalDateTime.now()).append("\n\n");
            report.append("统计结果:\n");
            stats.forEach((level, count) ->
                report.append("- ").append(level).append(": ").append(count).append(" 条\n"));

            Files.writeString(reportPath, report.toString(), StandardCharsets.UTF_8);
            System.out.println("✅ 日志分析报告已生成: " + reportPath);
        } catch (IOException e) {
            System.err.println("生成报告失败: " + e.getMessage());
        }
    }
}