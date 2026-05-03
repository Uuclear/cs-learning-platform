// solution-02.rs - 借用规则练习解决方案

fn main() {
    // 示例：安全地处理可变引用
    let mut data = vec![1, 2, 3, 4, 5];
    
    // 方法1：使用作用域分离引用
    {
        let first = get_first_element_mut(&mut data);
        *first += 10;
        println!("Modified first element: {}", first);
    } // 可变引用在这里结束
    
    // 现在可以安全地创建新的引用
    let last = get_last_element(&data);
    println!("Last element: {}", last);

    // 方法2：返回值而不是引用
    let max_value = find_max(&data);
    println!("Maximum value: {}", max_value);

    // 字符串处理示例
    let mut text = String::from("Hello");
    append_world(&mut text);
    println!("Modified text: {}", text);

    // 多个不可变引用示例
    let message = String::from("Rust is awesome!");
    let len = message.len();
    let is_empty = message.is_empty();
    println!("Length: {}, Is empty: {}", len, is_empty);
}

fn get_first_element_mut(data: &mut Vec<i32>) -> &mut i32 {
    &mut data[0]
}

fn get_last_element(data: &Vec<i32>) -> &i32 {
    data.last().unwrap()
}

fn find_max(data: &Vec<i32>) -> i32 {
    *data.iter().max().unwrap()
}

fn append_world(text: &mut String) {
    text.push_str(" World!");
}
