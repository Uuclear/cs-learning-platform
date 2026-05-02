package main

import (
    "context"
    "fmt"
    "net/http"
    "sync"
    "time"
)

// HTTPResult HTTP请求结果
type HTTPResult struct {
    URL     string
    Status  int
    Body    string
    Error   error
    Success bool
}

// ConcurrentHTTPClient 并发HTTP客户端
type ConcurrentHTTPClient struct {
    client *http.Client
}

// NewConcurrentHTTPClient 创建新的并发HTTP客户端
func NewConcurrentHTTPClient(timeout time.Duration) *ConcurrentHTTPClient {
    return &ConcurrentHTTPClient{
        client: &http.Client{
            Timeout: timeout,
        },
    }
}

// FetchURLs 并发获取多个URL
func (c *ConcurrentHTTPClient) FetchURLs(ctx context.Context, urls []string) []HTTPResult {
    var results []HTTPResult
    var mu sync.Mutex
    var wg sync.WaitGroup

    // 为每个URL创建goroutine
    for _, url := range urls {
        wg.Add(1)
        go func(u string) {
            defer wg.Done()

            // 创建带超时的子context
            reqCtx, cancel := context.WithTimeout(ctx, 5*time.Second)
            defer cancel()

            req, err := http.NewRequestWithContext(reqCtx, "GET", u, nil)
            if err != nil {
                mu.Lock()
                results = append(results, HTTPResult{
                    URL:     u,
                    Error:   err,
                    Success: false,
                })
                mu.Unlock()
                return
            }

            resp, err := c.client.Do(req)
            if err != nil {
                mu.Lock()
                results = append(results, HTTPResult{
                    URL:     u,
                    Error:   err,
                    Success: false,
                })
                mu.Unlock()
                return
            }
            defer resp.Body.Close()

            // 简单读取响应体（实际项目中可能需要限制读取大小）
            body := fmt.Sprintf("Status: %d, Content-Length: %d", resp.StatusCode, resp.ContentLength)

            mu.Lock()
            results = append(results, HTTPResult{
                URL:     u,
                Status:  resp.StatusCode,
                Body:    body,
                Success: true,
            })
            mu.Unlock()
        }(url)
    }

    wg.Wait()
    return results
}

func main() {
    // 创建客户端，整体超时10秒
    client := NewConcurrentHTTPClient(10 * time.Second)

    // 创建带超时的上下文
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()

    urls := []string{
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://invalid-url-that-will-fail.com",
    }

    results := client.FetchURLs(ctx, urls)

    // 打印结果
    for _, result := range results {
        if result.Success {
            fmt.Printf("✅ %s - %s\n", result.URL, result.Body)
        } else {
            fmt.Printf("❌ %s - 错误: %v\n", result.URL, result.Error)
        }
    }
}