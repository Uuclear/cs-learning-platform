// solution-02.rs
// 练习2解答：实现向量操作函数

fn double_and_max(vec: &mut Vec<i32>) -> Option<i32> {
    if vec.is_empty() {
        return None;
    }

    // 将所有元素翻倍
    for element in vec.iter_mut() {
        *element *= 2;
    }

    // 找到最大值
    vec.iter().max().copied()
}

fn main() {
    // 测试非空向量
    let mut vec1 = vec![1, 2, 3, 4, 5];
    println!("原向量: {:?}", vec1);
    let max1 = double_and_max(&mut vec1);
    println!("翻倍后: {:?}", vec1);
    println!("最大值: {:?}", max1);

    // 测试空向量
    let mut vec2: Vec<i32> = vec![];
    let max2 = double_and_max(&mut vec2);
    println!("空向量的最大值: {:?}", max2);

    // 验证原始向量被修改
    assert_eq!(vec1, vec![2, 4, 6, 8, 10]);
}