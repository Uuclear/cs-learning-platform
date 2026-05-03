package examples;

import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.Stream;

/**
 * 示例2: Stream filter/map/collect 链式操作
 * 演示 Stream API 的核心操作和链式调用
 */
public class Example02 {
    // 辅助类：学生
    static class Student {
        private String name;
        private int age;
        private double score;
        private String major;

        public Student(String name, int age, double score, String major) {
            this.name = name;
            this.age = age;
            this.score = score;
            this.major = major;
        }

        // Getters
        public String getName() { return name; }
        public int getAge() { return age; }
        public double getScore() { return score; }
        public String getMajor() { return major; }

        @Override
        public String toString() {
            return String.format("Student{name='%s', age=%d, score=%.1f, major='%s'}",
                               name, age, score, major);
        }
    }

    public static void main(String[] args) {
        List<Student> students = Arrays.asList(
            new Student("Alice", 20, 85.5, "Computer Science"),
            new Student("Bob", 19, 78.0, "Mathematics"),
            new Student("Charlie", 21, 92.5, "Computer Science"),
            new Student("Diana", 20, 88.0, "Physics"),
            new Student("Eve", 22, 95.0, "Computer Science"),
            new Student("Frank", 18, 72.5, "Mathematics")
        );

        System.out.println("=== 原始学生列表 ===");
        students.forEach(System.out::println);

        // 1. 基本过滤和映射
        System.out.println("\n=== 1. 找出计算机专业的学生姓名 ===");
        List<String> csNames = students.stream()
            .filter(student -> "Computer Science".equals(student.getMajor()))
            .map(Student::getName)
            .collect(Collectors.toList());
        csNames.forEach(System.out::println);

        // 2. 复杂条件过滤
        System.out.println("\n=== 2. 找出年龄>=20且分数>85的学生 ===");
        students.stream()
            .filter(student -> student.getAge() >= 20 && student.getScore() > 85)
            .forEach(System.out::println);

        // 3. 排序和限制
        System.out.println("\n=== 3. 分数最高的前3名学生 ===");
        students.stream()
            .sorted(Comparator.comparing(Student::getScore).reversed())
            .limit(3)
            .forEach(System.out::println);

        // 4. 去重操作
        System.out.println("\n=== 4. 所有专业（去重） ===");
        List<String> majors = students.stream()
            .map(Student::getMajor)
            .distinct()
            .collect(Collectors.toList());
        majors.forEach(System.out::println);

        // 5. 数值流操作
        System.out.println("\n=== 5. 统计信息 ===");
        DoubleSummaryStatistics stats = students.stream()
            .mapToDouble(Student::getScore)
            .summaryStatistics();

        System.out.printf("平均分: %.2f%n", stats.getAverage());
        System.out.printf("最高分: %.1f%n", stats.getMax());
        System.out.printf("最低分: %.1f%n", stats.getMin());
        System.out.printf("总人数: %d%n", stats.getCount());

        // 6. 条件检查
        System.out.println("\n=== 6. 条件检查 ===");
        boolean hasPerfectScore = students.stream()
            .anyMatch(student -> student.getScore() == 100.0);
        System.out.println("是否有满分学生: " + hasPerfectScore);

        boolean allAdults = students.stream()
            .allMatch(student -> student.getAge() >= 18);
        System.out.println("是否都是成年人: " + allAdults);

        boolean noSeniors = students.stream()
            .noneMatch(student -> student.getAge() >= 25);
        System.out.println("是否没有高年级学生(>=25): " + noSeniors);

        // 7. 查找操作
        System.out.println("\n=== 7. 查找操作 ===");
        Optional<Student> firstCsStudent = students.stream()
            .filter(student -> "Computer Science".equals(student.getMajor()))
            .findFirst();

        if (firstCsStudent.isPresent()) {
            System.out.println("第一个计算机专业学生: " + firstCsStudent.get());
        }

        // 8. 归约操作
        System.out.println("\n=== 8. 归约操作 ===");
        Optional<Double> totalScore = students.stream()
            .map(Student::getScore)
            .reduce(Double::sum);

        totalScore.ifPresent(score -> System.out.printf("总分: %.1f%n", score));

        // 使用初始值的归约
        double totalScoreWithInitial = students.stream()
            .map(Student::getScore)
            .reduce(0.0, Double::sum);
        System.out.printf("总分(带初始值): %.1f%n", totalScoreWithInitial);
    }
}