import java.util.HashMap;
import java.util.Map;

/**
 * Solution01: 泛型缓存实现
 * 实现 GenericCache<K, V> 类，支持基本的 put/get 操作
 */
public class Solution01 {
    public static class GenericCache<K, V> {
        private final Map<K, V> cache = new HashMap<>();

        /**
         * 存储键值对
         */
        public void put(K key, V value) {
            cache.put(key, value);
        }

        /**
         * 获取值，如果不存在返回 null
         */
        public V get(K key) {
            return cache.get(key);
        }

        /**
         * 检查是否包含指定键
         */
        public boolean containsKey(K key) {
            return cache.containsKey(key);
        }

        /**
         * 获取缓存大小
         */
        public int size() {
            return cache.size();
        }

        /**
         * 清空缓存
         */
        public void clear() {
            cache.clear();
        }
    }

    public static void main(String[] args) {
        // 测试字符串缓存
        GenericCache<String, Integer> stringCache = new GenericCache<>();
        stringCache.put("age", 25);
        stringCache.put("score", 95);

        System.out.println("Age: " + stringCache.get("age"));
        System.out.println("Score: " + stringCache.get("score"));
        System.out.println("Contains 'name': " + stringCache.containsKey("name"));

        // 测试数字缓存
        GenericCache<Integer, String> numberCache = new GenericCache<>();
        numberCache.put(1, "One");
        numberCache.put(2, "Two");

        System.out.println("Number 1: " + numberCache.get(1));
        System.out.println("Cache size: " + numberCache.size());
    }
}