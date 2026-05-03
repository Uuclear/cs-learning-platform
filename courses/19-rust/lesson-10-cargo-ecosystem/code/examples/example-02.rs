// example-02.rs - Cargo.toml 依赖配置演示
// 注意：这个文件主要展示如何在代码中使用不同类型的依赖

use serde::{Deserialize, Serialize};
use anyhow::Result;

// 基础功能：使用标准库
fn basic_string_operations(input: &str) -> String {
    input.to_uppercase()
}

// 使用可选依赖的特性
#[cfg(feature = "json")]
fn json_operations(data: &serde_json::Value) -> Result<String> {
    let serialized = serde_json::to_string_pretty(data)?;
    Ok(serialized)
}

// 使用条件编译
#[cfg(feature = "network")]
async fn fetch_data(url: &str) -> Result<String> {
    let response = reqwest::get(url).await?;
    let text = response.text().await?;
    Ok(text)
}

// 默认功能
#[derive(Serialize, Deserialize, Debug)]
struct Config {
    name: String,
    version: String,
    #[serde(default)]
    debug: bool,
}

impl Config {
    fn new(name: &str, version: &str) -> Self {
        Self {
            name: name.to_string(),
            version: version.to_string(),
            debug: false,
        }
    }
    
    #[cfg(feature = "env")]
    fn from_env() -> Result<Self> {
        let name = std::env::var("APP_NAME").unwrap_or_else(|_| "default".to_string());
        let version = std::env::var("APP_VERSION").unwrap_or_else(|_| "0.1.0".to_string());
        let debug = std::env::var("DEBUG").is_ok();
        
        Ok(Self { name, version, debug })
    }
}

// 主函数展示不同特性的使用
#[tokio::main]
async fn main() -> Result<()> {
    println!("Basic operation: {}", basic_string_operations("hello world"));
    
    let config = Config::new("my-app", "1.0.0");
    println!("Config: {:?}", config);
    
    // 条件编译块
    #[cfg(feature = "json")]
    {
        let data = serde_json::json!({
            "name": "test",
            "value": 42
        });
        match json_operations(&data) {
            Ok(json_str) => println!("JSON:\n{}", json_str),
            Err(e) => eprintln!("JSON error: {}", e),
        }
    }
    
    #[cfg(feature = "network")]
    {
        match fetch_data("https://httpbin.org/json").await {
            Ok(data) => println!("Fetched data length: {}", data.len()),
            Err(e) => eprintln!("Network error: {}", e),
        }
    }
    
    Ok(())
}
