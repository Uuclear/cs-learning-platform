# 编程挑战 1：类型安全的配置合并函数

## 任务描述

创建一个函数 `mergeConfig(baseConfig, userConfig)`，它能够安全地合并两个配置对象，而不会意外修改原始对象。

## 要求

1. 函数必须返回一个新对象，不能修改 `baseConfig` 或 `userConfig`
2. 支持嵌套对象的深度合并
3. 处理数组时，应该用 `userConfig` 中的数组完全替换 `baseConfig` 中的数组（不是合并数组元素）
4. 忽略 `userConfig` 中值为 `undefined` 的属性
5. 包含适当的类型检查和错误处理

## 示例

```javascript
const defaultConfig = {
  server: {
    port: 3000,
    host: 'localhost',
    ssl: false
  },
  database: {
    url: 'mongodb://localhost:27017',
    options: {
      useNewUrlParser: true,
      useUnifiedTopology: true
    }
  },
  features: ['auth', 'logging']
};

const userConfig = {
  server: {
    port: 8080,
    ssl: true
  },
  database: {
    url: 'mongodb://prod-server:27017'
  },
  features: ['auth', 'logging', 'monitoring']
};

const finalConfig = mergeConfig(defaultConfig, userConfig);
console.log(finalConfig);
// 应该输出合并后的完整配置，包含所有默认值和用户覆盖值
```

## 提示

- 使用展开运算符进行浅拷贝
- 对于嵌套对象，需要递归处理
- 注意处理 `null` 和 `undefined` 的情况
- 考虑使用 `hasOwnProperty` 来检查属性是否存在

## 验证测试

你的函数应该通过以下测试：

```javascript
// 测试1：基本合并
const result1 = mergeConfig({ a: 1, b: 2 }, { b: 3, c: 4 });
// 期望: { a: 1, b: 3, c: 4 }

// 测试2：嵌套对象
const result2 = mergeConfig({ obj: { x: 1 } }, { obj: { y: 2 } });
// 期望: { obj: { x: 1, y: 2 } }

// 测试3：数组替换
const result3 = mergeConfig({ arr: [1, 2] }, { arr: [3, 4] });
// 期望: { arr: [3, 4] }

// 测试4：undefined值被忽略
const result4 = mergeConfig({ a: 1, b: 2 }, { a: undefined, c: 3 });
// 期望: { a: 1, b: 2, c: 3 }
```