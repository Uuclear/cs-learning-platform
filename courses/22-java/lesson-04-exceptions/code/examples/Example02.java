/**
 * Example02: 自定义异常与 throw/throws 示例
 * 演示如何创建自定义异常类以及throw和throws的使用
 */

// 自定义受检异常
class InsufficientFundsException extends Exception {
    private double balance;
    private double amount;
    
    public InsufficientFundsException(double balance, double amount) {
        super("余额不足: 余额=" + balance + ", 尝试取款=" + amount);
        this.balance = balance;
        this.amount = amount;
    }
    
    public double getBalance() { return balance; }
    public double getAmount() { return amount; }
}

// 自定义非受检异常
class InvalidAccountException extends RuntimeException {
    public InvalidAccountException(String accountId) {
        super("无效的账户ID: " + accountId);
    }
}

public class Example02 {
    private static final String VALID_ACCOUNT_ID = "ACC123456";
    private static double accountBalance = 1000.0;
    
    public static void main(String[] args) {
        System.out.println("=== Example 2: 自定义异常与 throw/throws ===");
        
        // 测试有效的账户操作
        try {
            withdraw("ACC123456", 500.0);
            System.out.println("取款成功!");
        } catch (InsufficientFundsException e) {
            System.out.println("余额不足: " + e.getMessage());
        } catch (InvalidAccountException e) {
            System.out.println("账户无效: " + e.getMessage());
        }
        
        // 测试无效的账户ID
        try {
            withdraw("INVALID123", 100.0);
        } catch (InsufficientFundsException e) {
            System.out.println("余额不足: " + e.getMessage());
        } catch (InvalidAccountException e) {
            System.out.println("账户无效: " + e.getMessage());
        }
        
        // 测试余额不足的情况
        try {
            withdraw("ACC123456", 2000.0);
        } catch (InsufficientFundsException e) {
            System.out.println("余额不足: " + e.getMessage());
        } catch (InvalidAccountException e) {
            System.out.println("账户无效: " + e.getMessage());
        }
    }
    
    /**
     * 取款方法，声明可能抛出受检异常
     * @param accountId 账户ID
     * @param amount 取款金额
     * @throws InsufficientFundsException 余额不足时抛出
     */
    public static void withdraw(String accountId, double amount) 
            throws InsufficientFundsException {
        
        // 验证账户ID（抛出非受检异常）
        if (!VALID_ACCOUNT_ID.equals(accountId)) {
            throw new InvalidAccountException(accountId);
        }
        
        // 验证余额（抛出受检异常）
        if (amount > accountBalance) {
            throw new InsufficientFundsException(accountBalance, amount);
        }
        
        accountBalance -= amount;
        System.out.println("取款成功! 新余额: " + accountBalance);
    }
}
