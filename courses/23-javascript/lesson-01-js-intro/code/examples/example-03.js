// example-03.js - 数据类型与 typeof 检查

// Number 类型
let integer = 42;
let float = 3.14;
let negative = -10;
let scientific = 1.23e5; // 1.23 × 10^5

console.log("整数:", integer, "类型:", typeof integer);
console.log("小数:", float, "类型:", typeof float);
console.log("负数:", negative, "类型:", typeof negative);
console.log("科学计数法:", scientific, "类型:", typeof scientific);

// 特殊的数字值
console.log("Infinity:", Infinity, "类型:", typeof Infinity);
console.log("NaN:", NaN, "类型:", typeof NaN); // NaN 表示"不是一个数字"

// String 类型
let singleQuote = '单引号字符串';
let doubleQuote = "双引号字符串";
let templateString = `模板字符串可以包含变量`;

console.log("单引号:", singleQuote, "类型:", typeof singleQuote);
console.log("双引号:", doubleQuote, "类型:", typeof doubleQuote);
console.log("模板字符串:", templateString, "类型:", typeof templateString);

// Boolean 类型
let isTrue = true;
let isFalse = false;

console.log("true:", isTrue, "类型:", typeof isTrue);
console.log("false:", isFalse, "类型:", typeof isFalse);

// Undefined 类型
let undefinedVar;
let explicitlyUndefined = undefined;

console.log("未初始化变量:", undefinedVar, "类型:", typeof undefinedVar);
console.log("显式undefined:", explicitlyUndefined, "类型:", typeof explicitlyUndefined);

// Null 类型
let nullVar = null;
console.log("null值:", nullVar, "类型:", typeof nullVar); // 注意：typeof null 返回 "object"（这是JavaScript的一个历史bug）

// 对象和数组
let person = { name: "李四", age: 30 };
let numbers = [1, 2, 3, 4, 5];

console.log("对象:", person, "类型:", typeof person);
console.log("数组:", numbers, "类型:", typeof numbers); // 数组也是对象

// 使用 Array.isArray() 检查数组
console.log("numbers 是数组吗?", Array.isArray(numbers));
console.log("person 是数组吗?", Array.isArray(person));

// Symbol 类型 (ES6)
let sym1 = Symbol("description");
let sym2 = Symbol("description");

console.log("Symbol 1:", sym1, "类型:", typeof sym1);
console.log("Symbol 2:", sym2, "类型:", typeof sym2);
console.log("两个 Symbol 相等吗?", sym1 === sym2); // false，每个 Symbol 都是唯一的

// 类型转换示例
let numStr = "123";
let actualNum = Number(numStr);
console.log(`"${numStr}" 转换为数字:`, actualNum, "类型:", typeof actualNum);

let boolStr = "true";
let actualBool = Boolean(boolStr);
console.log(`"${boolStr}" 转换为布尔值:`, actualBool, "类型:", typeof actualBool);

// 空字符串转换为布尔值是 false
console.log('空字符串 "" 转换为布尔值:', Boolean(""), "类型:", typeof Boolean(""));