// TypeScript 基本类型示例
// 编译命令: tsc example-01-basic-types.ts

// 基本类型声明
let name: string = "张三";        // 字符串类型
let age: number = 25;            // 数字类型（包括整数和浮点数）
let isStudent: boolean = true;   // 布尔类型
let hobbies: string[] = ["读书", "编程", "游泳"];  // 字符串数组
let scores: Array<number> = [95, 87, 92];         // 数字数组的另一种写法

// 联合类型 - 变量可以是多种类型之一
let id: string | number = "TS001";  // 可以是字符串或数字
id = 123;  // 现在赋值为数字也是合法的

// 元组类型 - 固定长度和类型的数组
let person: [string, number, boolean] = ["李四", 30, false];

// 枚举类型 - 定义命名的常量集合
enum Color {
  Red = 1,
  Green = 2,
  Blue = 3
}
let favoriteColor: Color = Color.Blue;

// void 类型 - 表示没有任何类型，通常用于函数返回值
function sayHello(): void {
  console.log("你好，TypeScript！");
}

// null 和 undefined 类型
let u: undefined = undefined;
let n: null = null;

// any 类型 - 跳过类型检查（谨慎使用！）
let anything: any = "这可以是任何类型";
anything = 42;
anything = true;

// 使用函数
function introduce(personName: string, personAge: number): string {
  return `大家好，我是${personName}，今年${personAge}岁。`;
}

// 调用函数并输出结果
console.log(introduce(name, age));
console.log(`爱好: ${hobbies.join(", ")}`);
console.log(`成绩: ${scores}`);
console.log(`ID: ${id}`);
console.log(`人员信息: ${person}`);
console.log(`最喜欢的颜色: ${favoriteColor}`);
sayHello();