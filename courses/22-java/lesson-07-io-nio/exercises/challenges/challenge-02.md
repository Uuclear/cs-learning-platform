# 挑战2：实现高性能文件搜索工具

## 背景
在大型项目中，经常需要在多个文件中搜索特定的文本模式。传统的逐行读取方式在处理大文件时效率较低。

## 要求
1. 创建一个`FileSearcher`类，支持以下功能：
   - 在指定目录及其子目录中递归搜索文件
   - 支持文件扩展名过滤（例如只搜索`.java`和`.txt`文件）
   - 使用NIO的内存映射文件（MappedByteBuffer）提高大文件搜索性能
   - 支持正则表达式匹配
   - 返回包含匹配结果的文件路径和行号

2. 性能优化要求：
   - 对于小文件（<1MB），使用传统的BufferedReader逐行读取
   - 对于大文件（>=1MB），使用FileChannel配合MappedByteBuffer进行内存映射
   - 实现并行搜索，利用多核CPU优势

3. 输出格式：
   ```
   文件路径:行号:匹配内容
   /path/to/file.java:42:public class MyClass {
   ```

4. 编写完整的测试用例：
   - 测试小文件搜索
   - 测试大文件搜索  
   - 测试正则表达式匹配
   - 测试多线程性能对比

## 提示
- 使用`Files.walk()`进行目录遍历
- 使用`Pattern`和`Matcher`进行正则表达式匹配
- 内存映射文件使用`FileChannel.map()`方法
- 注意大文件的内存映射可能受限于虚拟内存大小
- 考虑使用`ForkJoinPool`或`CompletableFuture`实现并行处理