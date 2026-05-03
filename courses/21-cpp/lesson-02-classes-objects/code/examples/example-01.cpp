#include <iostream>
#include <string>

/**
 * 示例1：银行账户类
 * 演示封装、构造函数、成员函数的使用
 */
class BankAccount {
private:
    std::string accountNumber;
    double balance;
    std::string ownerName;

public:
    // 构造函数 - 初始化账户
    BankAccount(std::string accNum, std::string owner, double initialBalance = 0.0)
        : accountNumber(accNum), ownerName(owner), balance(initialBalance) {
        if (balance < 0) {
            balance = 0;
            std::cout << "警告：初始余额不能为负数，已设为0" << std::endl;
        }
    }

    // 存款功能
    void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            std::cout << "存款成功！当前余额：" << balance << std::endl;
        } else {
            std::cout << "存款金额必须大于0" << std::endl;
        }
    }

    // 取款功能
    bool withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            std::cout << "取款成功！当前余额：" << balance << std::endl;
            return true;
        } else {
            std::cout << "取款失败：余额不足或金额无效" << std::endl;
            return false;
        }
    }

    // 查询余额（const成员函数）
    double getBalance() const {
        return balance;
    }

    // 获取账户信息（const成员函数）
    void displayInfo() const {
        std::cout << "账户持有人：" << ownerName
                  << "，账号：" << accountNumber
                  << "，余额：" << balance << std::endl;
    }

    // 析构函数
    ~BankAccount() {
        std::cout << "账户 " << accountNumber << " 已关闭。" << std::endl;
    }
};

// 使用示例
int main() {
    std::cout << "=== 银行账户类演示 ===" << std::endl;

    // 创建银行账户对象
    BankAccount myAccount("ACC-12345", "张三", 1000.0);

    // 显示账户信息
    myAccount.displayInfo();

    // 进行一些操作
    myAccount.deposit(500.0);
    myAccount.withdraw(200.0);
    myAccount.withdraw(2000.0); // 这会失败

    std::cout << "最终余额：" << myAccount.getBalance() << std::endl;

    return 0;
}