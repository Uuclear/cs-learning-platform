// solution-02.js - 闭包创建和私有变量解决方案

console.log("=== 闭包创建和私有变量解决方案 ===\n");

// 1. 基础闭包示例
console.log("1. 基础闭包:");

function createCounter(initialValue = 0) {
  let count = initialValue; // 私有变量，外部无法直接访问

  return {
    increment: function() {
      count++;
      return count;
    },
    decrement: function() {
      count--;
      return count;
    },
    getValue: function() {
      return count;
    },
    reset: function() {
      count = initialValue;
      return count;
    }
  };
}

const counter = createCounter(10);
console.log("初始值:", counter.getValue()); // 10
console.log("递增:", counter.increment());  // 11
console.log("递减:", counter.decrement());  // 10
console.log("重置:", counter.reset());      // 10

// 尝试直接访问私有变量（会失败）
// console.log(counter.count); // undefined

// 2. 多个独立闭包实例
console.log("\n2. 独立闭包实例:");

const counterA = createCounter(0);
const counterB = createCounter(100);

console.log("计数器A:", counterA.increment(), counterA.increment()); // 1, 2
console.log("计数器B:", counterB.increment(), counterB.decrement()); // 101, 100
console.log("计数器A再次:", counterA.getValue()); // 2 (独立于B)

// 3. 私有方法和数据封装
console.log("\n3. 数据封装:");

function createBankAccount(initialBalance) {
  let balance = initialBalance;
  const transactionHistory = [];

  // 私有辅助函数
  function logTransaction(type, amount) {
    const timestamp = new Date().toISOString();
    transactionHistory.push({
      type,
      amount,
      balance: balance,
      timestamp
    });
  }

  return {
    deposit: function(amount) {
      if (amount <= 0) {
        throw new Error("存款金额必须大于0");
      }
      balance += amount;
      logTransaction("deposit", amount);
      return balance;
    },

    withdraw: function(amount) {
      if (amount <= 0) {
        throw new Error("取款金额必须大于0");
      }
      if (amount > balance) {
        throw new Error("余额不足");
      }
      balance -= amount;
      logTransaction("withdraw", amount);
      return balance;
    },

    getBalance: function() {
      return balance;
    },

    getTransactionHistory: function() {
      // 返回副本，防止外部修改
      return [...transactionHistory];
    }
  };
}

const account = createBankAccount(1000);
console.log("初始余额:", account.getBalance()); // 1000
console.log("存款500:", account.deposit(500));   // 1500
console.log("取款200:", account.withdraw(200));  // 1300

// 查看交易历史
const history = account.getTransactionHistory();
console.log("交易次数:", history.length); // 3
console.log("最新交易:", history[history.length - 1]);

// 4. 闭包中的this绑定问题
console.log("\n4. this绑定与闭包:");

const person = {
  name: "张三",
  greet: function() {
    const self = this; // 保存this引用

    setTimeout(function() {
      // 在普通函数中，this指向全局对象（或undefined严格模式）
      // 但我们可以使用闭包捕获self
      console.log(`你好, 我是 ${self.name}!`);
    }, 100);

    // 箭头函数版本（自动绑定this）
    setTimeout(() => {
      console.log(`箭头函数: 你好, 我是 ${this.name}!`);
    }, 200);
  }
};

person.greet();