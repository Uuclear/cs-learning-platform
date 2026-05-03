// solution-02.js - 模板字符串和Map/Set练习解答

// 练习1: 使用模板字符串格式化用户信息
const formatUserInfo = (user) => {
  return `
用户信息卡
==========
姓名: ${user.name}
年龄: ${user.age}
邮箱: ${user.email || '未提供'}
状态: ${user.isActive ? '活跃' : '非活跃'}
  `.trim();
};

// 练习2: 使用Map存储购物车商品
class ShoppingCart {
  constructor() {
    this.items = new Map();
  }

  addItem(product, quantity) {
    const currentQty = this.items.get(product) || 0;
    this.items.set(product, currentQty + quantity);
  }

  removeItem(product) {
    this.items.delete(product);
  }

  getTotalItems() {
    let total = 0;
    for (const qty of this.items.values()) {
      total += qty;
    }
    return total;
  }

  getItems() {
    return [...this.items.entries()];
  }
}

// 练习3: 使用Set实现数组去重和交集
const arrayUtils = {
  unique: (arr) => [...new Set(arr)],

  intersection: (arr1, arr2) => {
    const set1 = new Set(arr1);
    const set2 = new Set(arr2);
    return [...set1].filter(x => set2.has(x));
  },

  union: (arr1, arr2) => [...new Set([...arr1, ...arr2])]
};

// 测试代码
const user = { name: '王五', age: 30, email: 'wangwu@example.com', isActive: true };
console.log(formatUserInfo(user));

const cart = new ShoppingCart();
cart.addItem('苹果', 3);
cart.addItem('香蕉', 2);
cart.addItem('苹果', 2); // 累计苹果数量为5
console.log('购物车商品:', cart.getItems());
console.log('总商品数:', cart.getTotalItems());

const nums1 = [1, 2, 3, 4];
const nums2 = [3, 4, 5, 6];
console.log('去重:', arrayUtils.unique([1, 2, 2, 3, 3, 4]));
console.log('交集:', arrayUtils.intersection(nums1, nums2)); // [3, 4]
console.log('并集:', arrayUtils.union(nums1, nums2)); // [1, 2, 3, 4, 5, 6]