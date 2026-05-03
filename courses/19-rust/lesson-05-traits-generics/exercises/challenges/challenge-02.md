# 挑战 2：构建通用的数学运算库

## 背景
在科学计算和数据处理中，我们经常需要对不同类型的数值进行相同的数学运算。使用 Rust 的 trait 和泛型可以创建一个类型安全且高效的通用数学库。

## 任务要求
1. 定义以下 traits：
   - `Addable`: 支持加法运算，包含 `add` 方法
   - `Multipliable`: 支持乘法运算，包含 `multiply` 方法  
   - `Calculable`: 继承 `Addable` 和 `Multipliable`，并添加 `power` 方法（计算 x^n）

2. 为标准数值类型（`i32`, `f64`）实现这些 traits。

3. 创建一个泛型结构体 `Matrix<T>` 表示二维矩阵，要求 `T` 实现 `Calculable + Clone + Default`。

4. 为 `Matrix<T>` 实现以下方法：
   - `new(rows: usize, cols: usize) -> Self`
   - `set(&mut self, row: usize, col: usize, value: T)`
   - `get(&self, row: usize, col: usize) -> Option<&T>`
   - `add(&self, other: &Matrix<T>) -> Option<Matrix<T>>`（矩阵加法）
   - `multiply_scalar(&self, scalar: T) -> Matrix<T>`（标量乘法）

5. 实现一个泛型函数 `dot_product<T: Calculable + Clone>(a: &[T], b: &[T]) -> Option<T>` 计算两个向量的点积。

6. 在 `main` 函数中演示：
   - 使用整数和浮点数的点积计算
   - 创建和操作矩阵
   - 展示类型安全如何防止不同类型的操作

## 提示
- 使用 `std::ops` 中的标准 trait（如 `Add`, `Mul`）作为参考
- 考虑错误处理：维度不匹配时返回 `None`
- 使用 `derive` 宏为你的类型自动实现有用的 trait

## 扩展挑战（可选）
- 实现矩阵乘法
- 添加 `Display` trait 实现以便美观地打印矩阵
- 创建一个 trait 来支持不同的数值精度（单精度、双精度）