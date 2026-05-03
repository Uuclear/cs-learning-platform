// example-01.js - JavaScript基本类型和类型检测
// 本示例演示JavaScript的基本数据类型和各种类型检测方法

console.log("=== JavaScript 基本数据类型演示 ===");

// 1. 基本类型 (Primitive Types)
console.log("\n1. 基本类型示例:");
const str = "Hello World";        // string
const num = 42;                   // number
const bool = true;                // boolean
const n = null;                   // null
const undef = undefined;          // undefined
const sym = Symbol('id');         // symbol

console.log(`字符串: "${str}" - 类型: ${typeof str}`);
console.log(`数字: ${num} - 类型: ${typeof num}`);
console.log(`布尔值: ${bool} - 类型: ${typeof bool}`);
console.log(`null: ${n} - 类型: ${typeof n}`); // 注意：这是一个历史bug，返回"object"
console.log(`undefined: ${undef} - 类型: ${typeof undef}`);
console.log(`symbol: ${sym.toString()} - 类型: ${typeof sym}`);

// 2. 引用类型 (Reference Types)
console.log("\n2. 引用类型示例:");
const obj = { name: "张三", age: 25 };     // object
const arr = [1, 2, 3, 4, 5];              // array
const func = function() { return "函数"; }; // function

console.log(`对象: ${JSON.stringify(obj)} - typeof: ${typeof obj}`);
console.log(`数组: [${arr}] - typeof: ${typeof arr}, isArray: ${Array.isArray(arr)}`);
console.log(`函数: ${func.toString().substring(0, 20)}... - typeof: ${typeof func}`);

// 3. 类型检测方法对比
console.log("\n3. 类型检测方法对比:");

// 使用 typeof
console.log("使用 typeof 检测:");
console.log(`typeof "hello": ${typeof "hello"}`);
console.log(`typeof 123: ${typeof 123}`);
console.log(`typeof true: ${typeof true}`);
console.log(`typeof null: ${typeof null}`); // 返回 "object" - 这是bug!
console.log(`typeof [1,2,3]: ${typeof [1,2,3]}`); // 返回 "object"

// 使用 Array.isArray()
console.log("\n使用 Array.isArray() 检测数组:");
console.log(`Array.isArray([1,2,3]): ${Array.isArray([1,2,3])}`);
console.log(`Array.isArray({}): ${Array.isArray({})}`);

// 使用 instanceof
console.log("\n使用 instanceof 检测:");
console.log(`[1,2,3] instanceof Array: ${[1,2,3] instanceof Array}`);
console.log(`{} instanceof Object: ${{} instanceof Object}`);
console.log(`"hello" instanceof String: ${"hello" instanceof String}`); // false，因为字面量不是对象

// 最准确的类型检测方法
console.log("\n4. 最准确的类型检测方法 - Object.prototype.toString.call():");

function getTrueType(value) {
    return Object.prototype.toString.call(value).slice(8, -1).toLowerCase();
}

console.log(`getTrueType("hello"): ${getTrueType("hello")}`);
console.log(`getTrueType(123): ${getTrueType(123)}`);
console.log(`getTrueType(true): ${getTrueType(true)}`);
console.log(`getTrueType(null): ${getTrueType(null)}`);
console.log(`getTrueType(undefined): ${getTrueType(undefined)}`);
console.log(`getTrueType([1,2,3]): ${getTrueType([1,2,3])}`);
console.log(`getTrueType({}): ${getTrueType({})}`);
console.log(`getTrueType(new Date()): ${getTrueType(new Date())}`);

console.log("\n=== 示例结束 ===");