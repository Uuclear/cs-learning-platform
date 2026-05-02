// 编程挑战1解答：创建用户信息验证函数

// 定义用户接口
interface User {
  id: number;
  name: string;
  email: string;
  age: number;
}

// 验证用户信息的函数
function validateUser(user: User): { isValid: boolean; errors: string[] } {
  const errors: string[] = [];

  // 验证姓名
  if (!user.name || user.name.trim().length === 0) {
    errors.push("姓名不能为空");
  } else if (user.name.length > 50) {
    errors.push("姓名长度不能超过50个字符");
  }

  // 验证邮箱格式（简单验证）
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!user.email || !emailRegex.test(user.email)) {
    errors.push("邮箱格式不正确");
  }

  // 验证年龄范围
  if (user.age < 0 || user.age > 150) {
    errors.push("年龄必须在0-150之间");
  }

  // 验证ID
  if (user.id <= 0) {
    errors.push("ID必须是正整数");
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

// 测试用例
const validUser: User = {
  id: 1,
  name: "张三",
  email: "zhang@example.com",
  age: 25
};

const invalidUser: User = {
  id: -1,
  name: "",
  email: "invalid-email",
  age: 200
};

console.log("验证有效用户:");
console.log(validateUser(validUser));

console.log("\n验证无效用户:");
console.log(validateUser(invalidUser));