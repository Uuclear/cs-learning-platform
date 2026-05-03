/**
 * Solution02: 自定义异常解决方案
 * 实现一个完整的银行账户系统，包含自定义异常处理
 */
import java.util.HashMap;
import java.util.Map;

// 自定义受检异常：账户不存在
class AccountNotFoundException extends Exception {
    public AccountNotFoundException(String accountId) {
        super("账户不存在: " + accountId);
    }
}

// 自定义受检异常：余额不足
class InsufficientBalanceException extends Exception {
    private double currentBalance;
    private double requestedAmount;
    
    public InsufficientBalanceException(double currentBalance, double requestedAmount) {
        super(String.format("余额不足: 当前余额=%.2f, 请求金额=%.2f", 
              currentBalance, requestedAmount));
        this.currentBalance = currentBalance;
        this.requestedAmount = requestedAmount;
    }
    
    public double getCurrentBalance() { return currentBalance; }
    public double getRequestedAmount() { return requestedAmount; }
}

// 银行账户类
class BankAccount {
    private String accountId;
    private double balance;
    
    public BankAccount(String accountId, double initialBalance) {
        if (initialBalance < 0) {
            throw new IllegalArgumentException("初始余额不能为负数");
        }
        this.accountId = accountId;
        this.balance = initialBalance;
    }
    
    public String getAccountId() { return accountId; }
    public double getBalance() { return balance; }
    
    /**
     * 存款方法
     */
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("存款金额必须大于0");
        }
        balance += amount;
        System.out.println("存款成功! 账户 " + accountId + " 新余额: " + balance);
    }
    
    /**
     * 取款方法，可能抛出受检异常
     */
    public void withdraw(double amount) throws InsufficientBalanceException {
        if (amount <= 0) {
            throw new IllegalArgumentException("取款金额必须大于0");
        }
        if (amount > balance) {
            throw new InsufficientBalanceException(balance, amount);
        }
        balance -= amount;
        System.out.println("取款成功! 账户 " + accountId + " 新余额: " + balance);
    }
}

// 银行服务类
class BankService {
    private Map<String, BankAccount> accounts = new HashMap<>();
    
    public void createAccount(String accountId, double initialBalance) {
        if (accounts.containsKey(accountId)) {
            throw new IllegalArgumentException("账户已存在: " + accountId);
        }
        accounts.put(accountId, new BankAccount(accountId, initialBalance));
        System.out.println("账户创建成功: " + accountId);
    }
    
    public BankAccount getAccount(String accountId) throws AccountNotFoundException {
        BankAccount account = accounts.get(accountId);
        if (account == null) {
            throw new AccountNotFoundException(accountId);
        }
        return account;
    }
    
    public void transfer(String fromAccountId, String toAccountId, double amount) 
            throws AccountNotFoundException, InsufficientBalanceException {
        
        BankAccount fromAccount = getAccount(fromAccountId);
        BankAccount toAccount = getAccount(toAccountId);
        
        fromAccount.withdraw(amount);
        toAccount.deposit(amount);
        
        System.out.println("转账成功: " + fromAccountId + " -> " + toAccountId + 
                          ", 金额: " + amount);
    }
}

public class Solution02 {
    public static void main(String[] args) {
        System.out.println("=== Solution 2: 自定义异常完整示例 ===");
        
        BankService bank = new BankService();
        
        // 创建账户
        bank.createAccount("ACC001", 1000.0);
        bank.createAccount("ACC002", 500.0);
        
        try {
            // 正常转账
            bank.transfer("ACC001", "ACC002", 200.0);
            
            // 尝试余额不足的转账
            bank.transfer("ACC002", "ACC001", 1000.0);
            
        } catch (AccountNotFoundException e) {
            System.out.println("账户错误: " + e.getMessage());
        } catch (InsufficientBalanceException e) {
            System.out.println("余额错误: " + e.getMessage());
            System.out.printf("当前余额: %.2f, 请求金额: %.2f%n", 
                            e.getCurrentBalance(), e.getRequestedAmount());
        } catch (IllegalArgumentException e) {
            System.out.println("参数错误: " + e.getMessage());
        }
        
        // 测试不存在的账户
        try {
            bank.transfer("ACC999", "ACC001", 100.0);
        } catch (AccountNotFoundException e) {
            System.out.println("账户错误: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("其他错误: " + e.getMessage());
        }
    }
}
