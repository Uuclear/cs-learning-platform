// example-02.js - 模板字符串和Map/Set使用

console.log("=== 模板字符串 (Template Literals) ===");
// 模板字符串就像智能填空题：直接在字符串里插入变量和表达式

const userName = '小红';
const userAge = 25;

// 基础模板字符串
const greeting = `你好, ${userName}! 你今年${userAge}岁了。`;
console.log(greeting);

// 多行字符串（告别\n换行符）
const poem = `
春眠不觉晓，
处处闻啼鸟。
夜来风雨声，
花落知多少。
`;
console.log('古诗:');
console.log(poem);

// 表达式插值
const price = 99.99;
const taxRate = 0.08;
const totalPrice = `商品价格: $${price}, 含税总价: $${(price * (1 + taxRate)).toFixed(2)}`;
console.log(totalPrice);

// 标签模板（高级用法 - 自定义处理函数）
function highlight(strings, ...values) {
  let result = '';
  for (let i = 0; i < values.length; i++) {
    result += strings[i] + `<strong>${values[i]}</strong>`;
  }
  result += strings[strings.length - 1];
  return result;
}

const highlightedText = highlight`用户名: ${userName}, 年龄: ${userAge}`;
console.log('高亮文本:', highlightedText);

console.log("\n=== Map 数据结构 ===");
// Map 就像升级版的对象：键可以是任何类型，还有更多实用方法

// 创建Map
const userInfoMap = new Map();

// 设置键值对（键可以是任何类型！）
userInfoMap.set('name', '张三');
userInfoMap.set(123, '用户ID');
userInfoMap.set(true, '是否激活');
userInfoMap.set({ id: 1 }, '特殊对象键');

console.log('Map大小:', userInfoMap.size); // 4

// 获取值
console.log('用户名:', userInfoMap.get('name')); // 张三
console.log('用户ID:', userInfoMap.get(123)); // 用户ID

// 检查是否存在
console.log('是否有name键:', userInfoMap.has('name')); // true

// 遍历Map
console.log('\n遍历Map:');
for (const [key, value] of userInfoMap) {
  console.log(`${key} => ${value}`);
}

// 从数组创建Map
const keyValuePairs = [['color', 'red'], ['size', 'large'], ['material', 'cotton']];
const productMap = new Map(keyValuePairs);
console.log('产品信息Map:', [...productMap]);

console.log("\n=== Set 数据结构 ===");
// Set 就像自动去重的集合：重复的元素会被自动过滤掉

// 创建Set
const uniqueNumbers = new Set([1, 2, 2, 3, 3, 3, 4]);
console.log('去重后的数字:', [...uniqueNumbers]); // [1, 2, 3, 4]

// 添加元素
uniqueNumbers.add(5).add(6);
console.log('添加后:', [...uniqueNumbers]);

// 删除元素
uniqueNumbers.delete(1);
console.log('删除1后:', [...uniqueNumbers]);

// 检查是否存在
console.log('是否包含3:', uniqueNumbers.has(3)); // true

// 实际应用场景：数组去重
const duplicateArray = ['apple', 'banana', 'apple', 'orange', 'banana'];
const uniqueFruits = [...new Set(duplicateArray)];
console.log('去重水果:', uniqueFruits);

// 交集、并集、差集操作
const setA = new Set([1, 2, 3, 4]);
const setB = new Set([3, 4, 5, 6]);

// 交集
const intersection = new Set([...setA].filter(x => setB.has(x)));
console.log('交集:', [...intersection]); // [3, 4]

// 并集
const union = new Set([...setA, ...setB]);
console.log('并集:', [...union]); // [1, 2, 3, 4, 5, 6]

// 差集 (A - B)
const difference = new Set([...setA].filter(x => !setB.has(x)));
console.log('差集(A-B):', [...difference]); // [1, 2]