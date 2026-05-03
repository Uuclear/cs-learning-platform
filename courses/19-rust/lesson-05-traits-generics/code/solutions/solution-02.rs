// solution-02.rs - 泛型函数和结构体（完整解决方案）
// 扩展的 Pair<T> 实现和更多泛型示例

use std::ops::{Add, Mul, Div, Sub};

// 基础 Pair 结构体
#[derive(Debug, Clone)]
struct Pair<T> {
    first: T,
    second: T,
}

impl<T> Pair<T> {
    fn new(first: T, second: T) -> Self {
        Pair { first, second }
    }

    fn first(&self) -> &T {
        &self.first
    }

    fn second(&self) -> &T {
        &self.second
    }

    fn into_tuple(self) -> (T, T) {
        (self.first, self.second)
    }
}

// 当 T 支持比较操作时
impl<T: PartialOrd> Pair<T> {
    fn max(&self) -> &T {
        if self.first >= self.second {
            &self.first
        } else {
            &self.second
        }
    }

    fn min(&self) -> &T {
        if self.first <= self.second {
            &self.first
        } else {
            &self.second
        }
    }

    fn is_ordered(&self) -> bool {
        self.first <= self.second
    }
}

// 当 T 支持算术操作时
impl<T: Add<Output = T> + Copy> Pair<T> {
    fn sum(&self) -> T {
        self.first + self.second
    }
}

impl<T: Mul<Output = T> + Copy> Pair<T> {
    fn product(&self) -> T {
        self.first * self.second
    }
}

impl<T: Add<Output = T> + Div<Output = T> + Copy + From<u8>> Pair<T> {
    fn average(&self) -> T {
        (self.first + self.second) / T::from(2u8)
    }
}

// 泛型函数集合
fn swap<T>(a: T, b: T) -> (T, T) {
    (b, a)
}

fn duplicate<T: Clone>(value: T) -> (T, T) {
    (value.clone(), value)
}

fn print_debug<T: std::fmt::Debug>(item: T) {
    println!("{:?}", item);
}

// 更复杂的泛型函数：处理可迭代的泛型容器
fn process_collection<T, I>(collection: I) -> Vec<T>
where
    I: IntoIterator<Item = T>,
{
    collection.into_iter().collect()
}

// 使用 where 子句的复杂约束
fn calculate_stats<T>(values: &[T]) -> Option<(T, T, T)>
where
    T: Copy + PartialOrd + Add<Output = T> + Div<Output = T> + From<u8>,
{
    if values.is_empty() {
        return None;
    }

    let mut min = values[0];
    let mut max = values[0];
    let mut sum = values[0];

    for &value in &values[1..] {
        if value < min {
            min = value;
        }
        if value > max {
            max = value;
        }
        sum = sum + value;
    }

    let avg = sum / T::from(values.len() as u8);
    Some((min, max, avg))
}

fn main() {
    println!("=== 基础 Pair 操作 ===");
    let int_pair = Pair::new(10, 25);
    println!("整数对: {:?}", int_pair);
    println!("最大值: {}, 最小值: {}", int_pair.max(), int_pair.min());
    println!("和: {}, 积: {}, 平均值: {:.1}",
             int_pair.sum(), int_pair.product(), int_pair.average());

    let float_pair = Pair::new(3.5, 7.2);
    println!("\n浮点数对: {:?}", float_pair);
    println!("最大值: {:.1}, 最小值: {:.1}", float_pair.max(), float_pair.min());
    println!("和: {:.1}, 积: {:.1}, 平均值: {:.1}",
             float_pair.sum(), float_pair.product(), float_pair.average());

    println!("\n=== 泛型函数 ===");
    let (x, y) = swap("Hello", "World");
    println!("交换: {} {}", x, y);

    let (a, b) = duplicate(42);
    println!("复制: {} {}", a, b);

    println!("\n=== 集合处理 ===");
    let numbers = vec![1, 2, 3, 4, 5];
    let processed: Vec<i32> = process_collection(numbers.iter().map(|x| x * 2));
    println!("处理后的数字: {:?}", processed);

    println!("\n=== 统计计算 ===");
    let stats_data = vec![10, 20, 30, 40, 50];
    if let Some((min, max, avg)) = calculate_stats(&stats_data) {
        println!("最小值: {}, 最大值: {}, 平均值: {}", min, max, avg);
    }

    let float_data = vec![1.5, 2.5, 3.5, 4.5];
    if let Some((min, max, avg)) = calculate_stats(&float_data) {
        println!("浮点数 - 最小值: {:.1}, 最大值: {:.1}, 平均值: {:.1}", min, max, avg);
    }
}