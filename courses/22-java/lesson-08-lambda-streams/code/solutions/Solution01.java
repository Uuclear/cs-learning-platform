package solutions;

import java.util.Arrays;
import java.util.List;
import java.util.function.Consumer;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * 解决方案1: Lambda 表达式与函数式接口
 * 这是 Example01.java 的完整解决方案，包含所有练习的答案
 */
public class Solution01 {
    public static void main(String[] args) {
        // 1. 基本 Lambda 表达式语法
        System.out.println("=== 1. Lambda 表达式基本语法 ===");

        // 无参数 Lambda
        Runnable runnable = () -> System.out.println("Hello from Lambda!");
        runnable.run();

        // 单参数 Lambda
        Consumer<String> printer = s -> System.out.println("Printing: " + s);
        printer.accept("Single parameter");

        // 多参数 Lambda
        Function<Integer, Integer> doubler = x -> x * 2;
        System.out.println("Double of 5: " + doubler.apply(5));

        // 多行 Lambda
        Predicate<Integer> isEvenAndPositive = n -> {
            System.out.println("Checking number: " + n);
            return n > 0 && n % 2 == 0;
        };
        System.out.println("Is 4 even and positive? " + isEvenAndPositive.test(4));
        System.out.println("Is -2 even and positive? " + isEvenAndPositive.test(-2));

        // 2. 方法引用
        System.out.println("\n=== 2. 方法引用 ===");
        List<String> names = Arrays.asList("Alice", "Bob", "Charlie", "Diana");

        // 对象方法引用
        names.forEach(System.out::println);

        // 静态方法引用
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
        numbers.stream()
               .map(Math::abs)
               .forEach(n -> System.out.print(n + " "));
        System.out.println();

        // 构造器引用
        Function<String, StringBuilder> builderFactory = StringBuilder::new;
        StringBuilder sb = builderFactory.apply("Hello");
        System.out.println("StringBuilder content: " + sb.toString());

        // 3. 函数式接口组合
        System.out.println("\n=== 3. 函数式接口组合 ===");
        Predicate<String> isEmpty = String::isEmpty;
        Predicate<String> isBlank = s -> s.trim().isEmpty();

        // 使用 and, or, negate 组合谓词
        Predicate<String> isNotEmptyAndNotBlank = isEmpty.negate().and(isBlank.negate());

        System.out.println("Test '': " + isNotEmptyAndNotBlank.test(""));
        System.out.println("Test '   ': " + isNotEmptyAndNotBlank.test("   "));
        System.out.println("Test 'Hello': " + isNotEmptyAndNotBlank.test("Hello"));

        // 函数组合
        Function<Integer, Integer> addOne = x -> x + 1;
        Function<Integer, Integer> multiplyByTwo = x -> x * 2;

        // 先加1再乘2: f(g(x))
        Function<Integer, Integer> composed = multiplyByTwo.compose(addOne);
        System.out.println("Composed (5): " + composed.apply(5)); // (5+1)*2 = 12

        // 先乘2再加1: g(f(x))
        Function<Integer, Integer> andThen = addOne.andThen(multiplyByTwo);
        System.out.println("AndThen (5): " + andThen.apply(5)); // (5*2)+1 = 11

        // 额外练习：创建一个复合谓词来检查字符串是否长度在5-10之间且不为空
        Predicate<String> lengthBetween5And10 = s -> s.length() >= 5 && s.length() <= 10;
        Predicate<String> validString = isNotEmptyAndNotBlank.and(lengthBetween5And10);

        System.out.println("\n=== 额外练习：复合谓词 ===");
        System.out.println("Test 'Hi': " + validString.test("Hi"));           // false (too short)
        System.out.println("Test 'Hello World': " + validString.test("Hello World")); // false (too long)
        System.out.println("Test 'Hello': " + validString.test("Hello"));     // true (perfect)
    }
}