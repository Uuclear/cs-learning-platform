fn main() {
    // 练习1：完善枚举处理器
    enum Operation {
        Add(i32, i32),
        Subtract(i32, i32),
        Multiply(i32, i32),
        Divide(i32, i32),
    }

    fn calculate(op: Operation) -> Option<i32> {
        match op {
            Operation::Add(a, b) => Some(a + b),
            Operation::Subtract(a, b) => Some(a - b),
            Operation::Multiply(a, b) => Some(a * b),
            Operation::Divide(a, b) => {
                if b == 0 {
                    None
                } else {
                    Some(a / b)
                }
            }
        }
    }

    // 测试
    println!("{:?}", calculate(Operation::Add(5, 3))); // Some(8)
    println!("{:?}", calculate(Operation::Divide(10, 2))); // Some(5)
    println!("{:?}", calculate(Operation::Divide(10, 0))); // None

    // 练习2：实现配置解析器
    #[derive(Debug)]
    enum ConfigValue {
        String(String),
        Number(i32),
        Boolean(bool),
        List(Vec<ConfigValue>),
    }

    fn get_config_value_type(value: &ConfigValue) -> &'static str {
        match value {
            ConfigValue::String(_) => "string",
            ConfigValue::Number(_) => "number",
            ConfigValue::Boolean(_) => "boolean",
            ConfigValue::List(_) => "list",
        }
    }

    let config_values = vec![
        ConfigValue::String("hello".to_string()),
        ConfigValue::Number(42),
        ConfigValue::Boolean(true),
        ConfigValue::List(vec![ConfigValue::Number(1), ConfigValue::Number(2)]),
    ];

    for value in config_values {
        println!("类型: {}", get_config_value_type(&value));
    }

    // 练习3：优化状态转换
    #[derive(Debug, Clone)]
    enum State {
        Idle,
        Processing { task_id: u32, progress: f32 },
        Completed { result: String },
        Failed { error: String },
        Paused { task_id: u32, reason: String },
    }

    fn handle_state(current: State) -> State {
        match current {
            State::Idle => {
                println!("开始新任务");
                State::Processing { task_id: 1, progress: 0.0 }
            }
            State::Processing { task_id, progress } if progress < 1.0 => {
                let new_progress = progress + 0.1;
                println!("任务 {} 进度: {:.1}%", task_id, new_progress * 100.0);
                State::Processing { task_id, progress: new_progress }
            }
            State::Processing { task_id, .. } => {
                println!("任务 {} 完成", task_id);
                State::Completed { result: "Success!".to_string() }
            }
            State::Completed { result } => {
                println!("最终结果: {}", result);
                State::Idle
            }
            State::Failed { error } => {
                println!("错误: {}", error);
                State::Idle
            }
            State::Paused { task_id, reason } => {
                println!("任务 {} 暂停，原因: {}", task_id, reason);
                State::Processing { task_id, progress: 0.5 }
            }
        }
    }

    // 测试状态机
    let initial_state = State::Idle;
    let next_state = handle_state(initial_state);
    println!("下一个状态: {:?}", next_state);
}