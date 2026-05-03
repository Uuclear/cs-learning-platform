// solution-02.js - 示例2的解答：函数声明方式和箭头函数

// 这个解决方案总结了各种函数声明方式的最佳实践和使用场景

/**
 * 函数声明 - 适用于需要函数提升的场景
 * 或者作为主要的函数定义方式
 */
function greet(name) {
    return `你好, ${name}!`;
}

/**
 * 函数表达式 - 适用于将函数作为值传递的场景
 * 或者在条件语句中定义函数
 */
const processUser = function(user) {
    return {
        id: user.id,
        displayName: `${user.firstName} ${user.lastName}`,
        isActive: user.status === 'active'
    };
};

/**
 * 箭头函数 - 适用于简单的回调函数、数组方法等
 * 注意：箭头函数没有自己的this，适合不需要this绑定的场景
 */
const numbers = [1, 2, 3, 4, 5];
const doubled = numbers.map(x => x * 2);
const evens = numbers.filter(x => x % 2 === 0);

console.log("=== 函数声明方式最佳实践 ===");

// 1. 数组方法中的箭头函数
console.log("原数组:", numbers);
console.log("翻倍后:", doubled);
console.log("偶数:", evens);

// 2. 对象方法中的this绑定处理
const counter = {
    count: 0,

    // 普通方法 - this指向counter对象
    increment() {
        this.count++;
        return this.count;
    },

    // 使用箭头函数会丢失this绑定（不推荐用于对象方法）
    // badIncrement: () => {
    //     this.count++; // this指向全局对象，会出错
    // },

    // 正确的方式：如果需要在回调中保持this，使用普通函数或bind
    delayedIncrement(delay) {
        setTimeout(() => {
            this.count++; // 箭头函数继承外层this
            console.log(`延迟增加后计数: ${this.count}`);
        }, delay);
    }
};

console.log("初始计数:", counter.count);
console.log("直接增加:", counter.increment());
counter.delayedIncrement(100); // 异步增加

// 3. 高阶函数示例
function createMultiplier(multiplier) {
    // 返回箭头函数，简洁且不需要this
    return (number) => number * multiplier;
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log("乘以2:", double(5)); // 10
console.log("乘以3:", triple(5)); // 15

// 4. 默认参数和解构
const createUser = ({ name, email, age = 18 } = {}) => ({
    name,
    email,
    age,
    createdAt: new Date().toISOString()
});

const user1 = createUser({ name: "张三", email: "zhang@example.com" });
console.log("创建用户:", user1);

// 5. 错误处理函数
const safeParseJSON = (str) => {
    try {
        return JSON.parse(str);
    } catch (error) {
        console.error("JSON解析失败:", error.message);
        return null;
    }
};

console.log("安全解析成功:", safeParseJSON('{"name":"测试"}'));
console.log("安全解析失败:", safeParseJSON("invalid json"));

// 总结：选择合适的函数声明方式
console.log("\n=== 选择指南 ===");
console.log("1. 函数声明: 主要函数定义，需要提升");
console.log("2. 函数表达式: 条件定义，作为对象属性");
console.log("3. 箭头函数: 简单回调，数组方法，不需要this绑定");
console.log("4. 避免在对象方法中使用箭头函数（除非特意要继承外层this）");

console.log("\n=== 解答结束 ===");