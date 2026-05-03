// example-03.js - class语法和继承

console.log("=== ES6 Class 基础 ===");
// Class 就像建筑蓝图：定义了对象应该有什么属性和方法

class Animal {
  // 构造函数 - 创建实例时自动调用
  constructor(name, species) {
    this.name = name;
    this.species = species;
    this.isAlive = true;
  }

  // 实例方法
  speak() {
    console.log(`${this.name} 发出了声音`);
  }

  // 静态方法 - 属于类本身，不属于实例
  static getCategory() {
    return '生物';
  }

  // Getter - 像读取属性一样调用方法
  get info() {
    return `${this.name} 是一只 ${this.species}`;
  }

  // Setter - 像设置属性一样调用方法
  set age(value) {
    if (value < 0) {
      console.log('年龄不能为负数！');
      return;
    }
    this._age = value;
  }

  get age() {
    return this._age || 0;
  }
}

// 创建实例
const dog = new Animal('旺财', '狗');
console.log(dog.info); // 旺财 是一只 狗
dog.speak(); // 旺财 发出了声音
console.log('类别:', Animal.getCategory()); // 生物

dog.age = 3;
console.log(`${dog.name} 的年龄是 ${dog.age} 岁`); // 3岁

console.log("\n=== 继承 (extends) ===");
// 继承就像子女继承父母的特征，还能有自己的特色

class Dog extends Animal {
  constructor(name, breed) {
    // 调用父类构造函数
    super(name, '狗');
    this.breed = breed; // 狗的品种
  }

  // 重写父类方法（方法覆盖）
  speak() {
    console.log(`${this.name} 汪汪叫！`);
  }

  // 新增特有方法
  fetch() {
    console.log(`${this.name} 去捡球了！`);
  }
}

class Cat extends Animal {
  constructor(name, color) {
    super(name, '猫');
    this.color = color;
  }

  speak() {
    console.log(`${this.name} 喵喵叫！`);
  }

  climb() {
    console.log(`${this.name} 爬上了树！`);
  }
}

// 使用继承的类
const goldenRetriever = new Dog('金毛', '金毛寻回犬');
const persianCat = new Cat('波斯', '白色');

goldenRetriever.speak(); // 金毛 汪汪叫！
goldenRetriever.fetch(); // 金毛 去捡球了！
console.log(goldenRetriever.info); // 金毛 是一只 狗

persianCat.speak(); // 波斯 喵喵叫！
persianCat.climb(); // 波斯 爬上了树！

console.log("\n=== instanceof 操作符 ===");
// instanceof 判断对象是否是某个类的实例
console.log('goldenRetriever 是 Dog 实例:', goldenRetriever instanceof Dog); // true
console.log('goldenRetriever 是 Animal 实例:', goldenRetriever instanceof Animal); // true
console.log('persianCat 是 Dog 实例:', persianCat instanceof Dog); // false

console.log("\n=== 私有字段 (ES2022+) ===");
// 私有字段用 # 开头，外部无法直接访问

class BankAccount {
  // 私有字段
  #balance = 0;
  #accountNumber;

  constructor(accountNumber) {
    this.#accountNumber = accountNumber;
  }

  deposit(amount) {
    if (amount > 0) {
      this.#balance += amount;
      console.log(`存入 ${amount} 元，当前余额: ${this.#balance}`);
    }
  }

  withdraw(amount) {
    if (amount > 0 && amount <= this.#balance) {
      this.#balance -= amount;
      console.log(`取出 ${amount} 元，当前余额: ${this.#balance}`);
    } else {
      console.log('余额不足或金额无效');
    }
  }

  // 公共方法访问私有字段
  getBalance() {
    return this.#balance;
  }

  // 无法从外部直接访问 #balance 或 #accountNumber
}

const myAccount = new BankAccount('123456789');
myAccount.deposit(1000);
myAccount.withdraw(200);
console.log('账户余额:', myAccount.getBalance()); // 800

// 尝试直接访问私有字段会报错
// console.log(myAccount.#balance); // SyntaxError: Private field '#balance' must be declared in an enclosing class

console.log("\n=== 类表达式 ===");
// 类也可以作为表达式使用

const Rectangle = class {
  constructor(width, height) {
    this.width = width;
    this.height = height;
  }

  getArea() {
    return this.width * this.height;
  }
};

const rect = new Rectangle(10, 5);
console.log('矩形面积:', rect.getArea()); // 50