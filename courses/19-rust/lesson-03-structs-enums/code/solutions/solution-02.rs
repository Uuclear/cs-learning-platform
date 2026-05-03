// solution-02.rs - 枚举练习解决方案

// 定义交通信号灯枚举
enum TrafficLight {
    Red,
    Yellow,
    Green,
}

impl TrafficLight {
    fn next(&self) -> TrafficLight {
        match self {
            TrafficLight::Red => TrafficLight::Green,
            TrafficLight::Green => TrafficLight::Yellow,
            TrafficLight::Yellow => TrafficLight::Red,
        }
    }

    fn action(&self) -> &'static str {
        match self {
            TrafficLight::Red => "停车",
            TrafficLight::Yellow => "准备",
            TrafficLight::Green => "通行",
        }
    }

    fn color(&self) -> &'static str {
        match self {
            TrafficLight::Red => "红色",
            TrafficLight::Yellow => "黄色",
            TrafficLight::Green => "绿色",
        }
    }
}

// 定义计算器操作枚举
enum CalculatorOperation {
    Add(f64, f64),
    Subtract(f64, f64),
    Multiply(f64, f64),
    Divide(f64, f64),
}

impl CalculatorOperation {
    fn calculate(&self) -> Option<f64> {
        match self {
            CalculatorOperation::Add(a, b) => Some(a + b),
            CalculatorOperation::Subtract(a, b) => Some(a - b),
            CalculatorOperation::Multiply(a, b) => Some(a * b),
            CalculatorOperation::Divide(a, b) => {
                if *b == 0.0 {
                    None
                } else {
                    Some(a / b)
                }
            }
        }
    }

    fn operation_name(&self) -> &'static str {
        match self {
            CalculatorOperation::Add(_, _) => "加法",
            CalculatorOperation::Subtract(_, _) => "减法",
            CalculatorOperation::Multiply(_, _) => "乘法",
            CalculatorOperation::Divide(_, _) => "除法",
        }
    }
}

fn main() {
    // 测试交通信号灯
    let mut light = TrafficLight::Red;
    println!("当前信号灯: {} - {}", light.color(), light.action());

    light = light.next();
    println!("下一个信号灯: {} - {}", light.color(), light.action());

    light = light.next();
    println!("再下一个信号灯: {} - {}", light.color(), light.action());

    light = light.next();
    println!("循环回到: {} - {}", light.color(), light.action());

    println!("\n=== 计算器操作 ===");

    // 测试计算器操作
    let operations = vec![
        CalculatorOperation::Add(10.0, 5.0),
        CalculatorOperation::Subtract(10.0, 5.0),
        CalculatorOperation::Multiply(10.0, 5.0),
        CalculatorOperation::Divide(10.0, 5.0),
        CalculatorOperation::Divide(10.0, 0.0), // 除零测试
    ];

    for op in operations {
        match op.calculate() {
            Some(result) => println!("{}: {:.2}", op.operation_name(), result),
            None => println!("{}: 除零错误", op.operation_name()),
        }
    }
}