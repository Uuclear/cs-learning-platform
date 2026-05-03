// solution-03.js - class语法和继承练习解答

// 练习1: 创建一个Person类
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  introduce() {
    return `大家好，我是${this.name}，今年${this.age}岁。`;
  }

  static compareAge(person1, person2) {
    return person1.age - person2.age;
  }
}

// 练习2: 创建Student类继承Person
class Student extends Person {
  constructor(name, age, grade, subjects = []) {
    super(name, age);
    this.grade = grade;
    this.subjects = subjects;
  }

  addSubject(subject) {
    this.subjects.push(subject);
  }

  getSubjects() {
    return this.subjects.join(', ');
  }

  // 重写introduce方法
  introduce() {
    return `${super.introduce()} 我在${this.grade}年级，学习科目: ${this.getSubjects()}`;
  }
}

// 练习3: 创建Teacher类继承Person
class Teacher extends Person {
  constructor(name, age, subject, students = []) {
    super(name, age);
    this.subject = subject;
    this.students = students;
  }

  addStudent(student) {
    if (student instanceof Student) {
      this.students.push(student);
    }
  }

  teach() {
    return `${this.name}老师正在教授${this.subject}课程。`;
  }
}

// 测试代码
const alice = new Person('Alice', 25);
console.log(alice.introduce());

const bob = new Student('Bob', 16, '高一', ['数学', '物理']);
bob.addSubject('化学');
console.log(bob.introduce());

const mrSmith = new Teacher('Smith', 40, '数学');
mrSmith.addStudent(bob);
console.log(mrSmith.teach());
console.log('年龄比较:', Person.compareAge(alice, bob)); // 正数表示alice年龄大

// 额外练习：使用私有字段的BankAccount
class SecureBankAccount {
  #pin;
  #balance = 0;

  constructor(pin) {
    this.#pin = pin;
  }

  deposit(amount, pin) {
    if (pin === this.#pin && amount > 0) {
      this.#balance += amount;
      return true;
    }
    return false;
  }

  getBalance(pin) {
    if (pin === this.#pin) {
      return this.#balance;
    }
    return null;
  }
}

const secureAccount = new SecureBankAccount(1234);
secureAccount.deposit(500, 1234);
console.log('安全账户余额:', secureAccount.getBalance(1234)); // 500
console.log('错误PIN码查询:', secureAccount.getBalance(0000)); // null