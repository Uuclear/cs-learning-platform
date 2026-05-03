// example-01.rs - 结构体定义与方法（User 类型）

// 定义一个普通的结构体
struct User {
    username: String,
    email: String,
    sign_in_count: u64,
    active: bool,
}

// 为 User 结构体实现方法
impl User {
    // 关联函数（类似构造函数）
    fn new(username: String, email: String) -> User {
        User {
            username,
            email,
            sign_in_count: 1,
            active: true,
        }
    }

    // 实例方法
    fn activate(&mut self) {
        self.active = true;
    }

    fn deactivate(&mut self) {
        self.active = false;
    }

    fn increment_sign_in_count(&mut self) {
        self.sign_in_count += 1;
    }

    fn get_username(&self) -> &str {
        &self.username
    }
}

// 元组结构体示例
struct Color(u8, u8, u8);
struct Point(i32, i32);

// 单元结构体示例
struct AlwaysEqual;

fn main() {
    // 创建 User 实例
    let mut user1 = User::new(
        String::from("alice"),
        String::from("alice@example.com")
    );

    println!("用户名: {}", user1.get_username());
    println!("活跃状态: {}", user1.active);
    println!("登录次数: {}", user1.sign_in_count);

    // 调用方法
    user1.increment_sign_in_count();
    user1.deactivate();

    println!("更新后的登录次数: {}", user1.sign_in_count);
    println!("更新后的活跃状态: {}", user1.active);

    // 使用元组结构体
    let black = Color(0, 0, 0);
    let origin = Point(0, 0);

    println!("黑色 RGB: ({}, {}, {})", black.0, black.1, black.2);
    println!("原点坐标: ({}, {})", origin.0, origin.1);

    // 使用单元结构体
    let subject = AlwaysEqual;
    // 单元结构体通常用于泛型或标记类型
}