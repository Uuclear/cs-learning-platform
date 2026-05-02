// TypeScript 泛型示例
// 编译命令: tsc example-03-generics.ts

// 泛型函数 - 可以处理多种类型的函数
function identity<T>(arg: T): T {
  return arg;
}

// 泛型数组工具函数
function getFirstElement<T>(arr: T[]): T | undefined {
  return arr.length > 0 ? arr[0] : undefined;
}

function swapElements<T>(arr: T[], index1: number, index2: number): void {
  if (index1 >= 0 && index1 < arr.length && index2 >= 0 && index2 < arr.length) {
    const temp = arr[index1];
    arr[index1] = arr[index2];
    arr[index2] = temp;
  }
}

// 泛型接口
interface KeyValuePair<K, V> {
  key: K;
  value: V;
}

// 泛型类
class Stack<T> {
  private items: T[] = [];

  push(item: T): void {
    this.items.push(item);
  }

  pop(): T | undefined {
    return this.items.pop();
  }

  peek(): T | undefined {
    return this.items[this.items.length - 1];
  }

  isEmpty(): boolean {
    return this.items.length === 0;
  }

  size(): number {
    return this.items.length;
  }

  clear(): void {
    this.items = [];
  }
}

// 使用泛型函数
const stringResult = identity<string>("Hello TypeScript!");
const numberResult = identity<number>(42);
const booleanResult = identity<boolean>(true);

console.log("泛型函数结果:");
console.log(`字符串: ${stringResult}`);
console.log(`数字: ${numberResult}`);
console.log(`布尔值: ${booleanResult}`);
console.log("---");

// 使用泛型数组工具
const numbers = [1, 2, 3, 4, 5];
const fruits = ["苹果", "香蕉", "橙子"];

console.log("数组工具函数:");
console.log(`数字数组第一个元素: ${getFirstElement(numbers)}`);
console.log(`水果数组第一个元素: ${getFirstElement(fruits)}`);

swapElements(fruits, 0, 2);
console.log(`交换后水果数组: ${fruits}`);
console.log("---");

// 使用泛型接口
const stringNumberPair: KeyValuePair<string, number> = {
  key: "年龄",
  value: 25
};

const numberStringPair: KeyValuePair<number, string> = {
  key: 1,
  value: "第一名"
};

console.log("泛型接口:");
console.log(`键值对1: ${stringNumberPair.key} = ${stringNumberPair.value}`);
console.log(`键值对2: ${numberStringPair.key} = ${numberStringPair.value}`);
console.log("---");

// 使用泛型类
const numberStack = new Stack<number>();
numberStack.push(1);
numberStack.push(2);
numberStack.push(3);

console.log("泛型栈:");
console.log(`栈顶元素: ${numberStack.peek()}`);
console.log(`栈大小: ${numberStack.size()}`);
console.log(`弹出元素: ${numberStack.pop()}`);
console.log(`弹出后栈大小: ${numberStack.size()}`);

const stringStack = new Stack<string>();
stringStack.push("TypeScript");
stringStack.push("JavaScript");
stringStack.push("Python");

console.log(`字符串栈顶: ${stringStack.peek()}`);
while (!stringStack.isEmpty()) {
  console.log(`弹出: ${stringStack.pop()}`);
}