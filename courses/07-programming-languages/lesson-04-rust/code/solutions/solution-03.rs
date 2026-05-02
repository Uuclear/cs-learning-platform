// solution-03.rs
// 练习3解答：实现自定义智能指针

use std::ops::Deref;

struct MyBox<T> {
    ptr: *const T,
}

impl<T> MyBox<T> {
    fn new(x: T) -> MyBox<T> {
        // 在堆上分配内存并获取原始指针
        let boxed = Box::new(x);
        MyBox {
            ptr: Box::into_raw(boxed),
        }
    }
}

impl<T> Deref for MyBox<T> {
    type Target = T;

    fn deref(&self) -> &Self::Target {
        unsafe { &*self.ptr }
    }
}

impl<T> Drop for MyBox<T> {
    fn drop(&mut self) {
        // 安全地释放内存
        unsafe {
            let _ = Box::from_raw(self.ptr as *mut T);
        }
    }
}

fn main() {
    let x = 5;
    let y = MyBox::new(x);

    // 由于实现了Deref，可以直接像引用一样使用
    assert_eq!(5, *y);

    println!("MyBox包含的值: {}", *y);
    println!("MyBox地址: {:p}", y.ptr);

    // 当y离开作用域时，Drop trait会自动调用，释放内存
}