// example-03.rs - Trait bounds 与 derive 宏演示
// 展示如何使用 trait bounds 约束泛型参数和 derive 宏

// 使用 derive 宏自动实现标准 trait
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: f64,
    y: f64,
}

// 实现自定义 trait
trait Distance {
    fn distance_from_origin(&self) -> f64;
}

impl Distance for Point {
    fn distance_from_origin(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }
}

// 泛型函数，使用多个 trait bounds
fn process_points<T>(points: Vec<T>) -> Vec<f64>
where
    T: Distance + Clone + std::fmt::Debug,
{
    println!("处理点集: {:?}", points);
    points.iter().map(|p| p.distance_from_origin()).collect()
}

// 另一个结构体，也实现 Distance trait
#[derive(Debug, Clone)]
struct Vector3D {
    x: f64,
    y: f64,
    z: f64,
}

impl Distance for Vector3D {
    fn distance_from_origin(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2) + self.z.powi(2)).sqrt()
    }
}

// 使用 impl Trait 返回具体类型
fn create_point(x: f64, y: f64) -> impl Distance + Clone {
    Point { x, y }
}

// 使用 Box<dyn Trait> 返回 trait 对象
fn create_shape(is_circle: bool) -> Box<dyn std::fmt::Display> {
    if is_circle {
        Box::new("圆形")
    } else {
        Box::new("矩形")
    }
}

fn main() {
    println!("=== Derive 宏演示 ===");

    let p1 = Point { x: 3.0, y: 4.0 };
    let p2 = p1.clone(); // Clone trait 允许克隆

    println!("点 p1: {:?}", p1);
    println!("点 p2: {:?}", p2);
    println!("p1 == p2: {}", p1 == p2); // PartialEq trait 允许比较

    println!("p1 到原点距离: {:.2}", p1.distance_from_origin());

    println!("\n=== Trait Bounds 演示 ===");

    let points = vec![
        Point { x: 1.0, y: 1.0 },
        Point { x: 2.0, y: 2.0 },
        Point { x: 3.0, y: 4.0 },
    ];

    let distances = process_points(points);
    println!("距离列表: {:?}", distances);

    println!("\n=== 不同类型的 Distance 实现 ===");

    let vectors = vec![
        Vector3D { x: 1.0, y: 1.0, z: 1.0 },
        Vector3D { x: 2.0, y: 2.0, z: 2.0 },
    ];

    let vector_distances = process_points(vectors);
    println!("3D向量距离列表: {:?}", vector_distances);

    println!("\n=== Impl Trait 和 Trait 对象 ===");

    let my_point = create_point(5.0, 12.0);
    println!("创建的点到原点距离: {:.2}", my_point.distance_from_origin());

    let shape1 = create_shape(true);
    let shape2 = create_shape(false);
    println!("形状1: {}", shape1);
    println!("形状2: {}", shape2);
}