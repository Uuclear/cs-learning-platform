# 挑战 1：实现泛型二叉搜索树

## 背景
二叉搜索树（BST）是一种重要的数据结构，它允许高效的查找、插入和删除操作。现在你需要实现一个**泛型**的二叉搜索树，能够处理任何实现了 `Comparable` 接口的类型。

## 要求

### 基本功能
实现 `GenericBST<T extends Comparable<T>>` 类，包含以下方法：

1. **构造函数**: `GenericBST()`
2. **插入**: `void insert(T value)` - 插入一个值到树中
3. **查找**: `boolean contains(T value)` - 检查树中是否包含指定值
4. **中序遍历**: `List<T> inOrderTraversal()` - 返回中序遍历的结果（应该是一个排序后的列表）

### 高级功能（可选）
5. **删除**: `void delete(T value)` - 从树中删除指定值
6. **高度**: `int getHeight()` - 返回树的高度
7. **是否平衡**: `boolean isBalanced()` - 检查树是否平衡

## 提示

- 使用内部类 `Node` 来表示树节点
- 利用 `T` 的 `compareTo()` 方法进行比较
- 注意处理重复值的情况（可以选择忽略或覆盖）
- 中序遍历应该返回一个排序后的列表

## 测试用例

```java
// 测试整数 BST
GenericBST<Integer> intTree = new GenericBST<>();
intTree.insert(5);
intTree.insert(3);
intTree.insert(7);
intTree.insert(1);
intTree.insert(9);

System.out.println("Contains 3: " + intTree.contains(3)); // true
System.out.println("Contains 4: " + intTree.contains(4)); // false
System.out.println("In-order: " + intTree.inOrderTraversal()); // [1, 3, 5, 7, 9]

// 测试字符串 BST
GenericBST<String> stringTree = new GenericBST<>();
stringTree.insert("banana");
stringTree.insert("apple");
stringTree.insert("cherry");

System.out.println("String in-order: " + stringTree.inOrderTraversal()); // [apple, banana, cherry]
```

## 评估标准

- **正确性**: 所有基本功能必须正确实现
- **泛型使用**: 正确使用泛型约束 `<T extends Comparable<T>>`
- **代码质量**: 代码清晰、注释完整、异常处理得当
- **性能**: 时间复杂度符合 BST 的预期（平均 O(log n)，最坏 O(n)）

## 扩展思考

1. 如何修改这个实现来支持自定义比较器（Comparator）？
2. 如果要支持重复值，应该如何设计？
3. 如何将这个 BST 转换为自平衡树（如 AVL 树）？