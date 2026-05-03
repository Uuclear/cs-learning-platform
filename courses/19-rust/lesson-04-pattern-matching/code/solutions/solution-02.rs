// solution-02.rs - 更复杂的模式匹配练习

fn main() {
    // 练习：实现一个更复杂的配置解析器
    #[derive(Debug)]
    enum ConfigValue {
        String(String),
        Number(i32),
        Boolean(bool),
        List(Vec<ConfigValue>),
        Object(std::collections::HashMap<String, ConfigValue>),
    }

    use std::collections::HashMap;

    fn parse_config_value(value: &str) -> ConfigValue {
        // 尝试解析为数字
        if let Ok(num) = value.parse::<i32>() {
            return ConfigValue::Number(num);
        }

        // 尝试解析为布尔值
        match value.to_lowercase().as_str() {
            "true" => return ConfigValue::Boolean(true),
            "false" => return ConfigValue::Boolean(false),
            _ => {}
        }

        // 默认为字符串
        ConfigValue::String(value.to_string())
    }

    fn print_config_value(value: &ConfigValue, indent: usize) {
        let spaces = "  ".repeat(indent);
        match value {
            ConfigValue::String(s) => println!("{}\"{}\"", spaces, s),
            ConfigValue::Number(n) => println!("{}{}", spaces, n),
            ConfigValue::Boolean(b) => println!("{}{}", spaces, b),
            ConfigValue::List(items) => {
                println!("{}[", spaces);
                for item in items {
                    print_config_value(item, indent + 1);
                }
                println!("{}]", spaces);
            }
            ConfigValue::Object(map) => {
                println!("{}{{", spaces);
                for (key, value) in map {
                    println!("{}  {}: ", spaces, key);
                    print_config_value(value, indent + 2);
                }
                println!("{}}}", spaces);
            }
        }
    }

    // 创建测试数据
    let mut config = HashMap::new();
    config.insert("name".to_string(), ConfigValue::String("Alice".to_string()));
    config.insert("age".to_string(), ConfigValue::Number(30));
    config.insert("active".to_string(), ConfigValue::Boolean(true));

    let mut hobbies = Vec::new();
    hobbies.push(ConfigValue::String("reading".to_string()));
    hobbies.push(ConfigValue::String("coding".to_string()));
    config.insert("hobbies".to_string(), ConfigValue::List(hobbies));

    let root_config = ConfigValue::Object(config);
    print_config_value(&root_config, 0);
}