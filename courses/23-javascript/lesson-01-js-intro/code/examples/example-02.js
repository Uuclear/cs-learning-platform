// example-02.js - 变量声明与基本运算

// 使用 let 声明变量（可以重新赋值）
let message = "初始消息";
console.log("初始值:", message);

message = "更新后的消息";
console.log("更新后:", message);

// 使用 const 声明常量（不能重新赋值）
const PI = 3.14159;
const appName = "我的第一个应用";
console.log("PI =", PI);
console.log("应用名称:", appName);

// 基本算术运算
let a = 10;
let b = 3;

console.log("a + b =", a + b); // 加法
console.log("a - b =", a - b); // 减法
console.log("a * b =", a * b); // 乘法
console.log("a / b =", a / b); // 除法
console.log("a % b =", a % b); // 取余
console.log("a ** b =", a ** b); // 幂运算

// 字符串拼接
let firstName = "张";
let lastName = "三";
let fullName = firstName + lastName;
console.log("全名:", fullName);

// 布尔运算
let isAdult = true;
let hasLicense = false;

console.log("isAdult && hasLicense =", isAdult && hasLicense); // 逻辑与
console.log("isAdult || hasLicense =", isAdult || hasLicense); // 逻辑或
console.log("!isAdult =", !isAdult); // 逻辑非

// 复合赋值运算符
let counter = 0;
counter += 5; // 等同于 counter = counter + 5
console.log("counter =", counter);

counter *= 2; // 等同于 counter = counter * 2
console.log("counter =", counter);