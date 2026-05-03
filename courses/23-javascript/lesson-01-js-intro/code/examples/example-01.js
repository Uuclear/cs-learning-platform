// example-01.js - Hello World 与 console.log 调试

// 最简单的Hello World
console.log("Hello, JavaScript!");

// 输出不同类型的值
console.log("这是一个字符串");
console.log(42); // 这是一个数字
console.log(true); // 这是一个布尔值
console.log(null); // 这是空值
console.log(undefined); // 这是未定义

// 使用模板字符串输出多个值
const name = "小明";
const age = 18;
console.log(`你好，${name}！你今年${age}岁了。`);

// 输出对象和数组
console.log({ name: "张三", score: 95 });
console.log([1, 2, 3, 4, 5]);

// 调试技巧：给输出添加标签
console.log("调试信息:", "程序执行到这里了");
console.log("变量值:", { name, age });