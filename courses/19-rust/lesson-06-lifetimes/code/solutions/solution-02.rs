// solution-02.rs - ConfigReader 结构体实现

struct ConfigReader<'a> {
    config: &'a str,
}

impl<'a> ConfigReader<'a> {
    fn new(config: &'a str) -> Self {
        ConfigReader { config }
    }

    fn get_value(&self, key: &str) -> Option<&'a str> {
        for line in self.config.lines() {
            // 跳过空行和注释
            if line.trim().is_empty() || line.trim().starts_with('#') {
                continue;
            }

            // 查找键值对（格式：key=value）
            if let Some(pos) = line.find('=') {
                let line_key = line[..pos].trim();
                if line_key == key {
                    return Some(line[pos + 1..].trim());
                }
            }
        }
        None
    }

    // 获取所有配置项
    fn get_all_keys(&self) -> Vec<&'a str> {
        let mut keys = Vec::new();
        for line in self.config.lines() {
            if line.trim().is_empty() || line.trim().starts_with('#') {
                continue;
            }
            if let Some(pos) = line.find('=') {
                keys.push(line[..pos].trim());
            }
        }
        keys
    }
}

fn main() {
    let config_text = r#"
# Database configuration
host=localhost
port=5432
database=myapp

# Cache settings
cache_size=100
cache_ttl=3600
"#;

    let reader = ConfigReader::new(config_text);

    // 测试获取单个值
    if let Some(host) = reader.get_value("host") {
        println!("Database host: {}", host);
    }

    if let Some(port) = reader.get_value("port") {
        println!("Database port: {}", port);
    }

    // 测试获取不存在的键
    match reader.get_value("nonexistent") {
        Some(value) => println!("Found: {}", value),
        None => println!("Key not found"),
    }

    // 测试获取所有键
    let keys = reader.get_all_keys();
    println!("All config keys: {:?}", keys);
}