# 编程挑战 2：函数式编程工具库

## 任务描述

创建一个简单的函数式编程工具库，包含以下三个核心函数：

1. `pipe` - 从左到右组合函数
2. `compose` - 从右到左组合函数  
3. `memoize` - 为函数添加记忆化（缓存）功能

## 要求

### pipe 函数
- 接收任意数量的函数作为参数
- 返回一个新函数，该函数接收一个初始值
- 按照从左到右的顺序依次调用每个函数，前一个函数的返回值作为后一个函数的输入
- 如果没有提供函数，返回初始值

### compose 函数
- 接收任意数量的函数作为参数
- 返回一个新函数，该函数接收一个初始值
- 按照从右到左的顺序依次调用每个函数（与pipe相反）
- 如果没有提供函数，返回初始值

### memoize 函数
- 接收一个函数作为参数
- 返回一个带有记忆化功能的新函数
- 对于相同的输入参数，直接返回缓存的结果，不再执行原函数
- 使用参数的字符串化作为缓存键（简化实现）

## 示例

```javascript
// pipe 示例
const add = x => x + 1;
const multiply = x => x * 2;
const subtract = x => x - 3;

const piped = pipe(add, multiply, subtract);
console.log(piped(5)); // ((5 + 1) * 2) - 3 = 9

// compose 示例  
const composed = compose(subtract, multiply, add);
console.log(composed(5)); // (5 + 1) * 2 - 3 = 9 (same result, different order)

// memoize 示例
const expensiveCalculation = (x) => {
  console.log(`计算 ${x} 的平方...`);
  return x * x;
};

const memoizedCalc = memoize(expensiveCalculation);
console.log(memoizedCalc(5)); // 计算 5 的平方... \n 25
console.log(memoizedCalc(5)); // 25 (直接返回缓存结果，不打印计算信息)
```

## 提示

- 使用剩余参数（...args）接收任意数量的函数
- 使用 `reduce` 方法来实现函数组合
- 对于 `memoize`，可以使用一个对象或 Map 来存储缓存
- 注意处理多个参数的情况（可以使用 `JSON.stringify` 或其他方式生成缓存键）

## 验证测试

你的实现应该通过以下测试：

```javascript
// pipe 测试
const double = x => x * 2;
const addTen = x => x + 10;
const result1 = pipe(double, addTen)(5); // (5 * 2) + 10 = 20

// compose 测试  
const result2 = compose(addTen, double)(5); // (5 + 10) * 2 = 30

// memoize 测试
let callCount = 0;
const counter = (x) => {
  callCount++;
  return x;
};
const memoizedCounter = memoize(counter);
memoizedCounter(1); // callCount = 1
memoizedCounter(1); // callCount = 1 (cached)
memoizedCounter(2); // callCount = 2
```