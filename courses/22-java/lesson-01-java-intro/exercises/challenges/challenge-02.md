# 挑战 2：环境信息显示程序

## 目标
创建一个 Java 程序，能够显示当前 Java 运行环境的详细信息。

## 要求
1. 程序名为 `EnvironmentInfo.java`
2. 程序不需要命令行参数，直接运行即可
3. 显示以下系统属性信息：
   - Java 版本 (`java.version`)
   - Java 供应商 (`java.vendor`)
   - 操作系统名称 (`os.name`)
   - 操作系统版本 (`os.version`)
   - 操作系统架构 (`os.arch`)
   - 用户名 (`user.name`)
   - 当前工作目录 (`user.dir`)
4. 使用美观的格式输出，每项信息占一行
5. 在输出前后添加分隔线

## 示例输出

```
========================================
         Java 环境信息
========================================
Java 版本:     17.0.8
Java 供应商:   Oracle Corporation
操作系统:      Mac OS X
系统版本:      14.5
系统架构:      aarch64
用户名:        slouch
工作目录:      /Users/slouch/Documents/learn/courses
========================================
```

## 提示
- 使用 `System.getProperty()` 方法获取系统属性
- 可以使用 `System.out.printf()` 进行格式化输出
- 注意处理可能为空的属性值（虽然这些基本属性通常不会为空）

## 扩展挑战（可选）
- 添加 JVM 内存信息（最大内存、已用内存等）
- 显示可用处理器数量 (`Runtime.getRuntime().availableProcessors()`)
- 将输出保存到文件 `env_info.txt` 中
- 支持通过命令行参数选择要显示的信息类别

## 学习要点
通过这个挑战，你将学习到：
- 如何获取系统和 JVM 的运行时信息
- Java 的系统属性机制
- 字符串格式化输出
- 程序的自省能力（程序了解自己的运行环境）