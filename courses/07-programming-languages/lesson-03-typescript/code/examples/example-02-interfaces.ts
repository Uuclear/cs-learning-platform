// TypeScript 接口示例
// 编译命令: tsc example-02-interfaces.ts

// 定义用户接口
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;        // 可选属性，用 ? 标记
  isActive: boolean;
}

// 定义产品接口
interface Product {
  id: string;
  name: string;
  price: number;
  category: string;
  description?: string;  // 可选属性
  inStock: boolean;
}

// 实现接口的对象
const user1: User = {
  id: 1,
  name: "王小明",
  email: "wang@example.com",
  isActive: true
  // 注意：age 是可选的，所以可以不提供
};

const product1: Product = {
  id: "P001",
  name: "TypeScript编程指南",
  price: 59.99,
  category: "图书",
  inStock: true,
  description: "从入门到精通的TypeScript教程"
};

// 函数参数使用接口类型
function displayUser(user: User): void {
  console.log(`用户信息:`);
  console.log(`ID: ${user.id}`);
  console.log(`姓名: ${user.name}`);
  console.log(`邮箱: ${user.email}`);
  console.log(`年龄: ${user.age || "未提供"}`);  // 处理可选属性
  console.log(`状态: ${user.isActive ? "活跃" : "非活跃"}`);
  console.log("---");
}

function displayProduct(product: Product): void {
  console.log(`商品信息:`);
  console.log(`ID: ${product.id}`);
  console.log(`名称: ${product.name}`);
  console.log(`价格: ¥${product.price}`);
  console.log(`分类: ${product.category}`);
  if (product.description) {
    console.log(`描述: ${product.description}`);
  }
  console.log(`库存: ${product.inStock ? "有货" : "缺货"}`);
  console.log("---");
}

// 扩展接口 - 继承其他接口
interface Admin extends User {
  permissions: string[];  // 管理员额外的权限数组
  department: string;     // 所属部门
}

const adminUser: Admin = {
  id: 2,
  name: "李管理员",
  email: "admin@company.com",
  age: 35,
  isActive: true,
  permissions: ["read", "write", "delete", "manage"],
  department: "技术部"
};

function displayAdmin(admin: Admin): void {
  displayUser(admin);  // 复用 User 的显示逻辑
  console.log(`权限: ${admin.permissions.join(", ")}`);
  console.log(`部门: ${admin.department}`);
}

// 调用函数并输出结果
displayUser(user1);
displayProduct(product1);
displayAdmin(adminUser);