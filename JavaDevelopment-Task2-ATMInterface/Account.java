public class Account {

    private String accountId;
    private String userId;
    private int pin;
    private double balance;


    public Account(String accountId, String userId, int pin, double balance) {

        this.accountId = accountId;
        this.userId = userId;
        this.pin = pin;
        this.balance = balance;

    }


    public String getAccountId() {
        return accountId;
    }


    public String getUserId() {
        return userId;
    }


    public int getPin() {
        return pin;
    }


    public double getBalance() {
        return balance;
    }


    public void deposit(double amount) {

        balance = balance + amount;

    }


    public boolean withdraw(double amount) {

        if(balance >= amount) {

            balance = balance - amount;
            return true;

        }

        return false;

    }

}
