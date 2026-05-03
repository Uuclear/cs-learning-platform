// solution-01.rs - 单元测试与集成测试完整解决方案

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

/// 计算阶乘（带溢出检查）
pub fn factorial(n: u32) -> Option<u64> {
    if n <= 1 {
        Some(1)
    } else {
        factorial(n - 1).and_then(|prev| prev.checked_mul(n as u64))
    }
}

/// 计算平均值
pub fn average(numbers: &[f64]) -> Option<f64> {
    if numbers.is_empty() {
        None
    } else {
        Some(numbers.iter().sum::<f64>() / numbers.len() as f64)
    }
}

// 单元测试模块
#[cfg(test)]
mod unit_tests {
    use super::*;

    #[test]
    fn test_add_positive_numbers() {
        assert_eq!(add(2, 3), 5);
        assert_eq!(add(100, 200), 300);
    }

    #[test]
    fn test_add_negative_numbers() {
        assert_eq!(add(-2, -3), -5);
        assert_eq!(add(-100, -200), -300);
    }

    #[test]
    fn test_add_mixed_numbers() {
        assert_eq!(add(-2, 3), 1);
        assert_eq!(add(5, -3), 2);
    }

    #[test]
    fn test_add_zero() {
        assert_eq!(add(0, 5), 5);
        assert_eq!(add(-5, 0), -5);
    }

    #[test]
    fn test_safe_divide_normal() {
        assert_eq!(safe_divide(10.0, 2.0), Some(5.0));
        assert_eq!(safe_divide(-10.0, 2.0), Some(-5.0));
    }

    #[test]
    fn test_safe_divide_by_zero() {
        assert_eq!(safe_divide(10.0, 0.0), None);
        assert_eq!(safe_divide(-10.0, 0.0), None);
        assert_eq!(safe_divide(0.0, 0.0), None);
    }

    #[test]
    fn test_factorial_zero() {
        assert_eq!(factorial(0), Some(1));
    }

    #[test]
    fn test_factorial_one() {
        assert_eq!(factorial(1), Some(1));
    }

    #[test]
    fn test_factorial_small_numbers() {
        assert_eq!(factorial(5), Some(120));
        assert_eq!(factorial(10), Some(3628800));
    }

    #[test]
    fn test_factorial_overflow() {
        // 现在不会 panic，而是返回 None
        assert_eq!(factorial(100), None);
    }

    #[test]
    fn test_average_normal() {
        let numbers = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        assert_eq!(average(&numbers), Some(3.0));
    }

    #[test]
    fn test_average_single() {
        let numbers = vec![42.0];
        assert_eq!(average(&numbers), Some(42.0));
    }

    #[test]
    fn test_average_empty() {
        let numbers: Vec<f64> = vec![];
        assert_eq!(average(&numbers), None);
    }

    #[test]
    fn test_average_negative() {
        let numbers = vec![-1.0, -2.0, -3.0];
        assert_eq!(average(&numbers), Some(-2.0));
    }
}

// 集成测试概念演示
#[cfg(test)]
mod integration_tests {
    use super::*;

    #[test]
    fn test_combined_operations() {
        // 测试多个函数组合使用
        let sum = add(10, 5); // 15
        let avg_input = vec![sum as f64, 5.0, 10.0]; // [15.0, 5.0, 10.0]
        let avg = average(&avg_input); // Some(10.0)
        let divided = safe_divide(avg.unwrap(), 2.0); // Some(5.0)
        
        assert_eq!(divided, Some(5.0));
    }

    #[test]
    fn test_factorial_in_context() {
        let fact_5 = factorial(5).unwrap(); // 120
        let numbers = vec![fact_5 as f64, 120.0, 120.0];
        let avg = average(&numbers).unwrap(); // 120.0
        let result = safe_divide(avg, 24.0); // Some(5.0)
        
        assert_eq!(result, Some(5.0));
    }

    #[test]
    fn test_edge_case_handling() {
        // 测试边界情况的组合
        let empty_avg = average(&[]);
        assert_eq!(empty_avg, None);
        
        let zero_division = safe_divide(10.0, 0.0);
        assert_eq!(zero_division, None);
        
        let overflow_factorial = factorial(100);
        assert_eq!(overflow_factorial, None);
    }
}