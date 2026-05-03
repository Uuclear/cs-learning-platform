// solution-01.js - ES Modules 解决方案
// 这是练习1的完整解决方案

// mathUtils.js
export function add(a, b) {
  return a + b;
}

export function subtract(a, b) {
  return a - b;
}

export function multiply(a, b) {
  return a * b;
}

export function divide(a, b) {
  if (b === 0) {
    throw new Error('除数不能为零');
  }
  return a / b;
}

// 默认导出一个计算器对象
export default class Calculator {
  constructor() {
    this.history = [];
  }

  calculate(operation, a, b) {
    let result;
    switch (operation) {
      case 'add':
        result = add(a, b);
        break;
      case 'subtract':
        result = subtract(a, b);
        break;
      case 'multiply':
        result = multiply(a, b);
        break;
      case 'divide':
        result = divide(a, b);
        break;
      default:
        throw new Error('不支持的操作');
    }

    const record = { operation, a, b, result, timestamp: new Date() };
    this.history.push(record);
    return result;
  }

  getHistory() {
    return this.history;
  }
}

// main.js
import Calculator, { add, subtract, multiply, divide } from './mathUtils.js';

console.log('=== ES Modules 练习解决方案 ===');

// 使用默认导出的Calculator类
const calc = new Calculator();
console.log('加法:', calc.calculate('add', 10, 5)); // 15
console.log('减法:', calc.calculate('subtract', 10, 5)); // 5
console.log('乘法:', calc.calculate('multiply', 10, 5)); // 50
console.log('除法:', calc.calculate('divide', 10, 5)); // 2

console.log('\n计算历史:');
calc.getHistory().forEach((record, index) => {
  console.log(`${index + 1}. ${record.a} ${record.operation} ${record.b} = ${record.result}`);
});

// 直接使用命名导出的函数
console.log('\n直接使用函数:');
console.log('add(3, 7) =', add(3, 7));
console.log('multiply(4, 6) =', multiply(4, 6));