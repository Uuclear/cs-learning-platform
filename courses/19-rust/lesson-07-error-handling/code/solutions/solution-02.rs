// solution-02.rs - 自定义错误类型（enum + From trait）完整解决方案

use std::fmt;
use std::fs;
use std::io;
use std::num::ParseIntError;

// 定义自定义错误枚举
#[derive(Debug)]
enum ConfigError {
    IoError(io::Error),
    ParseError(ParseIntError),
    ValidationError(String),
}

// 实现 Error trait
impl std::error::Error for ConfigError {}

// 实现 Display trait 用于友好的错误信息
impl fmt::Display for ConfigError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            ConfigError::IoError(e) => write!(f, "IO 错误: {}", e),
            ConfigError::ParseError(e) => write!(f, "解析错误: {}", e),
            ConfigError::ValidationError(msg) => write!(f, "验证错误: {}", msg),
        }
    }
}

// 实现 From trait 用于自动转换
impl From<io::Error> for ConfigError {
    fn from(error: io::Error) -> Self {
        ConfigError::IoError(error)
    }
}

impl From<ParseIntError> for ConfigError {
    fn from(error: ParseIntError) -> Self {
        ConfigError::ParseError(error)
    }
}

// 配置结构体
#[derive(Debug)]
struct AppConfig {
    port: u16,
    max_connections: usize,
    timeout_seconds: u64,
}

// 从文件读取配置
fn load_config_from_file(filename: &str) -> Result<AppConfig, ConfigError> {
    let contents = fs::read_to_string(filename)?; // 自动转换为 ConfigError::IoError

    let lines: Vec<&str> = contents.lines().collect();
    let mut config = AppConfig {
        port: 8080,
        max_connections: 100,
        timeout_seconds: 30,
    };

    for line in lines {
        if line.trim().is_empty() || line.starts_with('#') {
            continue;
        }

        let parts: Vec<&str> = line.splitn(2, '=').collect();
        if parts.len() != 2 {
            return Err(ConfigError::ValidationError(
                format!("无效的配置行格式: {}", line)
            ));
        }

        let key = parts[0].trim();
        let value = parts[1].trim();

        match key {
            "port" => {
                let port_num: u16 = value.parse()?; // 自动转换为 ConfigError::ParseError
                if port_num == 0 {
                    return Err(ConfigError::ValidationError(
                        "端口号不能为 0".to_string()
                    ));
                }
                config.port = port_num;
            }
            "max_connections" => {
                let connections: usize = value.parse()?;
                if connections == 0 {
                    return Err(ConfigError::ValidationError(
                        "最大连接数不能为 0".to_string()
                    ));
                }
                config.max_connections = connections;
            }
            "timeout_seconds" => {
                let timeout: u64 = value.parse()?;
                if timeout == 0 {
                    return Err(ConfigError::ValidationError(
                        "超时时间不能为 0".to_string()
                    ));
                }
                config.timeout_seconds = timeout;
            }
            _ => {
                return Err(ConfigError::ValidationError(
                    format!("未知的配置项: {}", key)
                ));
            }
        }
    }

    Ok(config)
}

// 创建有效的配置文件
fn create_valid_config() -> io::Result<()> {
    let config_content = r#"# 应用配置文件
port=3000
max_connections=500
timeout_seconds=60
"#;
    fs::write("valid_config.txt", config_content)
}

// 创建无效的配置文件
fn create_invalid_config() -> io::Result<()> {
    let config_content = r#"# 无效的配置文件
port=abc  # 这会导致解析错误
max_connections=-1
timeout_seconds=0  # 这会导致验证错误
"#;
    fs::write("invalid_config.txt", config_content)
}

fn main() {
    println!("=== 自定义错误类型演示 ===\n");

    // 创建测试配置文件
    create_valid_config().expect("无法创建有效配置文件");
    create_invalid_config().expect("无法创建无效配置文件");

    println!("1. 加载有效配置:");
    match load_config_from_file("valid_config.txt") {
        Ok(config) => println!("成功加载配置: {:#?}", config),
        Err(e) => println!("加载失败: {}", e),
    }

    println!("\n2. 加载无效配置:");
    match load_config_from_file("invalid_config.txt") {
        Ok(config) => println!("意外成功加载配置: {:#?}", config),
        Err(e) => println!("预期的加载失败: {}", e),
    }

    println!("\n3. 演示不同类型的错误:");

    // IO 错误示例
    match load_config_from_file("nonexistent.txt") {
        Ok(_) => println!("意外成功"),
        Err(e) => println!("IO 错误: {}", e),
    }

    // 清理测试文件
    fs::remove_file("valid_config.txt").ok();
    fs::remove_file("invalid_config.txt").ok();
}