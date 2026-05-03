#include <iostream>
#include <string>
#include <vector>

/**
 * 解决方案3：改进的银行账户类，包含账户类型和更多功能
 */

// 账户类型枚举
enum class AccountType {
    SAVINGS,    // 储蓄账户
    CHECKING,   // 支票账户
    BUSINESS    // 商业账户
};

// 获取账户类型名称
std::string getAccountTypeName(AccountType type) {
    switch (type) {
        case AccountType::SAVINGS: return "储蓄账户";
        case AccountType::CHECKING: return "支票账户";
        case AccountType::BUSINESS: return "商业账户";
        default: return "未知账户类型";
    }
}

class BankAccount {
private:
    std::string accountNumber;
    double balance;
    std::string ownerName;
    AccountType accountType;
    std::vector<std::string> transactionHistory;
    double interestRate; // 利率（仅储蓄账户使用）

public:
    // 构造函数
    BankAccount(std::string accNum, std::string owner, AccountType type,
                double initialBalance = 0.0, double rate = 0.0)
        : accountNumber(accNum), ownerName(owner), accountType(type),
          balance(initialBalance), interestRate(rate) {

        if (balance < 0) {
            balance = 0;
            addTransaction("警告：初始余额不能为负数，已设为0");
        }

        if (initialBalance > 0) {
            addTransaction("初始存款: " + std::to_string(initialBalance) + "元");
        }

        // 验证利率
        if (interestRate < 0) interestRate = 0;
    }

    // 存款功能
    void deposit(double amount, const std::string& description = "") {
        if (amount > 0) {
            balance += amount;
            addTransaction("存款: " + std::to_string(amount) + "元" +
                          (description.empty() ? "" : " (" + description + ")"));
            std::cout << "存款成功！当前余额：" << balance << "元" << std::endl;
        } else {
            std::cout << "存款金额必须大于0" << std::endl;
        }
    }

    // 取款功能
    bool withdraw(double amount, const std::string& description = "") {
        if (amount <= 0) {
            std::cout << "取款金额必须大于0" << std::endl;
            return false;
        }

        // 支票账户和商业账户可能有透支保护
        double minBalance = 0.0;
        if (accountType == AccountType::CHECKING) {
            minBalance = -1000.0; // 允许透支1000元
        } else if (accountType == AccountType::BUSINESS) {
            minBalance = -5000.0; // 允许透支5000元
        }

        if (balance - amount < minBalance) {
            std::cout << "取款失败：余额不足" << std::endl;
            return false;
        }

        balance -= amount;
        addTransaction("取款: " + std::to_string(amount) + "元" +
                      (description.empty() ? "" : " (" + description + ")"));
        std::cout << "取款成功！当前余额：" << balance << "元" << std::endl;
        return true;
    }

    // 转账功能
    bool transferTo(BankAccount& target, double amount, const std::string& description = "") {
        if (amount <= 0) {
            std::cout << "转账金额必须大于0" << std::endl;
            return false;
        }

        // 尝试从当前账户取款
        if (!withdraw(amount, "转账到 " + target.accountNumber)) {
            return false;
        }

        // 向目标账户存款
        target.deposit(amount, "从 " + accountNumber + " 转入");

        // 注意：withdraw和deposit已经记录了交易，所以这里不需要额外记录
        std::cout << "向 " << target.ownerName << " 转账成功！" << std::endl;
        return true;
    }

    // 计算利息（仅储蓄账户）
    void calculateInterest() {
        if (accountType == AccountType::SAVINGS && interestRate > 0) {
            double interest = balance * (interestRate / 100.0);
            balance += interest;
            addTransaction("利息收入: " + std::to_string(interest) + "元 (利率: " +
                          std::to_string(interestRate) + "%)");
            std::cout << "利息计算完成！新增利息：" << interest << "元" << std::endl;
        } else {
            std::cout << "此账户类型不支持利息计算" << std::endl;
        }
    }

    // 获取余额
    double getBalance() const {
        return balance;
    }

    // 获取账户信息
    void displayInfo() const {
        std::cout << "=== 账户信息 ===" << std::endl;
        std::cout << "账户持有人：" << ownerName << std::endl;
        std::cout << "账号：" << accountNumber << std::endl;
        std::cout << "账户类型：" << getAccountTypeName(accountType) << std::endl;
        std::cout << "当前余额：" << balance << "元" << std::endl;
        if (accountType == AccountType::SAVINGS) {
            std::cout << "年利率：" << interestRate << "%" << std::endl;
        }
        std::cout << "===============" << std::endl;
    }

    // 显示交易历史
    void displayTransactionHistory() const {
        std::cout << "\n=== " << ownerName << " 的交易历史 ===" << std::endl;
        if (transactionHistory.empty()) {
            std::cout << "暂无交易记录" << std::endl;
        } else {
            for (size_t i = 0; i < transactionHistory.size(); ++i) {
                std::cout << (i + 1) << ". " << transactionHistory[i] << std::endl;
            }
        }
        std::cout << "=========================" << std::endl;
    }

    // 获取账户类型
    AccountType getAccountType() const {
        return accountType;
    }

    // 获取利率
    double getInterestRate() const {
        return interestRate;
    }

    // 内部辅助函数：添加交易记录
    void addTransaction(const std::string& transaction) {
        // 获取当前时间戳（简化版）
        transactionHistory.push_back(transaction);
    }

    // 析构函数
    ~BankAccount() {
        std::cout << "账户 " << accountNumber << " (" << getAccountTypeName(accountType)
                  << ") 已关闭。" << std::endl;
    }
};

// 使用示例
int main() {
    std::cout << "=== 改进的银行账户类解决方案 ===" << std::endl;

    // 创建不同类型的账户
    BankAccount savingsAcc("SAV-001", "张三", AccountType::SAVINGS, 5000.0, 2.5);
    BankAccount checkingAcc("CHK-001", "李四", AccountType::CHECKING, 2000.0);
    BankAccount businessAcc("BUS-001", "ABC公司", AccountType::BUSINESS, 10000.0);

    // 显示账户信息
    savingsAcc.displayInfo();
    checkingAcc.displayInfo();
    businessAcc.displayInfo();

    // 测试储蓄账户的利息功能
    std::cout << "\n=== 储蓄账户利息计算 ===" << std::endl;
    savingsAcc.calculateInterest();
    savingsAcc.displayInfo();

    // 测试不同账户类型的取款限制
    std::cout << "\n=== 测试取款限制 ===" << std::endl;
    std::cout << "储蓄账户尝试透支取款2000元：" << std::endl;
    savingsAcc.withdraw(2000.0); // 应该失败

    std::cout << "\n支票账户尝试透支取款1500元：" << std::endl;
    checkingAcc.withdraw(1500.0); // 应该失败（超过1000元透支限额）

    std::cout << "\n支票账户尝试透支取款800元：" << std::endl;
    checkingAcc.withdraw(800.0); // 应该成功

    // 测试转账功能
    std::cout << "\n=== 转账测试 ===" << std::endl;
    savingsAcc.transferTo(checkingAcc, 1000.0, "朋友借款");

    // 显示最终状态
    std::cout << "\n=== 最终账户状态 ===" << std::endl;
    savingsAcc.displayInfo();
    checkingAcc.displayInfo();

    // 显示交易历史
    savingsAcc.displayTransactionHistory();
    checkingAcc.displayTransactionHistory();

    return 0;
}