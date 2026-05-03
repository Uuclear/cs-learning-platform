public class BankAccount {
    private String accountNumber;
    private String ownerName;
    private double balance;
    private java.util.List<String> transactionHistory;

    // 构造方法
    public BankAccount(String accountNumber, String ownerName, double initialBalance) {
        this.accountNumber = accountNumber;
        this.ownerName = ownerName;
        this.balance = initialBalance >= 0 ? initialBalance : 0;
        this.transactionHistory = new java.util.ArrayList<>();
        if (initialBalance > 0) {
            transactionHistory.add("Initial deposit: $" + initialBalance);
        }
    }

    // Getter 方法
    public String getAccountNumber() {
        return accountNumber;
    }

    public String getOwnerName() {
        return ownerName;
    }

    public double getBalance() {
        return balance;
    }

    public java.util.List<String> getTransactionHistory() {
        return new java.util.ArrayList<>(transactionHistory); // 返回副本以保护内部状态
    }

    // Setter 方法（带验证）
    public void setOwnerName(String ownerName) {
        if (ownerName != null && !ownerName.trim().isEmpty()) {
            this.ownerName = ownerName;
        }
    }

    // 业务方法
    public boolean deposit(double amount) {
        if (amount > 0) {
            balance += amount;
            transactionHistory.add("Deposit: $" + amount);
            return true;
        }
        return false;
    }

    public boolean withdraw(double amount) {
        if (amount > 0 && amount <= balance) {
            balance -= amount;
            transactionHistory.add("Withdrawal: $" + amount);
            return true;
        }
        return false;
    }

    public boolean transfer(BankAccount targetAccount, double amount) {
        if (targetAccount == null || amount <= 0) {
            return false;
        }

        if (withdraw(amount)) {
            targetAccount.deposit(amount);
            transactionHistory.add("Transfer to " + targetAccount.getAccountNumber() + ": $" + amount);
            return true;
        }
        return false;
    }

    @Override
    public String toString() {
        return String.format("Account[%s]: %s, Balance: $%.2f",
                           accountNumber, ownerName, balance);
    }
}