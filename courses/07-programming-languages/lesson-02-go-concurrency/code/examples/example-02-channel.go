package main

import "fmt"

func worker(id int, jobs <-chan int, results chan<- int) {
    // 从jobs channel接收任务，处理后发送到results channel
    for job := range jobs {
        fmt.Printf("工人 %d 正在处理任务 %d\n", id, job)
        results <- job * 2 // 简单的处理：乘以2
    }
}

func main() {
    const numJobs = 5
    jobs := make(chan int, numJobs)   // 有缓冲的jobs channel
    results := make(chan int, numJobs) // 有缓冲的results channel

    // 启动3个worker goroutine
    for w := 1; w <= 3; w++ {
        go worker(w, jobs, results)
    }

    // 发送任务
    for j := 1; j <= numJobs; j++ {
        jobs <- j
    }
    close(jobs) // 关闭jobs channel，告诉workers没有更多任务了

    // 收集结果
    for a := 1; a <= numJobs; a++ {
        result := <-results
        fmt.Printf("收到结果: %d\n", result)
    }
}