// solution-03.rs - 生命周期约束理解

// 函数签名：fn choose_first<'a, 'b>(x: &'a str, y: &'b str) -> &'a str
// 问题：这个函数能安全地返回 y 吗？

// 答案：不能！因为返回类型指定为 &'a str，而 y 的生命周期是 'b。
// 除非 'b: 'a（即 'b 至少和 'a 一样长），否则这是不安全的。

// 正确的实现只能返回 x，或者需要添加生命周期约束
fn choose_first<'a, 'b>(x: &'a str, y: &'b str) -> &'a str {
    // 只能安全地返回 x，因为返回类型要求是 &'a str
    x

    // 以下代码会编译错误：
    // if some_condition { x } else { y }  // ❌ 不能返回 y
}

// 如果我们想要能够返回任一个参数，需要不同的方法：

// 方法1：使用相同的生命周期参数
fn choose_any<'a>(x: &'a str, y: &'a str, choose_x: bool) -> &'a str {
    if choose_x { x } else { y }
}

// 方法2：添加生命周期约束 'b: 'a
fn choose_with_constraint<'a, 'b>(x: &'a str, y: &'b str, choose_x: bool) -> &'a str
where
    'b: 'a  // 'b 至少和 'a 一样长
{
    if choose_x { x } else { y }
}

// 方法3：返回所有权而不是引用
fn choose_owned(x: &str, y: &str, choose_x: bool) -> String {
    if choose_x { x.to_string() } else { y.to_string() }
}

fn main() {
    let string1 = "hello";
    let string2 = "world";

    // 使用方法1
    let result1 = choose_any(string1, string2, true);
    println!("Chose first: {}", result1);

    let result2 = choose_any(string1, string2, false);
    println!("Chose second: {}", result2);

    // 使用方法2（需要确保生命周期约束满足）
    let result3 = choose_with_constraint(string1, string2, false);
    println!("Chose with constraint: {}", result3);

    // 使用方法3
    let result4 = choose_owned(string1, string2, false);
    println!("Chose owned: {}", result4);

    // 演示生命周期约束的重要性
    {
        let inner_string = String::from("inner");
        // 这样调用是安全的，因为 string1 的生命周期比 inner_string 长
        let _result = choose_with_constraint(string1, &inner_string, true);
        // 但如果尝试 choose_with_constraint(inner_string, string1, false)，
        // 就会编译错误，因为 string1 的生命周期不足以满足 'b: 'a 约束
    }
}