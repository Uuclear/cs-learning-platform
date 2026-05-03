import java.util.List;

/**
 * Solution02: 通配符应用
 * 实现 calculateAverage(List<? extends Number> numbers) 方法
 */
public class Solution02 {

    /**
     * 计算任意数值类型列表的平均值
     * @param numbers 包含 Number 或其子类型的列表
     * @return 平均值（double 类型）
     */
    public static double calculateAverage(List<? extends Number> numbers) {
        if (numbers == null || numbers.isEmpty()) {
            throw new IllegalArgumentException("List cannot be null or empty");
        }

        double sum = 0.0;
        for (Number num : numbers) {
            sum += num.doubleValue();
        }

        return sum / numbers.size();
    }

    public static void main(String[] args) {
        // 测试整数列表
        java.util.List<Integer> integers = java.util.Arrays.asList(1, 2, 3, 4, 5);
        double avgInts = calculateAverage(integers);
        System.out.println("Integer average: " + avgInts);

        // 测试双精度列表
        java.util.List<Double> doubles = java.util.Arrays.asList(1.5, 2.5, 3.5, 4.5);
        double avgDoubles = calculateAverage(doubles);
        System.out.println("Double average: " + avgDoubles);

        // 测试混合类型（通过 Number 列表）
        java.util.List<Number> mixed = java.util.Arrays.asList(10, 20.5, 30L, 40.0f);
        double avgMixed = calculateAverage(mixed);
        System.out.println("Mixed average: " + avgMixed);
    }
}