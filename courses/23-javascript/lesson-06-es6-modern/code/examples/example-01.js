// example-01.js - 解构赋值和展开运算符
// 解构就像拆快递：把包裹里的东西直接拿出来用，不用一层层打开

console.log("=== 数组解构 ===");
// 基础数组解构
const fruits = ['苹果', '香蕉', '橙子'];
const [first, second, third] = fruits;
console.log(`第一个水果: ${first}`); // 苹果
console.log(`第二个水果: ${second}`); // 香蕉

// 跳过元素（用逗号占位）
const [,,orange] = fruits;
console.log(`第三个水果: ${orange}`); // 橙子

// 默认值（像备胎一样，主选没有就用备选）
const [a, b, c, d = '葡萄'] = fruits;
console.log(`第四个水果(默认值): ${d}`); // 葡萄

console.log("\n=== 对象解构 ===");
// 对象解构 - 直接从对象中提取属性
const student = {
  name: '小明',
  age: 20,
  grade: '大二',
  hobby: '编程'
};

// 基础解构
const { name, age, grade } = student;
console.log(`学生信息: ${name}, ${age}岁, ${grade}`);

// 重命名属性（就像给朋友起外号）
const { name: nickname, hobby: interest } = student;
console.log(`昵称: ${nickname}, 兴趣: ${interest}`);

// 默认值 + 重命名
const { email = '未提供邮箱', phone = '未提供电话' } = student;
console.log(`联系方式: ${email}, ${phone}`);

console.log("\n=== 展开运算符 (...) ===");
// 展开运算符就像拼积木：把现有的积木块拆开，和其他积木重新组合

// 数组展开
const numbers1 = [1, 2, 3];
const numbers2 = [4, 5, 6];
const combinedNumbers = [...numbers1, ...numbers2, 7, 8];
console.log('合并数组:', combinedNumbers); // [1, 2, 3, 4, 5, 6, 7, 8]

// 对象展开（浅拷贝）
const originalConfig = { theme: 'dark', language: 'zh-CN' };
const newConfig = { ...originalConfig, theme: 'light', version: '2.0' };
console.log('新配置:', newConfig); // { theme: 'light', language: 'zh-CN', version: '2.0' }

console.log("\n=== 剩余参数 (...args) ===");
// 剩余参数收集所有额外参数，像收件箱一样收集所有邮件

function sumAll(...numbers) {
  return numbers.reduce((total, num) => total + num, 0);
}

console.log('求和结果:', sumAll(1, 2, 3, 4, 5)); // 15

// 结合解构使用剩余参数
const [head, ...rest] = [10, 20, 30, 40, 50];
console.log(`第一个元素: ${head}`); // 10
console.log('剩余元素:', rest); // [20, 30, 40, 50]

const { name: studentName, ...otherInfo } = student;
console.log(`学生姓名: ${studentName}`);
console.log('其他信息:', otherInfo); // { age: 20, grade: '大二', hobby: '编程' }