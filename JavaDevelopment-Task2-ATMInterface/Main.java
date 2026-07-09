import java.util.Scanner;


public class Main {


    public static void main(String[] args) {


        Scanner sc = new Scanner(System.in);


        Bank bank = new Bank();


        Account account = null;


        int attempts = 0;



        while(attempts < 3) {


            System.out.print("Enter User ID: ");

            String userId = sc.next();



            System.out.print("Enter PIN: ");

            int pin = sc.nextInt();



            account = bank.login(userId,pin);



            if(account != null) {


                System.out.println("Login Successful");


                ATM atm = new ATM(account,bank);


                atm.start();


                break;


            }


            else {


                attempts++;


                System.out.println(
                    "Invalid Login Attempt "
                    + attempts + "/3"
                );


            }


        }



        if(account == null) {


            System.out.println(
                "Access Denied"
            );


        }


        sc.close();


    }

}
