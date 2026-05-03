public class Solution03 {
    public static void main(String[] args) {
        // 命令行参数读取演示
        System.out.println("命令行参数演示程序");
        System.out.println("==================");

        // 检查是否有命令行参数
        if (args.length == 0) {
            System.out.println("没有提供命令行参数。");
            System.out.println("用法: java Solution03 [参数1] [参数2] ...");
            return;
        }

        // 输出参数个数
        System.out.println("接收到 " + args.length + " 个参数:");

        // 遍历并输出所有参数
        for (int i = 0; i < args.length; i++) {
            System.out.println("参数[" + i + "]: " + args[i]);
        }

        // 演示参数的实际应用
        System.out.println("\n实际应用示例:");
        if (args.length >= 2) {
            try {
                double num1 = Double.parseDouble(args[0]);
                double num2 = Double.parseDouble(args[1]);
                System.out.println("数字计算: " + num1 + " + " + num2 + " = " + (num1 + num2));
            } catch (NumberFormatException e) {
                System.out.println("前两个参数不是有效的数字，无法进行计算。");
            }
        }

        // 演示字符串拼接
        StringBuilder message = new StringBuilder();
        for (String arg : args) {
            message.append(arg).append(" ");
        }
        System.out.println("\n拼接消息: \"" + message.toString().trim() + "\"");
    }
}