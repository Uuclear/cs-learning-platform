// solution-01.js - 示例1的解答：JavaScript基本类型和类型检测

// 这个解决方案提供了一个更完善的类型检测函数
// 能够准确识别所有JavaScript数据类型

/**
 * 准确检测JavaScript数据类型的函数
 * @param {*} value - 要检测的值
 * @returns {string} - 数据类型名称
 */
function accurateTypeOf(value) {
    // 处理null特殊情况
    if (value === null) {
        return 'null';
    }

    // 使用Object.prototype.toString获取准确类型
    const typeString = Object.prototype.toString.call(value);
    // 提取类型名称（去掉[object 和 ]）
    return typeString.slice(8, -1).toLowerCase();
}

// 测试函数
console.log("=== 准确类型检测函数测试 ===");

// 基本类型测试
console.log(`accurateTypeOf("hello"): ${accurateTypeOf("hello")}`); // string
console.log(`accurateTypeOf(42): ${accurateTypeOf(42)}`); // number
console.log(`accurateTypeOf(true): ${accurateTypeOf(true)}`); // boolean
console.log(`accurateTypeOf(null): ${accurateTypeOf(null)}`); // null
console.log(`accurateTypeOf(undefined): ${accurateTypeOf(undefined)}`); // undefined
console.log(`accurateTypeOf(Symbol('id')): ${accurateTypeOf(Symbol('id'))}`); // symbol

// 引用类型测试
console.log(`accurateTypeOf([1,2,3]): ${accurateTypeOf([1,2,3])}`); // array
console.log(`accurateTypeOf({}): ${accurateTypeOf({})}`); // object
console.log(`accurateTypeOf(function(){}): ${accurateTypeOf(function(){})}`); // function
console.log(`accurateTypeOf(new Date()): ${accurateTypeOf(new Date())}`); // date
console.log(`accurateTypeOf(/regex/): ${accurateTypeOf(/regex/)}`); // regexp

// 与typeof对比
console.log("\n=== 与typeof对比 ===");
const testValues = [null, [1,2,3], new Date(), /regex/];

testValues.forEach(value => {
    console.log(`值: ${value}`);
    console.log(`  typeof: ${typeof value}`);
    console.log(`  accurateTypeOf: ${accurateTypeOf(value)}`);
});

console.log("\n=== 解答结束 ===");