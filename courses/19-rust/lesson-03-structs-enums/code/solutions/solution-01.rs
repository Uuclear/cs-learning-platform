// solution-01.rs - 结构体练习解决方案

// 定义 Book 结构体
struct Book {
    title: String,
    author: String,
    pages: u32,
    is_borrowed: bool,
}

impl Book {
    fn new(title: String, author: String, pages: u32) -> Book {
        Book {
            title,
            author,
            pages,
            is_borrowed: false,
        }
    }

    fn borrow(&mut self) {
        if !self.is_borrowed {
            self.is_borrowed = true;
            println!("成功借阅《{}》", self.title);
        } else {
            println!("《{}》已被借出", self.title);
        }
    }

    fn return_book(&mut self) {
        if self.is_borrowed {
            self.is_borrowed = false;
            println!("成功归还《{}》", self.title);
        } else {
            println!("《{}》未被借出", self.title);
        }
    }

    fn get_info(&self) -> String {
        format!(
            "书名: {}, 作者: {}, 页数: {}, 状态: {}",
            self.title,
            self.author,
            self.pages,
            if self.is_borrowed { "已借出" } else { "可借阅" }
        )
    }
}

// 元组结构体用于表示坐标
struct Coordinate(f64, f64);

impl Coordinate {
    fn new(x: f64, y: f64) -> Coordinate {
        Coordinate(x, y)
    }

    fn distance_from_origin(&self) -> f64 {
        (self.0.powi(2) + self.1.powi(2)).sqrt()
    }
}

fn main() {
    // 测试 Book 结构体
    let mut book = Book::new(
        String::from("Rust编程之道"),
        String::from("张三"),
        300
    );

    println!("{}", book.get_info());
    book.borrow();
    println!("{}", book.get_info());
    book.borrow(); // 尝试重复借阅
    book.return_book();
    println!("{}", book.get_info());

    // 测试 Coordinate 结构体
    let point = Coordinate::new(3.0, 4.0);
    println!("点 ({}, {}) 到原点的距离: {}", point.0, point.1, point.distance_from_origin());
}