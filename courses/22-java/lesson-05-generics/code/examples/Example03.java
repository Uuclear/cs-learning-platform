import java.lang.reflect.ParameterizedType;
import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Example03: 类型擦除演示与 workaround
 * 演示 Java 泛型的类型擦除机制以及如何绕过限制
 */
public class Example03 {

    /**
     * 演示类型擦除：运行时无法获取泛型类型信息
     */
    public static void demonstrateTypeErasure() {
        System.out.println("=== 类型擦除演示 ===");

        List<String> stringList = new ArrayList<>();
        List<Integer> integerList = new ArrayList<>();

        // 运行时类型都是 ArrayList，泛型信息被擦除了
        System.out.println("String list class: " + stringList.getClass());
        System.out.println("Integer list class: " + integerList.getClass());
        System.out.println("Are they same class? " + (stringList.getClass() == integerList.getClass()));

        // 无法在运行时检查泛型类型
        // if (stringList instanceof List<String>) { } // 编译错误！
    }

    /**
     * Workaround 1: 传递 Class 对象来保留类型信息
     */
    public static class GenericClassWithClass<T> {
        private final Class<T> typeClass;
        private final List<T> items = new ArrayList<>();

        public GenericClassWithClass(Class<T> typeClass) {
            this.typeClass = typeClass;
        }

        public void addItem(T item) {
            items.add(item);
        }

        public Class<T> getTypeClass() {
            return typeClass;
        }

        public void printType() {
            System.out.println("Generic type: " + typeClass.getSimpleName());
        }
    }

    /**
     * Workaround 2: 使用匿名内部类配合反射获取泛型类型
     */
    public static abstract class TypeReference<T> {
        private final Type type;

        protected TypeReference() {
            Type superClass = getClass().getGenericSuperclass();
            if (superClass instanceof ParameterizedType) {
                this.type = ((ParameterizedType) superClass).getActualTypeArguments()[0];
            } else {
                throw new IllegalArgumentException("TypeReference constructed without actual type information");
            }
        }

        public Type getType() {
            return type;
        }
    }

    /**
     * Workaround 3: 类型安全的工厂方法避免重复类型声明
     */
    public static <T> List<T> createList() {
        return new ArrayList<T>();
    }

    /**
     * 演示泛型数组创建的问题和解决方案
     */
    public static <T> T[] createGenericArray(Class<T> type, int size) {
        // 不能直接创建泛型数组：T[] array = new T[size]; // 编译错误

        // 解决方案：使用反射
        @SuppressWarnings("unchecked")
        T[] array = (T[]) java.lang.reflect.Array.newInstance(type, size);
        return array;
    }

    public static void main(String[] args) {
        demonstrateTypeErasure();

        System.out.println("\n=== Workaround 1: 传递 Class 对象 ===");
        GenericClassWithClass<String> stringContainer = new GenericClassWithClass<>(String.class);
        stringContainer.printType();

        GenericClassWithClass<Integer> integerContainer = new GenericClassWithClass<>(Integer.class);
        integerContainer.printType();

        System.out.println("\n=== Workaround 2: 匿名内部类获取类型 ===");
        TypeReference<List<String>> stringListRef = new TypeReference<List<String>>() {};
        System.out.println("Type from reference: " + stringListRef.getType());

        System.out.println("\n=== Workaround 3: 工厂方法 ===");
        List<String> names = createList();
        names.add("Alice");
        names.add("Bob");
        System.out.println("Created list: " + names);

        System.out.println("\n=== 泛型数组创建 ===");
        String[] stringArray = createGenericArray(String.class, 3);
        stringArray[0] = "Hello";
        stringArray[1] = "World";
        stringArray[2] = "Java";
        System.out.println("Generic array: " + Arrays.toString(stringArray));
    }
}