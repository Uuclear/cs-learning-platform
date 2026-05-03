// example-03.rs - 文档注释与 cargo doc 生成演示

//! # 数学工具箱
//!
//! 这是一个简单的数学工具库，提供了基本的数学运算函数。
//!
//! ## 特性
//!
//! - 基本算术运算
//! - 安全的除法操作
//! - 阶乘计算
//! - 质数检测
//!
//! ## 使用示例
//!
//! ```rust
//! use math_toolbox::{add, safe_divide, is_prime};
//!
//! let sum = add(2, 3);
//! assert_eq!(sum, 5);
//!
//! let division = safe_divide(10.0, 2.0);
//! assert_eq!(division, Some(5.0));
//!
//! assert!(is_prime(17));
//! assert!(!is_prime(18));
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

/// 计算阶乘
///
/// # 参数
///
/// * `n` - 非负整数
///
/// # 返回值
///
/// 返回 n 的阶乘
///
/// # Panics
///
/// 如果 n 太大导致溢出，会 panic
///
/// # 示例
///
/// ```
/// use math_toolbox::factorial;
///
/// assert_eq!(factorial(0), 1);
/// assert_eq!(factorial(5), 120);
/// ```
pub fn factorial(n: u32) -> u64 {
    if n <= 1 {
        1
    } else {
        (n as u64) * factorial(n - 1)
    }
}

/// 检测一个数是否为质数
///
/// # 参数
///
/// * `n` - 要检测的正整数
///
/// # 返回值
///
/// 如果 n 是质数返回 `true`，否则返回 `false`
///
/// # 示例
///
/// ```
/// use math_toolbox::is_prime;
///
/// assert!(is_prime(2));
/// assert!(is_prime(17));
/// assert!(!is_prime(18));
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

/// 数学常量模块
pub mod constants {
    /// 圆周率 π
    pub const PI: f64 = 3.141592653589793;
    
    /// 自然对数的底 e
    pub const E: f64 = 2.718281828459045;
    
    /// 黄金比例 φ
    pub const PHI: f64 = 1.618033988749895;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(-1, 1), 0);
    }

    #[test]
    fn test_safe_divide() {
        assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
        assert_eq!(safe_divide(10.0, 0.0), None);
    }

    #[test]
    fn test_factorial() {
        assert_eq!(factorial(0), 1);
        assert_eq!(factorial(5), 120);
    }

    #[test]
    fn test_is_prime() {
        assert!(is_prime(2));
        assert!(is_prime(17));
        assert!(!is_prime(18));
        assert!(!is_prime(1));
    }
}