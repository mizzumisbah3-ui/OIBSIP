public class Transaction {


    private String type;
    private double amount;
    private String description;


    public Transaction(String type, double amount, String description) {

        this.type = type;
        this.amount = amount;
        this.description = description;

    }


    @Override
    public String toString() {

        return type + 
        " | Amount: ₹" + amount +
        " | " + description;

    }

}
