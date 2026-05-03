# 挑战 2：高效文本处理器

## 背景
你正在开发一个日志分析工具，需要处理大量的文本数据。性能和内存使用是关键考虑因素。

## 任务
实现一个高效的文本处理器，使用 `std::string_view` 和其他现代 C++ 特性。

## 功能要求

### 1. 文本分割器
实现一个函数，能够将文本按指定分隔符分割：
```cpp
std::vector<std::string_view> split(std::string_view text, std::string_view delimiter);
```

### 2. 安全类型转换
实现安全的字符串到数值转换函数：
```cpp
std::optional<int> toInt(std::string_view str);
std::optional<double> toDouble(std::string_view str);
```

### 3. 文本分析器
实现一个文本分析器，能够：
- 统计单词数量
- 找出最长和最短的单词
- 提取所有数字并计算总和
- 识别重复的单词

### 4. 高效的文件处理模拟
创建一个模拟函数，处理大量文本数据而不产生不必要的内存分配：
```cpp
struct TextStats {
    size_t totalChars;
    size_t totalWords;
    size_t numericValues;
    double sumOfNumbers;
};

TextStats analyzeLargeText(const std::vector<std::string>& largeTexts);
```

## 性能要求
- 避免不必要的字符串复制
- 使用 `std::string_view` 进行零拷贝操作
- 合理使用 `std::optional` 处理转换失败
- 使用结构化绑定简化代码

## 示例用法
```cpp
int main() {
    std::string logData = "ERROR: User login failed at 2026-05-03 14:30:45. Attempts: 3";
    
    // 分割日志
    auto parts = split(logData, " ");
    for (const auto& part : parts) {
        std::cout << "[" << part << "] ";
    }
    std::cout << std::endl;
    
    // 提取数字
    for (const auto& part : parts) {
        if (auto num = toInt(part)) {
            std::cout << "找到数字: " << *num << std::endl;
        }
    }
    
    // 分析大量数据
    std::vector<std::string> logs = {
        "INFO: Server started successfully",
        "WARN: Memory usage at 85%",
        "ERROR: Database connection timeout after 30 seconds",
        "DEBUG: Processing request ID 12345 with 42 parameters"
    };
    
    auto stats = analyzeLargeText(logs);
    std::cout << "分析结果: " << stats.totalWords << " 个单词, "
              << stats.sumOfNumbers << " 数字总和" << std::endl;
    
    return 0;
}
```

## 验收标准
- 代码正确处理各种边界情况
- 性能优于传统的字符串处理方式
- 充分利用现代 C++ 特性
- 代码简洁、安全、高效
- 包含适当的错误处理