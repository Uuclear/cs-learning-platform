import java.util.*;

/**
 * Example02: 通配符 ? extends/? super 对比
 */
public class Example02 {

    /**
     * Producer Extends: 从列表中读取数据（生产者）
     * 使用 ? extends Number 可以接受 List<Integer>, List<Double> 等
     */
    public static double sumOfList(List<? extends Number> list) {
        double sum = 0.0;
        for (Number num : list) {
            sum += num.doubleValue();
        }
        return sum;
    }

    /**
     * Consumer Super: 向列表中写入数据（消费者）
     * 使用 ? super Integer 可以接受 List<Integer>, List<Number>, List<Object>
     */
    public static void addNumbers(List<? super Integer> list) {
        for (int i = 1; i <= 5; i++) {
            list.add(i);
        }
    }

    /**
     * 错误示例：尝试向 ? extends 列表中添加元素
     */
    public static void tryToAddToExtendsList(List<? extends Number> list) {
        // 这行代码会导致编译错误！
        // list.add(10); // 编译错误：不能确定具体类型

        // 但是可以添加 null
        list.add(null);

        // 可以安全地读取
        Number first = list.get(0);
        System.out.println("First element: " + first);
    }

    /**
     * 错误示例：尝试从 ? super 列表中获取具体类型
     */
    public static void tryToGetFromSuperList(List<? super Integer> list) {
        // 这行代码只能返回 Object 类型
        Object obj = list.get(0); // 只能是 Object

        // 不能直接赋值给 Integer
        // Integer num = list.get(0); // 编译错误

        System.out.println("Object from super list: " + obj);
    }

    public static void main(String[] args) {
        System.out.println("=== Producer Extends 示例 ===");
        List<Integer> integers = Arrays.asList(1, 2, 3, 4, 5);
        List<Double> doubles = Arrays.asList(1.5, 2.5, 3.5);

        double sumInts = sumOfList(integers);
        double sumDoubles = sumOfList(doubles);

        System.out.println("Integer list sum: " + sumInts);
        System.out.println("Double list sum: " + sumDoubles);

        System.out.println("\n=== Consumer Super 示例 ===");
        List<Integer> intList = new ArrayList<>();
        List<Number> numList = new ArrayList<>();
        List<Object> objList = new ArrayList<>();

        addNumbers(intList);
        addNumbers(numList);
        addNumbers(objList);

        System.out.println("Integer list after adding: " + intList);
        System.out.println("Number list after adding: " + numList);
        System.out.println("Object list after adding: " + objList);

        System.out.println("\n=== 错误示例演示 ===");
        tryToAddToExtendsList(integers);
        tryToGetFromSuperList(intList);
    }
}