#include <iostream>
#include <string>

/**
 * 解决方案1：银行账户类完整实现
 * 包含交易历史记录和转账功能
 */
#include <vector>
#include <ctime>
#include <iomanip>

class Transaction {
public:
    enum Type { DEPOSIT, WITHDRAWAL, TRANSFER_IN, TRANSFER_OUT };

    Transaction(Type t, double amount, const std::string& desc = "")
        : type(t), amount(amount), description(desc) {
        time_t now = time(0);
        timestamp = ctime(&now);
        // 移除ctime返回字符串末尾的换行符
        if (!timestamp.empty() && timestamp.back() == '\n') {
            timestamp.pop_back();
        }
    }

    void display() const {
        std::string typeStr;
        switch (type) {
            case DEPOSIT: typeStr = "存款"; break;
            case WITHDRAWAL: typeStr = "取款"; break;
            case TRANSFER_IN: typeStr = "转入"; break;
            case TRANSFER_OUT: typeStr = "转出"; break;
        }
        std::cout << "[" << timestamp << "] " << typeStr
                  << " " << amount << "元";
        if (!description.empty()) {
            std::cout << " (" << description << ")";
        }
        std::cout << std::endl;
    }

private:
    Type type;
    double amount;
    std::string description;
    std::string timestamp;
};

class BankAccount {
private:
    std::string accountNumber;
    double balance;
    std::string ownerName;
    std::vector<Transaction> transactionHistory;

public:
    // 构造函数
    BankAccount(std::string accNum, std::string owner, double initialBalance = 0.0)
        : accountNumber(accNum), ownerName(owner), balance(initialBalance) {
        if (balance < 0) {
            balance = 0;
            std::cout << "警告：初始余额不能为负数，已设为0" << std::endl;
        }
        if (initialBalance > 0) {
            transactionHistory.emplace_back(Transaction::DEPOSIT, initialBalance, "初始存款");
        }
    }

    // 存款功能
    void deposit(double amount, const std::string& description = "") {
        if (amount > 0) {
            balance += amount;
            transactionHistory.emplace_back(Transaction::DEPOSIT, amount, description);
            std::cout << "存款成功！当前余额：" << balance << std::endl;
        } else {
            std::cout << "存款金额必须大于0" << std::endl;
        }
    }

    // 取款功能
    bool withdraw(double amount, const std::string& description = "") {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            transactionHistory.emplace_back(Transaction::WITHDRAWAL, amount, description);
            std::cout << "取款成功！当前余额：" << balance << std::endl;
            return true;
        } else {
            std::cout << "取款失败：余额不足或金额无效" << std::endl;
            return false;
        }
    }

    // 转账功能
    bool transferTo(BankAccount& target, double amount, const std::string& description = "") {
        if (amount <= 0) {
            std::cout << "转账金额必须大于0" << std::endl;
            return false;
        }
        if (amount > balance) {
            std::cout << "转账失败：余额不足" << std::endl;
            return false;
        }

        // 执行转账
        balance -= amount;
        target.balance += amount;

        // 记录交易
        transactionHistory.emplace_back(Transaction::TRANSFER_OUT, amount,
            "转账到 " + target.accountNumber + (description.empty() ? "" : " - " + description));
        target.transactionHistory.emplace_back(Transaction::TRANSFER_IN, amount,
            "从 " + accountNumber + (description.empty() ? "" : " - " + description));

        std::cout << "转账成功！向 " << target.ownerName
                  << " (" << target.accountNumber << ") 转账 " << amount << " 元" << std::endl;
        std::cout << "当前余额：" << balance << std::endl;
        return true;
    }

    // 查询余额
    double getBalance() const {
        return balance;
    }

    // 获取账户信息
    void displayInfo() const {
        std::cout << "账户持有人：" << ownerName
                  << "，账号：" << accountNumber
                  << "，余额：" << balance << std::endl;
    }

    // 显示交易历史
    void displayTransactionHistory() const {
        std::cout << "\n=== " << ownerName << " 的交易历史 ===" << std::endl;
        if (transactionHistory.empty()) {
            std::cout << "暂无交易记录" << std::endl;
        } else {
            for (const auto& transaction : transactionHistory) {
                transaction.display();
            }
        }
        std::cout << "=========================" << std::endl;
    }

    // 获取账户号
    std::string getAccountNumber() const {
        return accountNumber;
    }

    // 获取账户持有人姓名
    std::string getOwnerName() const {
        return ownerName;
    }

    // 析构函数
    ~BankAccount() {
        std::cout << "账户 " << accountNumber << " 已关闭。" << std::endl;
    }
};

// 使用示例
int main() {
    std::cout << "=== 银行账户类完整解决方案 ===" << std::endl;

    // 创建两个银行账户
    BankAccount account1("ACC-001", "张三", 1000.0);
    BankAccount account2("ACC-002", "李四", 500.0);

    // 显示初始信息
    account1.displayInfo();
    account2.displayInfo();

    // 进行一些操作
    account1.deposit(200.0, "工资收入");
    account1.withdraw(150.0, "购物");
    account1.transferTo(account2, 300.0, "还款");

    // 显示最终信息
    std::cout << "\n=== 最终账户状态 ===" << std::endl;
    account1.displayInfo();
    account2.displayInfo();

    // 显示交易历史
    account1.displayTransactionHistory();
    account2.displayTransactionHistory();

    return 0;
}