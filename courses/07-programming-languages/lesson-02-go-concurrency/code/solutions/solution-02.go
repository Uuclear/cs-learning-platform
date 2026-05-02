package main

import (
    "fmt"
    "sync"
)

// Task 任务接口
type Task interface {
    Execute() (interface{}, error)
}

// WorkerPool 工作池
type WorkerPool struct {
    tasks    chan Task
    results  chan Result
    workers  int
}

// Result 任务结果
type Result struct {
    Value interface{}
    Error error
}

// NewWorkerPool 创建新的工作池
func NewWorkerPool(workers int) *WorkerPool {
    return &WorkerPool{
        tasks:   make(chan Task),
        results: make(chan Result),
        workers: workers,
    }
}

// Start 启动工作池
func (wp *WorkerPool) Start() {
    var wg sync.WaitGroup

    // 启动worker goroutine
    for i := 0; i < wp.workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for task := range wp.tasks {
                value, err := task.Execute()
                wp.results <- Result{Value: value, Error: err}
            }
        }()
    }

    // 等待所有worker完成并关闭results channel
    go func() {
        wg.Wait()
        close(wp.results)
    }()
}

// Submit 提交任务
func (wp *WorkerPool) Submit(task Task) {
    wp.tasks <- task
}

// Close 关闭任务提交通道
func (wp *WorkerPool) Close() {
    close(wp.tasks)
}

// ProcessTasks 处理任务列表
func (wp *WorkerPool) ProcessTasks(tasks []Task) []Result {
    var results []Result

    // 启动工作池
    wp.Start()

    // 提交所有任务
    for _, task := range tasks {
        wp.Submit(task)
    }

    // 关闭任务提交通道
    wp.Close()

    // 收集所有结果
    for result := range wp.results {
        results = append(results, result)
    }

    return results
}

// 示例任务实现
type NumberTask struct {
    Number int
}

func (t *NumberTask) Execute() (interface{}, error) {
    return t.Number * t.Number, nil
}

func main() {
    // 创建工作池
    pool := NewWorkerPool(3)

    // 创建任务列表
    var tasks []Task
    for i := 1; i <= 5; i++ {
        tasks = append(tasks, &NumberTask{Number: i})
    }

    // 处理任务
    results := pool.ProcessTasks(tasks)

    // 打印结果
    for i, result := range results {
        if result.Error != nil {
            fmt.Printf("任务 %d 失败: %v\n", i+1, result.Error)
        } else {
            fmt.Printf("任务 %d 结果: %v\n", i+1, result.Value)
        }
    }
}