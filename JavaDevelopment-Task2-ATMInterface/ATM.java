import java.util.ArrayList;
import java.util.Scanner;

public class ATM {

    private Account account;
    private Bank bank;
    private ArrayList<Transaction> history;
    private Scanner sc;


    public ATM(Account account, Bank bank) {

        this.account = account;
        this.bank = bank;
        this.history = new ArrayList<>();
        this.sc = new Scanner(System.in);

    }


    public void start() {

        int choice;


        do {

            System.out.println("\n===== ATM MENU =====");
            System.out.println("1. Transaction History");
            System.out.println("2. Withdraw");
            System.out.println("3. Deposit");
            System.out.println("4. Transfer");
            System.out.println("5. Check Balance");
            System.out.println("6. Quit");


            System.out.print("Enter choice: ");
            choice = sc.nextInt();



            switch(choice) {


                case 1:

                    System.out.println("\n===== Transaction History =====");


                    if(history.isEmpty()) {

                        System.out.println("No transactions found");

                    } 
                    else {

                        for(Transaction transaction : history) {

                            System.out.println(transaction);

                        }

                    }

                    break;



                case 2:

                    System.out.print("Enter withdrawal amount: ");
                    double withdrawAmount = sc.nextDouble();


                    if(withdrawAmount <= 0) {

                        System.out.println("Invalid amount");

                    }
                    else if(account.withdraw(withdrawAmount)) {


                        history.add(
                            new Transaction(
                                "Withdraw",
                                withdrawAmount,
                                "Withdrawal successful"
                            )
                        );


                        System.out.println("Withdrawal Successful");


                    }
                    else {

                        System.out.println("Insufficient Funds");

                    }

                    break;



                case 3:

                    System.out.print("Enter deposit amount: ");
                    double depositAmount = sc.nextDouble();


                    if(depositAmount <= 0) {

                        System.out.println("Invalid amount");

                    }
                    else {


                        account.deposit(depositAmount);


                        history.add(
                            new Transaction(
                                "Deposit",
                                depositAmount,
                                "Deposit successful"
                            )
                        );


                        System.out.println("Deposit Successful");

                    }

                    break;




                case 4:

                    System.out.print("Enter recipient account ID: ");
                    String receiverId = sc.next();


                    Account receiver = bank.getAccount(receiverId);


                    System.out.print("Enter transfer amount: ");
                    double transferAmount = sc.nextDouble();



                    if(receiver == null) {

                        System.out.println("Account not found");

                    }
                    else if(transferAmount <= 0) {

                        System.out.println("Invalid amount");

                    }
                    else if(account.withdraw(transferAmount)) {


                        receiver.deposit(transferAmount);


                        history.add(
                            new Transaction(
                                "Transfer",
                                transferAmount,
                                "Transferred to " + receiverId
                            )
                        );


                        System.out.println("Transfer Successful");


                    }
                    else {

                        System.out.println("Insufficient Funds");

                    }


                    break;




                case 5:

                    System.out.println(
                        "Current Balance: ₹" + account.getBalance()
                    );

                    break;




                case 6:

                    System.out.println(
                        "Thank you for using ATM"
                    );

                    break;



                default:

                    System.out.println("Invalid choice");

            }



        } while(choice != 6);


    }

}
