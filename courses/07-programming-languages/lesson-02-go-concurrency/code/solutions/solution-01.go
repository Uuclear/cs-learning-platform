package main

import (
    "sync"
)

// Counter 并发安全的计数器
type Counter struct {
    mu sync.Mutex
    value int
}

// Increment 增加计数器值
func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value++
}

// Decrement 减少计数器值
func (c *Counter) Decrement() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.value--
}

// Value 获取当前计数器值
func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.value
}