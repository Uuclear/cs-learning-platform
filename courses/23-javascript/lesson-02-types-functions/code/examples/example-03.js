// example-03.js - 值类型vs引用类型的区别
// 本示例演示JavaScript中值类型（基本类型）和引用类型（对象类型）在赋值和传递时的区别

console.log("=== 值类型 vs 引用类型演示 ===");

// 1. 值类型（基本类型）- 按值传递
console.log("\n1. 值类型（基本类型）演示:");

let primitive1 = 10;
let primitive2 = primitive1; // 复制值

console.log(`初始值: primitive1 = ${primitive1}, primitive2 = ${primitive2}`);

primitive2 = 20; // 修改primitive2

console.log(`修改后: primitive1 = ${primitive1}, primitive2 = ${primitive2}`);
console.log("结论：修改primitive2不会影响primitive1，因为它们是独立的值");

// 字符串示例
let str1 = "Hello";
let str2 = str1;
str2 = str2 + " World";

console.log(`\n字符串示例:`);
console.log(`str1 = "${str1}"`);
console.log(`str2 = "${str2}"`);

// 2. 引用类型（对象类型）- 按引用传递
console.log("\n2. 引用类型（对象类型）演示:");

let obj1 = { name: "张三", age: 25 };
let obj2 = obj1; // 复制引用（指向同一个对象）

console.log(`初始对象: obj1 = ${JSON.stringify(obj1)}, obj2 = ${JSON.stringify(obj2)}`);

obj2.name = "李四"; // 通过obj2修改对象

console.log(`修改后: obj1 = ${JSON.stringify(obj1)}, obj2 = ${JSON.stringify(obj2)}`);
console.log("结论：修改obj2会影响obj1，因为它们指向同一个对象");

// 数组示例
let arr1 = [1, 2, 3];
let arr2 = arr1;
arr2.push(4);

console.log(`\n数组示例:`);
console.log(`arr1 = [${arr1}]`);
console.log(`arr2 = [${arr2}]`);

// 3. 函数参数传递
console.log("\n3. 函数参数传递演示:");

// 值类型参数
function modifyPrimitive(value) {
    console.log(`函数内修改前: value = ${value}`);
    value = 100;
    console.log(`函数内修改后: value = ${value}`);
    return value;
}

let num = 50;
console.log(`\n调用modifyPrimitive前: num = ${num}`);
let result = modifyPrimitive(num);
console.log(`调用modifyPrimitive后: num = ${num}, 返回值 = ${result}`);

// 引用类型参数
function modifyObject(obj) {
    console.log(`函数内修改前: obj.name = ${obj.name}`);
    obj.name = "王五";
    console.log(`函数内修改后: obj.name = ${obj.name}`);

    // 如果重新赋值整个对象，不会影响外部
    obj = { name: "新对象" };
    console.log(`函数内重新赋值后: obj.name = ${obj.name}`);
}

let person = { name: "赵六" };
console.log(`\n调用modifyObject前: person.name = ${person.name}`);
modifyObject(person);
console.log(`调用modifyObject后: person.name = ${person.name}`);

// 4. 如何避免引用类型的意外修改（深拷贝 vs 浅拷贝）
console.log("\n4. 避免引用类型意外修改:");

// 浅拷贝示例
let original = {
    name: "原始对象",
    details: {
        city: "北京",
        hobbies: ["读书", "游泳"]
    }
};

// 使用展开运算符进行浅拷贝
let shallowCopy = { ...original };
shallowCopy.name = "浅拷贝对象"; // 这不会影响原对象
shallowCopy.details.city = "上海"; // 这会影响原对象！

console.log(`浅拷贝结果:`);
console.log(`original.details.city = ${original.details.city}`); // "上海"
console.log(`shallowCopy.details.city = ${shallowCopy.details.city}`); // "上海"

// 深拷贝示例（简单版本）
function deepClone(obj) {
    if (obj === null || typeof obj !== "object") {
        return obj;
    }

    if (Array.isArray(obj)) {
        return obj.map(item => deepClone(item));
    }

    const cloned = {};
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            cloned[key] = deepClone(obj[key]);
        }
    }
    return cloned;
}

let deepOriginal = {
    name: "深度原始",
    details: {
        city: "广州",
        hobbies: ["电影", "音乐"]
    }
};

let deepCopy = deepClone(deepOriginal);
deepCopy.details.city = "深圳";

console.log(`\n深拷贝结果:`);
console.log(`deepOriginal.details.city = ${deepOriginal.details.city}`); // "广州"
console.log(`deepCopy.details.city = ${deepCopy.details.city}`); // "深圳"

// 5. 实际应用中的注意事项
console.log("\n5. 实际应用建议:");

// 错误的做法：直接修改传入的对象
function badFunction(config) {
    config.newProperty = "添加的属性";
    return config;
}

// 正确的做法：创建新对象
function goodFunction(config) {
    return {
        ...config,
        newProperty: "添加的属性"
    };
}

let inputConfig = { theme: "dark" };
// let badResult = badFunction(inputConfig); // 这会修改inputConfig！
let goodResult = goodFunction(inputConfig);

console.log(`输入配置: ${JSON.stringify(inputConfig)}`);
console.log(`正确结果: ${JSON.stringify(goodResult)}`);

console.log("\n=== 示例结束 ===");