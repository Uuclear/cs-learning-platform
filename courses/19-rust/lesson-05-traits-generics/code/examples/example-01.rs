// example-01.rs - Trait 定义与实现
// 演示如何定义 Shape trait 并为不同形状实现 area 方法

// 定义 Shape trait
trait Shape {
    // 计算面积的方法
    fn area(&self) -> f64;

    // 可选：提供默认实现的方法
    fn description(&self) -> String {
        "这是一个几何形状".to_string()
    }
}

// 定义矩形结构体
struct Rectangle {
    width: f64,
    height: f64,
}

// 为 Rectangle 实现 Shape trait
impl Shape for Rectangle {
    fn area(&self) -> f64 {
        self.width * self.height
    }

    fn description(&self) -> String {
        format!("矩形：宽{}，高{}", self.width, self.height)
    }
}

// 定义圆形结构体
struct Circle {
    radius: f64,
}

// 为 Circle 实现 Shape trait
impl Shape for Circle {
    fn area(&self) -> f64 {
        std::f64::consts::PI * self.radius * self.radius
    }

    fn description(&self) -> String {
        format!("圆形：半径{}", self.radius)
    }
}

// 使用泛型函数处理任何实现了 Shape 的类型
fn print_shape_info<T: Shape>(shape: &T) {
    println!("{} - 面积: {:.2}", shape.description(), shape.area());
}

fn main() {
    let rectangle = Rectangle { width: 5.0, height: 3.0 };
    let circle = Circle { radius: 2.0 };

    println!("=== 形状信息 ===");
    print_shape_info(&rectangle);
    print_shape_info(&circle);

    // 直接调用 trait 方法
    println!("\n=== 直接调用 ===");
    println!("矩形面积: {:.2}", rectangle.area());
    println!("圆形面积: {:.2}", circle.area());
}