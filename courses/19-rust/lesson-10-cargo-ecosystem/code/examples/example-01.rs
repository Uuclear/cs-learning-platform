// example-01.rs - 单元测试与集成测试演示

/// 计算两个数的和
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// 安全除法，避免除零错误
pub fn safe_divide(dividend: f64, divisor: f64) -> Option<f64> {
    if divisor == 0.0 {
        None
    } else {
        Some(dividend / divisor)
    }
}

/// 计算阶乘
pub fn factorial(n: u32) -> u64 {
    if n <= 1 {
        1
    } else {
        (n as u64) * factorial(n - 1)
    }
}

// 单元测试模块
#[cfg(test)]
mod unit_tests {
    use super::*;

    #[test]
    fn test_add_positive_numbers() {
        assert_eq!(add(2, 3), 5);
    }

    #[test]
    fn test_add_negative_numbers() {
        assert_eq!(add(-2, -3), -5);
    }

    #[test]
    fn test_add_mixed_numbers() {
        assert_eq!(add(-2, 3), 1);
    }

    #[test]
    fn test_safe_divide_normal() {
        assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
    }

    #[test]
    fn test_safe_divide_by_zero() {
        assert_eq!(safe_divide(10.0, 0.0), None);
    }

    #[test]
    fn test_factorial_zero() {
        assert_eq!(factorial(0), 1);
    }

    #[test]
    fn test_factorial_one() {
        assert_eq!(factorial(1), 1);
    }

    #[test]
    fn test_factorial_five() {
        assert_eq!(factorial(5), 120);
    }

    #[test]
    #[should_panic(expected = "attempt to multiply with overflow")]
    fn test_factorial_overflow() {
        // 这个测试会 panic，因为我们没有处理溢出
        let _ = factorial(100);
    }
}

// 集成测试应该放在 tests/ 目录下，但这里我们模拟集成测试的概念
#[cfg(test)]
mod integration_tests {
    use super::*;

    #[test]
    fn test_math_operations_together() {
        let sum = add(10, 5);
        let result = safe_divide(sum as f64, 3.0);
        assert_eq!(result, Some(5.0));
    }

    #[test]
    fn test_factorial_in_calculation() {
        let fact = factorial(4); // 24
        let divided = safe_divide(fact as f64, 8.0); // 3.0
        assert_eq!(divided, Some(3.0));
    }
}
