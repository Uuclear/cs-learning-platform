// example-02.rs - 泛型函数和结构体
// 演示 Pair<T> 泛型结构体和相关操作

// 定义泛型结构体 Pair
struct Pair<T> {
    first: T,
    second: T,
}

// 为 Pair<T> 实现方法
impl<T> Pair<T> {
    // 创建新的 Pair 实例
    fn new(first: T, second: T) -> Self {
        Pair { first, second }
    }

    // 获取第一个元素的引用
    fn first(&self) -> &T {
        &self.first
    }

    // 获取第二个元素的引用
    fn second(&self) -> &T {
        &self.second
    }
}

// 只有当 T 实现了 PartialOrd trait 时，才能比较大小
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
}

// 泛型函数：交换两个值
fn swap<T>(a: T, b: T) -> (T, T) {
    (b, a)
}

// 泛型函数：打印任意类型（需要实现 Debug trait）
fn print_anything<T: std::fmt::Debug>(value: T) {
    println!("{:?}", value);
}

fn main() {
    println!("=== 泛型结构体 Pair ===");

    // 创建整数对
    let int_pair = Pair::new(10, 20);
    println!("整数对: ({}, {})", int_pair.first(), int_pair.second());
    println!("最大值: {}, 最小值: {}", int_pair.max(), int_pair.min());

    // 创建浮点数对
    let float_pair = Pair::new(3.14, 2.71);
    println!("浮点数对: ({:.2}, {:.2})", float_pair.first(), float_pair.second());
    println!("最大值: {:.2}, 最小值: {:.2}", float_pair.max(), float_pair.min());

    // 创建字符串对
    let string_pair = Pair::new("Hello".to_string(), "World".to_string());
    println!("字符串对: ({}, {})", string_pair.first(), string_pair.second());

    println!("\n=== 泛型函数 ===");

    // 使用 swap 函数
    let (x, y) = swap(100, 200);
    println!("交换后: x={}, y={}", x, y);

    let (a, b) = swap("Rust", "Programming");
    println!("交换后: a={}, b={}", a, b);

    // 使用 print_anything 函数
    print_anything(42);
    print_anything(vec![1, 2, 3, 4, 5]);
    print_anything(("tuple", 123));
}