// example-02.js - 函数声明方式和箭头函数
// 本示例演示JavaScript中各种函数声明方式的区别和使用场景

console.log("=== JavaScript 函数声明方式演示 ===");

// 1. 函数声明 (Function Declaration)
// 特点：函数提升（hoisting），可以在声明前调用
console.log("\n1. 函数声明:");
console.log(hoistedFunction()); // 可以在声明前调用

function hoistedFunction() {
    return "这是通过函数声明创建的函数";
}

console.log(hoistedFunction());

// 2. 函数表达式 (Function Expression)
// 特点：没有函数提升，必须在声明后才能调用
console.log("\n2. 函数表达式:");

// console.log(notHoisted()); // 这会报错！Cannot access 'notHoisted' before initialization

const notHoisted = function() {
    return "这是通过函数表达式创建的函数";
};

console.log(notHoisted());

// 命名函数表达式
const namedFuncExpr = function myName() {
    return `这是命名函数表达式，函数名是: ${myName.name}`;
};

console.log(namedFuncExpr());

// 3. 箭头函数 (Arrow Function)
// 特点：简洁语法，没有自己的this、arguments、super、new.target
console.log("\n3. 箭头函数:");

// 基本语法
const add = (a, b) => a + b;
const square = x => x * x; // 单参数可以省略括号
const sayHello = () => "你好！"; // 无参数需要括号

console.log(`add(5, 3) = ${add(5, 3)}`);
console.log(`square(4) = ${square(4)}`);
console.log(sayHello());

// 多行箭头函数
const multiLineArrow = (name) => {
    const greeting = `你好, ${name}!`;
    const time = new Date().toLocaleTimeString();
    return `${greeting} 现在时间是: ${time}`;
};

console.log(multiLineArrow("小明"));

// 4. this绑定的区别
console.log("\n4. this绑定的区别:");

const obj = {
    name: "张三",

    // 普通方法 - this指向调用对象
    regularMethod: function() {
        return `普通方法中的this.name: ${this.name}`;
    },

    // 箭头函数方法 - this指向定义时的上下文（这里是全局对象）
    arrowMethod: () => {
        return `箭头函数中的this.name: ${this.name}`; // this.name 是 undefined
    },

    // 在方法内部使用箭头函数
    methodWithArrow: function() {
        const innerArrow = () => {
            return `方法内部箭头函数的this.name: ${this.name}`; // 继承外层this
        };
        return innerArrow();
    }
};

console.log(obj.regularMethod());
console.log(obj.arrowMethod());
console.log(obj.methodWithArrow());

// 5. 构造函数 vs 箭头函数
console.log("\n5. 构造函数能力:");

// 普通函数可以用作构造函数
function Person(name, age) {
    this.name = name;
    this.age = age;
}

const person1 = new Person("李四", 30);
console.log(`Person实例: ${person1.name}, ${person1.age}`);

// 箭头函数不能用作构造函数
const ArrowPerson = (name, age) => {
    // 这里不能使用this，也不能用new调用
    return { name, age };
};

const person2 = ArrowPerson("王五", 25);
console.log(`ArrowPerson返回: ${person2.name}, ${person2.age}`);

// 尝试用new调用箭头函数会报错
// const person3 = new ArrowPerson("赵六", 35); // TypeError: ArrowPerson is not a constructor

// 6. 参数处理
console.log("\n6. 参数处理:");

// 普通函数有arguments对象
function withArguments() {
    console.log(`arguments对象:`, Array.from(arguments));
    return arguments.length;
}

console.log(`withArguments(1, 2, 3) 返回参数个数: ${withArguments(1, 2, 3)}`);

// 箭头函数没有arguments，但可以用rest参数
const withRest = (...args) => {
    console.log(`rest参数:`, args);
    return args.length;
};

console.log(`withRest(4, 5, 6, 7) 返回参数个数: ${withRest(4, 5, 6, 7)}`);

console.log("\n=== 示例结束 ===");