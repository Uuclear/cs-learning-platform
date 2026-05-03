// example-01.js - 作用域链和变量提升
// 演示JavaScript的作用域链、词法作用域和变量提升机制

console.log("=== 作用域链和变量提升演示 ===\n");

// 1. 变量提升示例
console.log("1. 变量提升:");
console.log("var声明的变量:", typeof x); // undefined (被提升但未初始化)
var x = "hello";

// let和const的暂时性死区
try {
  console.log("let声明的变量:", y); // ReferenceError!
} catch (e) {
  console.log("访问let变量在声明前:", e.message);
}
let y = "world";

console.log("声明后的let变量:", y); // world

// 2. 函数提升
console.log("\n2. 函数提升:");
hoistedFunction(); // 正常工作！函数声明被完全提升

function hoistedFunction() {
  console.log("这个函数被提升了！");
}

// 函数表达式不会被提升
try {
  notHoisted(); // TypeError!
} catch (e) {
  console.log("函数表达式未被提升:", e.message);
}
const notHoisted = function() {
  console.log("这个不会被提升");
};

// 3. 作用域链示例
console.log("\n3. 作用域链:");

const globalVar = "全局变量";

function outerFunction() {
  const outerVar = "外层变量";

  function innerFunction() {
    const innerVar = "内层变量";

    // 按照作用域链查找变量
    console.log("内层变量:", innerVar);      // 内层作用域
    console.log("外层变量:", outerVar);      // 外层作用域（闭包）
    console.log("全局变量:", globalVar);     // 全局作用域

    // 尝试访问不存在的变量
    try {
      console.log(nonExistentVar);
    } catch (e) {
      console.log("不存在的变量:", e.message);
    }
  }

  return innerFunction;
}

const scopeDemo = outerFunction();
scopeDemo();

// 4. 块级作用域 vs 函数作用域
console.log("\n4. 块级作用域 vs 函数作用域:");

function scopeComparison() {
  if (true) {
    var functionScoped = "函数作用域";    // var是函数作用域
    let blockScoped = "块级作用域";       // let是块级作用域
  }

  console.log("函数作用域变量:", functionScoped); // 可以访问
  try {
    console.log("块级作用域变量:", blockScoped); // ReferenceError!
  } catch (e) {
    console.log("块级变量在块外:", e.message);
  }
}

scopeComparison();