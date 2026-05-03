// solution-01.rs - 所有权练习解决方案

fn main() {
    // 练习1：函数接收 Vec<i32>，添加元素并返回
    let mut vec = vec![1, 2, 3];
    vec = add_element(vec, 4);
    println!("Vector after adding: {:?}", vec);

    // 练习2：计算向量和（使用引用）
    let numbers = vec![1, 2, 3, 4, 5];
    let sum = calculate_sum(&numbers);
    println!("Sum of numbers: {}", sum);

    // 练习3：找到最长单词
    let text = "hello world programming";
    let longest = longest_word(text);
    println!("Longest word: {}", longest);

    // 练习4：修复所有权错误
    let s1 = String::from("hello");
    let s2 = s1.clone(); // 克隆而不是移动
    println!("s1 = {}, s2 = {}", s1, s2);
}

// 练习1的解决方案
fn add_element(mut vec: Vec<i32>, element: i32) -> Vec<i32> {
    vec.push(element);
    vec // 返回修改后的向量（所有权）
}

// 练习2的解决方案
fn calculate_sum(numbers: &Vec<i32>) -> i32 {
    let mut sum = 0;
    for num in numbers {
        sum += num;
    }
    sum
}

// 练习3的解决方案
fn longest_word(text: &str) -> &str {
    let mut longest = "";
    for word in text.split_whitespace() {
        if word.len() > longest.len() {
            longest = word;
        }
    }
    longest
}
