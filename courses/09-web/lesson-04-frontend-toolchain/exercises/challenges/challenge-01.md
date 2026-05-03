# 挑战 1：实现自定义 Webpack Loader ⭐⭐⭐

## 背景
你正在为一个团队开发项目，需要处理一种特殊的文件格式 `.greet`，这种文件包含简单的问候语模板。

## 要求
创建一个 Webpack loader，能够将 `.greet` 文件转换为可执行的 JavaScript 函数。

### .greet 文件格式
```
name: {name}
message: 欢迎来到 {course} 课程！
signature: - {instructor}
```

### 预期输出
loader 应该将上述内容转换为：
```javascript
module.exports = function greet(data) {
  const { name, course, instructor } = data;
  return `欢迎来到 ${course} 课程！\n- ${instructor}`;
};
```

## 实现步骤
1. 创建 `greet-loader.js` 文件
2. 实现 loader 函数，解析 `.greet` 文件内容
3. 提取模板变量（花括号中的内容）
4. 生成对应的 JavaScript 函数代码
5. 在 Webpack 配置中注册这个 loader

## 测试用例
创建一个测试文件 `test.greet`：
```
name: 学生
message: 欢迎学习 {title}！今天是 {date}。
signature: - {teacher}
```

预期使用方式：
```javascript
const greet = require('./test.greet');
console.log(greet({ 
  title: '前端工具链', 
  date: '2026-05-03', 
  teacher: 'CS教授' 
}));
```

## 提示
- 使用正则表达式提取花括号中的变量名
- 注意处理多行内容
- 确保生成的 JavaScript 语法正确
- 考虑错误处理（如无效的 .greet 文件格式）

## 扩展思考
- 如何支持嵌套对象参数？
- 如何添加缓存机制提高性能？
- 如何与其他 loader 链式调用？