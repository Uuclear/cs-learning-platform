fn main() {
    let numbers = vec![1, 2, 3, 4, 5];

    for num in numbers {
        match num {
            1 => println!("找到了冠军！"),
            2 => println!("亚军也不错！"),
            3 => println!("季军加油！"),
            _ => println!("其他选手：{}", num), // _ 是通配符，匹配所有其他情况
        }
    }

    // 枚举示例
    #[derive(Debug)]
    enum TrafficLight {
        Red,
        Yellow,
        Green,
    }

    let light = TrafficLight::Red;
    match light {
        TrafficLight::Red => println!("停下！"),
        TrafficLight::Yellow => println!("准备！"),
        TrafficLight::Green => println!("通行！"),
    }
}