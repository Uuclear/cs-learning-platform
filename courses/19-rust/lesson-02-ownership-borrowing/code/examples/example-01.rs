// example-01.rs - 所有权转移与 move 语义演示

fn main() {
    // 基本的所有权转移
    let s1 = String::from("hello");
    println!("s1 = {}", s1);

    let s2 = s1; // 所有权从 s1 移动到 s2
    println!("s2 = {}", s2);

    // 下面这行会编译错误，因为 s1 已经被移动了
    // println!("s1 = {}", s1); // error: value borrowed here after move

    // 函数调用中的所有权转移
    let s3 = String::from("world");
    takes_ownership(s3); // s3 的所有权移动到函数中

    // 下面这行也会编译错误
    // println!("s3 = {}", s3); // error: borrow of moved value

    // Copy 类型的例子（不会发生移动）
    let x = 5;
    let y = x; // x 被复制，不是移动
    println!("x = {}, y = {}", x, y); // 都能正常工作！
}

fn takes_ownership(some_string: String) {
    println!("Inside function: {}", some_string);
    // some_string 在这里离开作用域并被 drop
}
