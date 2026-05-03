# 挑战 1：实现自定义排序 trait

## 背景
在实际开发中，我们经常需要对不同类型的数据进行排序。Rust 的标准库提供了 `Ord` 和 `PartialOrd` trait 来支持排序，但有时我们需要自定义的排序逻辑。

## 任务要求
1. 定义一个名为 `Sortable` 的 trait，包含以下方法：
   - `fn compare(&self, other: &Self) -> std::cmp::Ordering`
   - `fn is_less_than(&self, other: &Self) -> bool`（提供默认实现）

2. 创建一个 `Student` 结构体，包含字段：
   - `name: String`
   - `age: u32`
   - `grade: f64`（成绩）

3. 为 `Student` 实现 `Sortable` trait，按以下优先级排序：
   - 首先按成绩降序排列（成绩高的在前）
   - 成绩相同时按年龄升序排列（年龄小的在前）
   - 年龄也相同时按姓名字母顺序排列

4. 实现一个泛型函数 `sort_students<T: Sortable + Clone>`，接收 `Vec<T>` 并返回排序后的向量。

5. 在 `main` 函数中创建至少 5 个不同的学生实例，使用你的排序函数进行排序并打印结果。

## 提示
- 使用 `std::cmp::Ordering::{Less, Equal, Greater}`
- 可以使用元组比较来简化多字段排序逻辑
- 考虑为 `Student` 实现 `Debug` trait 以便打印

## 扩展挑战（可选）
- 实现另一个排序策略：按年龄升序，然后按成绩降序
- 使用 trait 对象创建可以动态选择排序策略的系统