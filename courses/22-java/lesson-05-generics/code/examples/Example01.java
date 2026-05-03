/**
 * Example01: 泛型类 Pair<T, U> 和泛型方法
 */
public class Example01 {
    /**
     * 泛型类：键值对
     */
    public static class Pair<T, U> {
        private T first;
        private U second;

        public Pair(T first, U second) {
            this.first = first;
            this.second = second;
        }

        public T getFirst() { return first; }
        public U getSecond() { return second; }

        public void setFirst(T first) { this.first = first; }
        public void setSecond(U second) { this.second = second; }

        @Override
        public String toString() {
            return "(" + first + ", " + second + ")";
        }
    }

    /**
     * 静态泛型方法：打印数组
     */
    public static <T> void printArray(T[] array) {
        System.out.print("[");
        for (int i = 0; i < array.length; i++) {
            if (i > 0) System.out.print(", ");
            System.out.print(array[i]);
        }
        System.out.println("]");
    }

    /**
     * 实例泛型方法：找到两个可比较对象中的最大值
     */
    public <T extends Comparable<T>> T findMax(T a, T b) {
        return a.compareTo(b) > 0 ? a : b;
    }

    public static void main(String[] args) {
        // 使用泛型类
        Pair<String, Integer> nameAge = new Pair<>("张三", 25);
        Pair<Double, Boolean> priceAvailable = new Pair<>(99.99, true);

        System.out.println("Name-Age pair: " + nameAge);
        System.out.println("Price-Available pair: " + priceAvailable);

        // 使用泛型方法
        String[] names = {"Alice", "Bob", "Charlie"};
        System.out.print("Names array: ");
        printArray(names);

        Integer[] numbers = {10, 20, 30};
        System.out.print("Numbers array: ");
        printArray(numbers);

        // 使用实例泛型方法
        Example01 example = new Example01();
        Integer maxInt = example.findMax(15, 25);
        String maxStr = example.findMax("apple", "banana");

        System.out.println("Max of 15 and 25: " + maxInt);
        System.out.println("Max of 'apple' and 'banana': " + maxStr);
    }
}