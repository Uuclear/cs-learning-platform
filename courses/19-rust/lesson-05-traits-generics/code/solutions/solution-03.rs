// solution-03.rs - Trait bounds 与 derive 宏（完整解决方案）
// 综合示例展示高级 trait 使用和泛型约束

use std::fmt::{Debug, Display};

// 自定义错误类型
#[derive(Debug)]
struct ValidationError(String);

impl Display for ValidationError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        write!(f, "验证错误: {}", self.0)
    }
}

impl std::error::Error for ValidationError {}

// 可验证的 trait
trait Validatable {
    fn validate(&self) -> Result<(), ValidationError>;
}

// 坐标点结构体
#[derive(Debug, Clone, PartialEq)]
struct Point2D {
    x: f64,
    y: f64,
}

impl Validatable for Point2D {
    fn validate(&self) -> Result<(), ValidationError> {
        if self.x.is_nan() || self.y.is_nan() {
            Err(ValidationError("坐标不能为 NaN".to_string()))
        } else if self.x.is_infinite() || self.y.is_infinite() {
            Err(ValidationError("坐标不能为无穷大".to_string()))
        } else {
            Ok(())
        }
    }
}

// 3D 向量结构体
#[derive(Debug, Clone)]
struct Vector3D {
    x: f64,
    y: f64,
    z: f64,
}

impl Validatable for Vector3D {
    fn validate(&self) -> Result<(), ValidationError> {
        if self.x.is_nan() || self.y.is_nan() || self.z.is_nan() {
            Err(ValidationError("向量分量不能为 NaN".to_string()))
        } else if self.x.is_infinite() || self.y.is_infinite() || self.z.is_infinite() {
            Err(ValidationError("向量分量不能为无穷大".to_string()))
        } else {
            Ok(())
        }
    }
}

// 距离计算 trait
trait DistanceFrom<T> {
    fn distance_from(&self, other: &T) -> f64;
}

impl DistanceFrom<Point2D> for Point2D {
    fn distance_from(&self, other: &Point2D) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}

// 泛型验证函数
fn validate_and_process<T>(items: Vec<T>) -> Result<Vec<T>, ValidationError>
where
    T: Validatable + Clone,
{
    for item in &items {
        item.validate()?;
    }
    Ok(items)
}

// 泛型距离计算函数
fn calculate_distances<T, U>(points: &[T], reference: &U) -> Vec<f64>
where
    T: DistanceFrom<U> + Clone,
    U: Clone,
{
    points.iter().map(|p| p.distance_from(reference)).collect()
}

// 使用关联类型的高级 trait
trait Container {
    type Item;
    fn get(&self, index: usize) -> Option<&Self::Item>;
    fn len(&self) -> usize;
}

impl<T> Container for Vec<T> {
    type Item = T;
    fn get(&self, index: usize) -> Option<&Self::Item> {
        self.get(index)
    }
    fn len(&self) -> usize {
        self.len()
    }
}

// 多重 trait bounds 的复杂函数
fn process_valid_containers<C, T>(
    containers: Vec<C>,
) -> Result<Vec<(usize, Option<String>)>, ValidationError>
where
    C: Container<Item = T> + Validatable,
    T: Display + Clone,
{
    let mut results = Vec::new();

    for container in containers {
        container.validate()?;
        let len = container.len();
        let first_item = container.get(0).map(|item| item.to_string());
        results.push((len, first_item));
    }

    Ok(results)
}

fn main() {
    println!("=== 验证功能 ===");

    // 有效的点
    let valid_points = vec![
        Point2D { x: 1.0, y: 2.0 },
        Point2D { x: 3.0, y: 4.0 },
    ];

    match validate_and_process(valid_points.clone()) {
        Ok(points) => println!("验证成功，处理了 {} 个点", points.len()),
        Err(e) => println!("验证失败: {}", e),
    }

    // 包含无效点的情况
    let invalid_points = vec![
        Point2D { x: 1.0, y: 2.0 },
        Point2D { x: f64::NAN, y: 3.0 }, // 无效点
    ];

    match validate_and_process(invalid_points) {
        Ok(_) => println!("不应该到这里"),
        Err(e) => println!("捕获到验证错误: {}", e),
    }

    println!("\n=== 距离计算 ===");
    let points = vec![
        Point2D { x: 0.0, y: 0.0 },
        Point2D { x: 3.0, y: 4.0 },
        Point2D { x: 1.0, y: 1.0 },
    ];
    let origin = Point2D { x: 0.0, y: 0.0 };

    let distances = calculate_distances(&points, &origin);
    println!("到原点的距离: {:?}", distances);

    println!("\n=== 关联类型和容器 ===");
    let string_vectors = vec![
        vec!["Hello".to_string(), "World".to_string()],
        vec!["Rust".to_string(), "Programming".to_string(), "Language".to_string()],
    ];

    // 为 Vec<String> 实现 Validatable（简单实现）
    impl Validatable for Vec<String> {
        fn validate(&self) -> Result<(), ValidationError> {
            if self.is_empty() {
                Err(ValidationError("向量不能为空".to_string()))
            } else {
                Ok(())
            }
        }
    }

    match process_valid_containers(string_vectors) {
        Ok(results) => {
            for (len, first) in results {
                println!("容器长度: {}, 第一个元素: {:?}", len, first);
            }
        }
        Err(e) => println!("处理容器时出错: {}", e),
    }

    println!("\n=== 高级 trait 对象使用 ===");
    let shapes: Vec<Box<dyn Display>> = vec![
        Box::new("圆形"),
        Box::new("矩形"),
        Box::new("三角形"),
    ];

    for shape in shapes {
        println!("形状: {}", shape);
    }
}