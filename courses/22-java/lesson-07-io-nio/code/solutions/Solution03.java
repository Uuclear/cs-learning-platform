import java.io.IOException;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.nio.file.Files;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

/**
 * 解决方案3: 高效文件备份
 * 使用NIO的FileChannel进行高效复制，并添加时间戳到备份文件名
 */
public class Solution03 {
    public static void main(String[] args) {
        Path originalFile = Paths.get("important_data.txt");

        // 创建原始文件
        createOriginalFile(originalFile);

        // 执行备份
        backupFile(originalFile);
    }

    private static void createOriginalFile(Path filePath) {
        try {
            String content = "这是重要的数据文件。\n" +
                           "包含需要定期备份的关键信息。\n" +
                           "使用NIO可以高效地完成备份任务！";
            Files.writeString(filePath, content);
            System.out.println("✅ 创建原始文件成功: " + filePath);
        } catch (IOException e) {
            System.err.println("创建原始文件失败: " + e.getMessage());
        }
    }

    private static void backupFile(Path originalFile) {
        if (!Files.exists(originalFile)) {
            System.err.println("❌ 原始文件不存在: " + originalFile);
            return;
        }

        // 生成带时间戳的备份文件名
        String timestamp = LocalDateTime.now()
            .format(DateTimeFormatter.ofPattern("yyyyMMdd_HHmmss"));
        String backupFileName = originalFile.getFileName().toString()
            .replaceFirst("\\.([^.]+)$", "_backup_" + timestamp + ".$1");
        Path backupFile = originalFile.getParent().resolve(backupFileName);

        // 使用FileChannel进行高效复制
        try (FileChannel sourceChannel = FileChannel.open(originalFile, StandardOpenOption.READ);
             FileChannel backupChannel = FileChannel.open(backupFile,
                 StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {

            long position = 0;
            long fileSize = sourceChannel.size();

            while (position < fileSize) {
                position += sourceChannel.transferTo(position, fileSize - position, backupChannel);
            }

            System.out.println("✅ 备份完成!");
            System.out.println("原始文件: " + originalFile);
            System.out.println("备份文件: " + backupFile);

            // 验证备份文件大小
            long originalSize = Files.size(originalFile);
            long backupSize = Files.size(backupFile);
            if (originalSize == backupSize) {
                System.out.println("✅ 备份验证通过 - 文件大小一致");
            } else {
                System.out.println("⚠️  备份验证失败 - 文件大小不一致");
            }

        } catch (IOException e) {
            System.err.println("❌ 备份失败: " + e.getMessage());
        }
    }
}