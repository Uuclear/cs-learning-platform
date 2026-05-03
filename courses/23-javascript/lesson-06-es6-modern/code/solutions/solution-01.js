// solution-01.js - 解构赋值和展开运算符练习解答

// 练习1: 使用解构从用户对象中提取信息
const extractUserInfo = (user) => {
  const { name, email, age = 18 } = user;
  return { name, email, age };
};

// 练习2: 合并两个配置对象，新配置优先
const mergeConfig = (defaultConfig, userConfig) => {
  return { ...defaultConfig, ...userConfig };
};

// 练习3: 实现一个函数，接受任意数量的数字并返回最大值
const findMax = (...numbers) => {
  return Math.max(...numbers);
};

// 测试代码
const testUser = { name: '李四', email: 'lisi@example.com' };
console.log('提取用户信息:', extractUserInfo(testUser));

const defaultConf = { theme: 'light', language: 'en' };
const userConf = { language: 'zh', notifications: true };
console.log('合并配置:', mergeConfig(defaultConf, userConf));

console.log('最大值:', findMax(1, 5, 3, 9, 2)); // 9

// 额外练习：数组解构交换变量
let a = 10, b = 20;
[a, b] = [b, a];
console.log(`交换后: a=${a}, b=${b}`); // a=20, b=10