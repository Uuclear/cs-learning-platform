// solution-01.rs - Trait 定义与实现（完整解决方案）
// 包含更完整的 Shape trait 实现和使用示例

trait Shape {
    fn area(&self) -> f64;
    fn perimeter(&self) -> f64;
    fn description(&self) -> String;
}

struct Rectangle {
    width: f64,
    height: f64,
}

impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }

    fn perimeter(&self) -> f64 {
        2.0 * (self.width + self.height)
    }

    fn description(&self) -> String {
        format!("矩形 ({} × {})", self.width, self.height)
    }
}

struct Circle {
    radius: f64,
}

impl Shape for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius.powi(2)
    }

    fn perimeter(&self) -> f64 {
        2.0 * std::f64::consts::PI * self.radius
    }

    fn description(&self) -> String {
        format!("圆形 (半径: {})", self.radius)
    }
}

struct Triangle {
    base: f64,
    height: f64,
    side1: f64,
    side2: f64,
}

impl Shape for Triangle {
    fn area(&self) -> f64 {
        0.5 * self.base * self.height
    }

    fn perimeter(&self) -> f64 {
        self.base + self.side1 + self.side2
    }

    fn description(&self) -> String {
        format!("三角形 (底: {}, 高: {})", self.base, self.height)
    }
}

fn analyze_shapes<T: Shape>(shapes: &[T]) {
    println!("=== 形状分析 ===");
    for shape in shapes {
        println!(
            "{} - 面积: {:.2}, 周长: {:.2}",
            shape.description(),
            shape.area(),
            shape.perimeter()
        );
    }
}

fn main() {
    let rectangles = vec![
        Rectangle { width: 4.0, height: 6.0 },
        Rectangle { width: 3.0, height: 8.0 },
    ];

    let circles = vec![
        Circle { radius: 2.0 },
        Circle { radius: 5.0 },
    ];

    let triangles = vec![Triangle {
        base: 6.0,
        height: 4.0,
        side1: 5.0,
        side2: 5.0,
    }];

    analyze_shapes(&rectangles);
    analyze_shapes(&circles);
    analyze_shapes(&triangles);

    // 使用 trait 对象进行异构集合
    let mixed_shapes: Vec<Box<dyn Shape>> = vec![
        Box::new(Rectangle { width: 2.0, height: 3.0 }),
        Box::new(Circle { radius: 1.5 }),
        Box::new(Triangle {
            base: 4.0,
            height: 3.0,
            side1: 5.0,
            side2: 5.0,
        }),
    ];

    println!("\n=== 混合形状 ===");
    for shape in &mixed_shapes {
        println!(
            "{} - 面积: {:.2}",
            shape.description(),
            shape.area()
        );
    }
}