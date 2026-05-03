// solution-02.rs - Cargo.toml 依赖配置完整解决方案

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
#[derive(Serialize, Deserialize, Debug, Clone)]
struct Config {
    name: String,
    version: String,
    #[serde(default)]
    debug: bool,
    #[serde(default)]
    features: Vec<String>,
}

impl Config {
    fn new(name: &str, version: &str) -> Self {
        Self {
            name: name.to_string(),
            version: version.to_string(),
            debug: false,
            features: vec![],
        }
    }
    
    #[cfg(feature = "env")]
    fn from_env() -> Result<Self> {
        let name = std::env::var("APP_NAME").unwrap_or_else(|_| "default".to_string());
        let version = std::env::var("APP_VERSION").unwrap_or_else(|_| "0.1.0".to_string());
        let debug = std::env::var("DEBUG").is_ok();
        
        // 获取启用的特性
        let features = std::env::var("FEATURES")
            .map(|s| s.split(',').map(|s| s.trim().to_string()).collect())
            .unwrap_or_else(|_| vec![]);
        
        Ok(Self { name, version, debug, features })
    }
    
    fn enable_feature(&mut self, feature: &str) {
        if !self.features.contains(&feature.to_string()) {
            self.features.push(feature.to_string());
        }
    }
}

// 配置管理器
struct ConfigManager {
    configs: std::collections::HashMap<String, Config>,
}

impl ConfigManager {
    fn new() -> Self {
        Self {
            configs: std::collections::HashMap::new(),
        }
    }
    
    fn add_config(&mut self, key: &str, config: Config) {
        self.configs.insert(key.to_string(), config);
    }
    
    fn get_config(&self, key: &str) -> Option<&Config> {
        self.configs.get(key)
    }
    
    fn list_configs(&self) -> Vec<String> {
        self.configs.keys().cloned().collect()
    }
}

// 主函数展示不同特性的使用
#[tokio::main]
async fn main() -> Result<()> {
    println!("=== 数学工具箱配置演示 ===");
    println!("Basic operation: {}", basic_string_operations("hello world"));
    
    let mut config = Config::new("math-toolbox", "1.0.0");
    config.enable_feature("basic-math");
    println!("Config: {:?}", config);
    
    // 条件编译块
    #[cfg(feature = "json")]
    {
        println!("\n--- JSON 特性启用 ---");
        let data = serde_json::json!({
            "name": "math-toolbox",
            "version": "1.0.0",
            "features": ["basic-math", "advanced-math"],
            "config": {
                "debug": true,
                "precision": 6
            }
        });
        match json_operations(&data) {
            Ok(json_str) => println!("JSON 配置:\n{}", json_str),
            Err(e) => eprintln!("JSON 错误: {}", e),
        }
    }
    
    #[cfg(not(feature = "json"))]
    {
        println!("\n--- JSON 特性未启用 ---");
        println!("要启用 JSON 支持，请使用: cargo run --features json");
    }
    
    #[cfg(feature = "network")]
    {
        println!("\n--- 网络特性启用 ---");
        match fetch_data("https://httpbin.org/json").await {
            Ok(data) => {
                println!("成功获取网络数据!");
                println!("数据长度: {} 字符", data.len());
                // 只显示前200个字符
                println!("数据预览: {:.200}", data);
            },
            Err(e) => eprintln!("网络请求失败: {}", e),
        }
    }
    
    #[cfg(not(feature = "network"))]
    {
        println!("\n--- 网络特性未启用 ---");
        println!("要启用网络支持，请使用: cargo run --features network");
    }
    
    #[cfg(feature = "env")]
    {
        println!("\n--- 环境变量特性启用 ---");
        match Config::from_env() {
            Ok(env_config) => println!("从环境变量加载的配置: {:?}", env_config),
            Err(e) => eprintln!("加载环境变量配置失败: {}", e),
        }
    }
    
    // 演示配置管理器
    let mut manager = ConfigManager::new();
    manager.add_config("default", Config::new("default-app", "1.0.0"));
    manager.add_config("dev", {
        let mut dev_config = Config::new("dev-app", "1.0.0-dev");
        dev_config.debug = true;
        dev_config.enable_feature("debug-mode");
        dev_config
    });
    
    println!("\n--- 配置管理器 ---");
    println!("可用配置: {:?}", manager.list_configs());
    if let Some(default_config) = manager.get_config("default") {
        println!("默认配置: {:?}", default_config);
    }
    
    Ok(())
}