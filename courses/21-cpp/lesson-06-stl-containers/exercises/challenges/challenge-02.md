# 挑战2：高性能词频分析器

## 背景
你正在开发一个文本分析工具，需要高效处理大量文本数据并生成详细的词频统计报告。

## 要求
实现一个高性能的词频分析器，能够处理多种文本格式并提供丰富的分析功能。

### 核心功能
1. **基础词频统计**：
   - 读取文本文件（支持.txt格式）
   - 统计每个单词的出现频率
   - 忽略大小写和标点符号
   - 支持自定义停用词列表（如"the", "a", "an", "and"等）

2. **容器选择优化**：
   - 实现两个版本：一个使用`std::map`，另一个使用`std::unordered_map`
   - 比较两种实现的性能差异（处理时间、内存使用）
   - 根据输入数据大小自动选择最优容器

3. **高级分析功能**：
   - 找出最常用的N个单词（N可配置）
   - 找出只出现一次的单词（独特词汇）
   - 计算词汇多样性（不同单词数/总单词数）
   - 生成按频率排序的词汇表

4. **输出格式**：
   - 控制台输出基本统计信息
   - 生成CSV文件包含详细词频数据
   - 生成HTML报告包含可视化图表（可选）

### 性能要求
- 能够处理至少10MB的文本文件
- 处理时间不超过30秒（在普通笔记本电脑上）
- 内存使用合理，避免不必要的拷贝

### 数据结构设计建议
```cpp
class WordFrequencyAnalyzer {
private:
    // 主要数据存储
    std::unordered_map<std::string, int> wordCount_;
    
    // 停用词集合（用于快速查找）
    std::unordered_set<std::string> stopWords_;
    
    // 统计信息
    size_t totalWords_ = 0;
    size_t uniqueWords_ = 0;
    
public:
    // 核心方法
    void loadText(const std::string& filename);
    void addStopWords(const std::vector<std::string>& words);
    std::vector<std::pair<std::string, int>> getTopWords(size_t n) const;
    std::vector<std::string> getUniqueWords() const;
    double getVocabularyRichness() const;
    void saveToCSV(const std::string& filename) const;
    void generateReport(const std::string& filename) const;
};
```

### 测试场景
1. **小文件测试**：处理几百字的短文，验证功能正确性
2. **大文件测试**：处理几MB的小说或文章，测试性能
3. **边界情况**：空文件、只有标点符号、全是停用词等

### 额外挑战（选做）
- 支持多线程处理多个文件
- 实现增量处理：可以多次添加文本而不重新计算全部
- 添加n-gram分析（二元组、三元组词频）

## 评估标准
- 功能完整性（40%）
- 性能优化（30%）
- 容器选择的合理性（20%）
- 代码质量和文档（10%）

## 参考资源
- C++ STL文档关于map、unordered_map、set、unordered_set的详细说明
- 文本处理的最佳实践（字符串处理、内存管理）
- 性能分析工具（如chrono库进行时间测量）