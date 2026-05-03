import java.io.IOException;
import java.nio.ByteBuffer;
import java.nio.channels.FileChannel;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;
import java.nio.file.Files;

/**
 * 示例3: NIO FileChannel 文件复制
 * 演示使用NIO的FileChannel进行高效文件复制
 */
public class Example03 {
    public static void main(String[] args) {
        Path sourcePath = Paths.get("example03_source.txt");
        Path targetPath = Paths.get("example03_target.txt");

        // 创建源文件
        try {
            String sourceContent = "这是源文件的内容。\n" +
                                 "包含多行文本用于演示NIO文件复制。\n" +
                                 "NIO的FileChannel提供了高效的文件传输能力！";
            Files.writeString(sourcePath, sourceContent);
            System.out.println("✅ 创建源文件成功！");
        } catch (IOException e) {
            System.err.println("❌ 创建源文件失败: " + e.getMessage());
            return;
        }

        // 方法1: 使用transferTo()进行高效复制（推荐）
        copyFileWithTransfer(sourcePath, targetPath);

        // 验证复制结果
        try {
            String copiedContent = Files.readString(targetPath);
            System.out.println("\n📄 复制后的文件内容:");
            System.out.println(copiedContent);
        } catch (IOException e) {
            System.err.println("❌ 读取复制文件失败: " + e.getMessage());
        }
    }

    /**
     * 使用FileChannel.transferTo()进行高效文件复制
     */
    private static void copyFileWithTransfer(Path source, Path target) {
        try (FileChannel inputChannel = FileChannel.open(source, StandardOpenOption.READ);
             FileChannel outputChannel = FileChannel.open(target, StandardOpenOption.CREATE, StandardOpenOption.WRITE)) {

            // transferTo()方法可以实现零拷贝，性能极高
            long position = 0;
            long count = inputChannel.size();

            while (position < count) {
                position += inputChannel.transferTo(position, count - position, outputChannel);
            }

            System.out.println("✅ 使用FileChannel.transferTo()复制文件成功！");

        } catch (IOException e) {
            System.err.println("❌ 使用transferTo()复制文件失败: " + e.getMessage());
        }
    }
}