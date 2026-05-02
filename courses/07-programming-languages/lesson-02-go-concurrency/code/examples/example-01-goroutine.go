package main

import (
    "fmt"
    "time"
)

func sayHello(name string) {
    // 模拟一些工作
    time.Sleep(100 * time.Millisecond)
    fmt.Printf("你好, %s!\n", name)
}

func main() {
    // 启动多个goroutine
    go sayHello("小明")
    go sayHello("小红")
    go sayHello("小刚")

    // 等待goroutine完成（实际项目中应该用更优雅的方式）
    time.Sleep(200 * time.Millisecond)
    fmt.Println("主程序结束")
}