// solution-03.rs - 文档注释与 cargo doc 生成完整解决方案

//! # 数学工具箱 (Math Toolbox)
//!
//! 这是一个功能完整的数学工具库，提供了各种数学运算函数和常量。
//!
//! ## 特性
//!
//! - **基本算术运算**: 加法、减法、乘法、除法
//! - **安全操作**: 避免除零和溢出错误
//! - **高级数学函数**: 阶乘、质数检测、最大公约数、最小公倍数
//! - **统计函数**: 平均值、中位数、标准差
//! - **数学常量**: π、e、黄金比例等
//!
//! ## 安装
//!
//! 在你的 `Cargo.toml` 中添加:
//!
//! ```toml
//! [dependencies]
//! math-toolbox = "1.0"
//! ```
//!
//! ## 使用示例
//!
//! ```rust
//! use math_toolbox::{add, safe_divide, is_prime, statistics::mean};
//!
//! // 基本运算
//! let sum = add(2, 3);
//! assert_eq!(sum, 5);
//!
//! // 安全除法
//! let division = safe_divide(10.0, 2.0);
//! assert_eq!(division, Some(5.0));
//!
//! // 质数检测
//! assert!(is_prime(17));
//! assert!(!is_prime(18));
//!
//! // 统计计算
//! let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
//! let avg = mean(&numbers);
//! assert_eq!(avg, Some(3.0));
//! ```
//!
//! ## 特性标志
//!
//! - `statistics`: 启用统计函数（默认启用）
//! - `advanced`: 启用高级数学函数
//! - `serde`: 为数据结构启用 Serde 序列化支持
//!
//! ```toml
//! # 启用所有特性
//! math-toolbox = { version = "1.0", features = ["advanced", "serde"] }
//! ```

/// 计算两个整数的和
///
/// # 参数
///
/// * `a` - 第一个整数
/// * `b` - 第二个整数
///
/// # 返回值
///
/// 返回两个整数的和
///
/// # 示例
///
/// ```
/// use math_toolbox::add;
///
/// let result = add(2, 3);
/// assert_eq!(result, 5);
/// ```
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// 计算两个整数的差
///
/// # 参数
///
/// * `a` - 被减数
/// * `b` - 减数
///
/// # 返回值
///
/// 返回 a - b 的结果
///
/// # 示例
///
/// ```
/// use math_toolbox::subtract;
///
/// let result = subtract(5, 3);
/// assert_eq!(result, 2);
/// ```
pub fn subtract(a: i32, b: i32) -> i32 {
    a - b
}

/// 安全除法函数
///
/// 避免除零错误，返回 `Option<f64>`
///
/// # 参数
///
/// * `dividend` - 被除数
/// * `divisor` - 除数
///
/// # 返回值
///
/// 如果除数不为零，返回 `Some(结果)`；否则返回 `None`
///
/// # 示例
///
/// ```
/// use math_toolbox::safe_divide;
///
/// assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
/// assert_eq!(safe_divide(10.0, 0.0), None);
/// ```
pub fn safe_divide(dividend: f64, divisor: f64) -> Option<f64> {
    if divisor == 0.0 {
        None
    } else {
        Some(dividend / divisor)
    }
}

/// 计算阶乘（带溢出检查）
///
/// # 参数
///
/// * `n` - 非负整数
///
/// # 返回值
///
/// 如果计算成功返回 `Some(n!)`，如果溢出返回 `None`
///
/// # 示例
///
/// ```
/// use math_toolbox::factorial;
///
/// assert_eq!(factorial(0), Some(1));
/// assert_eq!(factorial(5), Some(120));
/// assert_eq!(factorial(100), None); // 溢出
/// ```
pub fn factorial(n: u32) -> Option<u64> {
    if n <= 1 {
        Some(1)
    } else {
        factorial(n - 1).and_then(|prev| prev.checked_mul(n as u64))
    }
}

/// 检测一个数是否为质数
///
/// 使用优化的试除法算法
///
/// # 参数
///
/// * `n` - 要检测的正整数
///
/// # 返回值
///
/// 如果 n 是质数返回 `true`，否则返回 `false`
///
/// # 算法复杂度
///
/// 时间复杂度: O(√n)
///
/// # 示例
///
/// ```
/// use math_toolbox::is_prime;
///
/// assert!(is_prime(2));
/// assert!(is_prime(17));
/// assert!(!is_prime(18));
/// assert!(!is_prime(1));
/// ```
pub fn is_prime(n: u32) -> bool {
    if n <= 1 {
        return false;
    }
    if n <= 3 {
        return true;
    }
    if n % 2 == 0 || n % 3 == 0 {
        return false;
    }
    
    let mut i = 5;
    while i * i <= n {
        if n % i == 0 || n % (i + 2) == 0 {
            return false;
        }
        i += 6;
    }
    true
}

/// 计算最大公约数 (GCD)
///
/// 使用欧几里得算法
///
/// # 参数
///
/// * `a` - 第一个正整数
/// * `b` - 第二个正整数
///
/// # 返回值
///
/// 返回 a 和 b 的最大公约数
///
/// # 算法复杂度
///
/// 时间复杂度: O(log(min(a, b)))
///
/// # 示例
///
/// ```
/// use math_toolbox::gcd;
///
/// assert_eq!(gcd(48, 18), 6);
/// assert_eq!(gcd(17, 13), 1);
/// ```
#[cfg(feature = "advanced")]
pub fn gcd(mut a: u32, mut b: u32) -> u32 {
    while b != 0 {
        let temp = b;
        b = a % b;
        a = temp;
    }
    a
}

/// 计算最小公倍数 (LCM)
///
/// # 参数
///
/// * `a` - 第一个正整数
/// * `b` - 第二个正整数
///
/// # 返回值
///
/// 返回 a 和 b 的最小公倍数
///
/// # 示例
///
/// ```
/// use math_toolbox::lcm;
///
/// assert_eq!(lcm(12, 18), 36);
/// ```
#[cfg(feature = "advanced")]
pub fn lcm(a: u32, b: u32) -> Option<u32> {
    if a == 0 || b == 0 {
        Some(0)
    } else {
        gcd(a, b).checked_mul(a / gcd(a, b)).map(|x| x / b)
    }
}

/// 数学常量模块
pub mod constants {
    /// 圆周率 π
    ///
    /// 精度: 15 位小数
    pub const PI: f64 = 3.141592653589793;
    
    /// 自然对数的底 e
    ///
    /// 精度: 15 位小数
    pub const E: f64 = 2.718281828459045;
    
    /// 黄金比例 φ
    ///
    /// φ = (1 + √5) / 2
    pub const PHI: f64 = 1.618033988749895;
    
    /// 平方根 2
    pub const SQRT_2: f64 = 1.4142135623730951;
}

/// 统计函数模块
#[cfg(feature = "statistics")]
pub mod statistics {
    /// 计算平均值
    ///
    /// # 参数
    ///
    /// * `numbers` - 数字切片
    ///
    /// # 返回值
    ///
    /// 如果输入非空返回 `Some(平均值)`，否则返回 `None`
    ///
    /// # 示例
    ///
    /// ```
    /// use math_toolbox::statistics::mean;
    ///
    /// let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    /// assert_eq!(mean(&numbers), Some(3.0));
    /// ```
    pub fn mean(numbers: &[f64]) -> Option<f64> {
        if numbers.is_empty() {
            None
        } else {
            Some(numbers.iter().sum::<f64>() / numbers.len() as f64)
        }
    }
    
    /// 计算中位数
    ///
    /// # 参数
    ///
    /// * `numbers` - 数字切片
    ///
    /// # 返回值
    ///
    /// 如果输入非空返回 `Some(中位数)`，否则返回 `None`
    ///
    /// # 示例
    ///
    /// ```
    /// use math_toolbox::statistics::median;
    ///
    /// let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    /// assert_eq!(median(&numbers), Some(3.0));
    ///
    /// let numbers = vec![1.0, 2.0, 3.0, 4.0];
    /// assert_eq!(median(&numbers), Some(2.5));
    /// ```
    pub fn median(mut numbers: Vec<f64>) -> Option<f64> {
        if numbers.is_empty() {
            return None;
        }
        
        numbers.sort_by(|a, b| a.partial_cmp(b).unwrap());
        let len = numbers.len();
        
        if len % 2 == 0 {
            Some((numbers[len / 2 - 1] + numbers[len / 2]) / 2.0)
        } else {
            Some(numbers[len / 2])
        }
    }
    
    /// 计算标准差
    ///
    /// # 参数
    ///
    /// * `numbers` - 数字切片
    ///
    /// # 返回值
    ///
    /// 如果输入包含至少两个元素返回 `Some(标准差)`，否则返回 `None`
    ///
    /// # 示例
    ///
    /// ```
    /// use math_toolbox::statistics::standard_deviation;
    ///
    /// let numbers = vec![2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
    /// let std_dev = standard_deviation(&numbers);
    /// assert!(std_dev.unwrap() - 2.0 < 0.0001);
    /// ```
    pub fn standard_deviation(numbers: &[f64]) -> Option<f64> {
        if numbers.len() < 2 {
            return None;
        }
        
        let mean_val = mean(numbers)?;
        let variance = numbers.iter()
            .map(|&x| (x - mean_val).powi(2))
            .sum::<f64>() / (numbers.len() - 1) as f64;
        
        Some(variance.sqrt())
    }
}

/// 配置结构体（用于演示 Serde 特性）
#[cfg(feature = "serde")]
#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct MathConfig {
    /// 是否启用调试模式
    #[serde(default)]
    pub debug: bool,
    
    /// 计算精度（小数位数）
    #[serde(default = "default_precision")]
    pub precision: u32,
    
    /// 启用的特性列表
    #[serde(default)]
    pub enabled_features: Vec<String>,
}

#[cfg(feature = "serde")]
fn default_precision() -> u32 {
    6
}

#[cfg(feature = "serde")]
impl Default for MathConfig {
    fn default() -> Self {
        Self {
            debug: false,
            precision: 6,
            enabled_features: vec![],
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
        assert_eq!(add(0, 0), 0);
    }

    #[test]
    fn test_subtract() {
        assert_eq!(subtract(5, 3), 2);
        assert_eq!(subtract(0, 5), -5);
        assert_eq!(subtract(-2, -3), 1);
    }

    #[test]
    fn test_safe_divide() {
        assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
        assert_eq!(safe_divide(-10.0, 2.0), Some(-5.0));
        assert_eq!(safe_divide(10.0, 0.0), None);
        assert_eq!(safe_divide(0.0, 5.0), Some(0.0));
    }

    #[test]
    fn test_factorial() {
        assert_eq!(factorial(0), Some(1));
        assert_eq!(factorial(1), Some(1));
        assert_eq!(factorial(5), Some(120));
        assert_eq!(factorial(20), Some(2432902008176640000));
        assert_eq!(factorial(100), None); // 溢出
    }

    #[test]
    fn test_is_prime() {
        assert!(is_prime(2));
        assert!(is_prime(3));
        assert!(is_prime(17));
        assert!(is_prime(97));
        assert!(!is_prime(1));
        assert!(!is_prime(4));
        assert!(!is_prime(18));
        assert!(!is_prime(100));
    }

    #[cfg(feature = "advanced")]
    #[test]
    fn test_gcd() {
        assert_eq!(gcd(48, 18), 6);
        assert_eq!(gcd(17, 13), 1);
        assert_eq!(gcd(100, 25), 25);
        assert_eq!(gcd(7, 7), 7);
    }

    #[cfg(feature = "advanced")]
    #[test]
    fn test_lcm() {
        assert_eq!(lcm(12, 18), Some(36));
        assert_eq!(lcm(7, 5), Some(35));
        assert_eq!(lcm(0, 5), Some(0));
    }

    #[cfg(feature = "statistics")]
    #[test]
    fn test_mean() {
        let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert_eq!(statistics::mean(&numbers), Some(3.0));
        
        let numbers = vec![10.0];
        assert_eq!(statistics::mean(&numbers), Some(10.0));
        
        let numbers: Vec<f64> = vec![];
        assert_eq!(statistics::mean(&numbers), None);
    }

    #[cfg(feature = "statistics")]
    #[test]
    fn test_median() {
        let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert_eq!(statistics::median(numbers.clone()), Some(3.0));
        
        let numbers = vec![1.0, 2.0, 3.0, 4.0];
        assert_eq!(statistics::median(numbers), Some(2.5));
        
        let numbers = vec![5.0];
        assert_eq!(statistics::median(numbers), Some(5.0));
    }

    #[cfg(feature = "statistics")]
    #[test]
    fn test_standard_deviation() {
        let numbers = vec![2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0];
        let std_dev = statistics::standard_deviation(&numbers).unwrap();
        assert!((std_dev - 2.0).abs() < 0.0001);
        
        let numbers = vec![1.0, 1.0];
        assert_eq!(statistics::standard_deviation(&numbers), Some(0.0));
        
        let numbers = vec![1.0];
        assert_eq!(statistics::standard_deviation(&numbers), None);
    }

    #[cfg(feature = "serde")]
    #[test]
    fn test_math_config_serialization() {
        let config = MathConfig {
            debug: true,
            precision: 8,
            enabled_features: vec!["advanced".to_string(), "statistics".to_string()],
        };
        
        let serialized = serde_json::to_string(&config).unwrap();
        let deserialized: MathConfig = serde_json::from_str(&serialized).unwrap();
        
        assert_eq!(config.debug, deserialized.debug);
        assert_eq!(config.precision, deserialized.precision);
        assert_eq!(config.enabled_features, deserialized.enabled_features);
    }
}