import java.util.ArrayList;


public class Bank {


    private ArrayList<Account> accounts;


    public Bank() {


        accounts = new ArrayList<>();


        accounts.add(
            new Account("1001","Anjum",1234,5000)
        );


        accounts.add(
            new Account("1002","User2",5678,3000)
        );


    }



    public Account login(String userId,int pin) {


        for(Account account : accounts) {


            if(account.getUserId().equals(userId)
            && account.getPin()==pin) {


                return account;

            }

        }


        return null;

    }



    public Account getAccount(String id) {


        for(Account account : accounts) {


            if(account.getAccountId().equals(id)) {

                return account;

            }

        }


        return null;

    }


}
