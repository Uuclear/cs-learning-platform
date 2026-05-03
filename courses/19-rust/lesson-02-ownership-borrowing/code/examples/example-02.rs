// example-02.rs - 借用规则：不可变与可变引用

fn main() {
    let mut s = String::from("hello");

    // 多个不可变引用 - OK！
    let r1 = &s;
    let r2 = &s;
    println!("{} and {}", r1, r2);

    // 一旦我们创建了可变引用，就不能再有不可变引用
    // let r3 = &mut s; // error: cannot borrow `s` as mutable because it is also borrowed as immutable
    // println!("{}, {}, and {}", r1, r2, r3);

    // 正确的方式：先结束不可变引用的作用域
    {
        let r3 = &mut s;
        println!("{}", r3);
    } // r3 在这里离开作用域

    // 现在可以再次创建不可变引用
    let r4 = &s;
    println!("{}", r4);

    // 可变引用的独占性
    let mut s2 = String::from("world");
    let r5 = &mut s2;
    // let r6 = &mut s2; // error: cannot borrow `s2` as mutable more than once at a time
    println!("{}", r5);

    // 函数中的借用
    let s3 = String::from("Rust");
    let len = calculate_length(&s3); // 传递不可变引用
    println!("The length of '{}' is {}.", s3, len); // s3 仍然有效！

    let mut s4 = String::from("mutable");
    change(&mut s4); // 传递可变引用
    println!("Changed string: {}", s4);
}

fn calculate_length(s: &String) -> usize {
    s.len() // s 是对 String 的引用，不会获取所有权
} // s 离开作用域，但因为没有所有权，所以不会 drop 原始数据

fn change(some_string: &mut String) {
    some_string.push_str(", world!");
}
