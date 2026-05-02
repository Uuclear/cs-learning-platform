package main

import (
    "fmt"
    "time"
)

func main() {
    ch1 := make(chan string)
    ch2 := make(chan string)

    // 启动两个goroutine，分别向不同的channel发送消息
    go func() {
        time.Sleep(150 * time.Millisecond)
        ch1 <- "来自channel 1的消息"
    }()

    go func() {
        time.Sleep(100 * time.Millisecond)
        ch2 <- "来自channel 2的消息"
    }()

    // 使用select等待多个channel
    for i := 0; i < 2; i++ {
        select {
        case msg1 := <-ch1:
            fmt.Println("收到:", msg1)
        case msg2 := <-ch2:
            fmt.Println("收到:", msg2)
        case <-time.After(200 * time.Millisecond):
            fmt.Println("超时了！")
        }
    }
}