public class Solution02 {
    public static void main(String[] args) {
        // 基本数据类型演示
        int age = 25;                    // 整数类型
        double height = 175.5;           // 浮点类型
        char grade = 'A';                // 字符类型
        boolean isStudent = true;        // 布尔类型
        String name = "张三";            // 字符串类型（注意：String 是引用类型）

        // 输出各种数据类型
        System.out.println("姓名: " + name);
        System.out.println("年龄: " + age + " 岁");
        System.out.println("身高: " + height + " cm");
        System.out.println("成绩等级: " + grade);
        System.out.println("是否是学生: " + isStudent);

        // 演示基本运算
        int a = 10, b = 3;
        System.out.println("\n基本运算演示:");
        System.out.println(a + " + " + b + " = " + (a + b));
        System.out.println(a + " - " + b + " = " + (a - b));
        System.out.println(a + " * " + b + " = " + (a * b));
        System.out.println(a + " / " + b + " = " + (a / b)); // 整数除法
        System.out.println(a + " % " + b + " = " + (a % b)); // 取余运算
    }
}