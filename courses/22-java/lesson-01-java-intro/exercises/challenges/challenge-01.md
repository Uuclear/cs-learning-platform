# 挑战 1：个性化问候程序

## 目标
创建一个 Java 程序，能够根据用户输入的姓名和年龄，输出个性化的问候信息。

## 要求
1. 程序名为 `PersonalGreeting.java`
2. 使用命令行参数接收用户的姓名和年龄
3. 输出格式为：`你好，[姓名]！你今年 [年龄] 岁，欢迎学习 Java 编程！`
4. 如果没有提供足够的参数，显示使用说明
5. 对年龄参数进行有效性验证（必须是正整数）

## 示例运行

```bash
# 正常情况
$ java PersonalGreeting 张三 25
你好，张三！你今年 25 岁，欢迎学习 Java 编程！

# 参数不足
$ java PersonalGreeting 张三
用法: java PersonalGreeting <姓名> <年龄>

# 年龄无效
$ java PersonalGreeting 张三 abc
错误: 年龄必须是有效的正整数！
```

## 提示
- 参考 Example03.java 中的命令行参数处理
- 使用 `Integer.parseInt()` 将字符串转换为整数
- 使用 try-catch 处理 NumberFormatException 异常
- 验证年龄是否为正数

## 扩展挑战（可选）
- 添加对负数年龄的检查
- 支持中文姓名中的空格（如 "张 小三"）
- 根据年龄显示不同的问候语（如年轻人、中年人、老年人）