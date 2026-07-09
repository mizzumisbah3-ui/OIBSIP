# ATM Interface 

## Project Overview

ATM Interface is a console-based ATM simulation application developed using Java and Object-Oriented Programming (OOP) concepts.

The project simulates the basic functionalities of a real ATM system where users can securely log in using their User ID and PIN. After successful authentication, users can perform various banking operations such as withdrawing money, depositing money, transferring funds, checking account balance, and viewing transaction history.

This project demonstrates the practical implementation of Java OOP concepts such as classes, objects, encapsulation, constructors, methods, and ArrayList collections.

---

## Features

### User Authentication
- Users can log in using a unique User ID and PIN.
- The system allows a maximum of 3 incorrect login attempts.
- Access is denied after exceeding the allowed attempts.

### Withdraw Money
- Users can withdraw money from their account.
- The system checks the available balance before processing the withdrawal.
- Displays an "Insufficient Funds" message when the balance is too low.
- Successful withdrawals are recorded in transaction history.

### Deposit Money
- Users can add money to their account.
- The deposited amount is updated in the account balance.
- Deposit transactions are stored for future reference.

### Fund Transfer
- Users can transfer money to another account.
- The system validates the recipient account ID.
- Balance verification is performed before completing the transfer.
- Transfer details are stored in transaction history.

### Transaction History
- All transactions performed during the session are stored using ArrayList.
- Users can view details of previous transactions including transaction type, amount, and description.

### Exit Option
- Users can safely exit the ATM application using the quit option.
- A goodbye message is displayed before closing the program.

---

## Technologies Used
- Java
- OOP Concepts 
- ArrayList 
- Scanner Class

## Project Structure
ATMInterface
│
└── src

├── Main.java
├── ATM.java
├── Account.java
├── Bank.java
└── Transaction.java


### Class Description

**Main.java**
- Acts as the entry point of the application.
- Handles user login process.
- Creates Bank and ATM objects.

**ATM.java**
- Controls ATM operations.
- Displays the menu and manages transactions.
- Handles withdrawal, deposit, transfer, and transaction history.

**Account.java**
- Represents customer account details.
- Stores account ID, User ID, PIN, and balance.
- Provides methods for deposit and withdrawal.

**Bank.java**
- Stores account information.
- Handles user authentication.
- Finds recipient accounts during money transfer.

**Transaction.java**
- Represents individual transaction details.
- Stores transaction type, amount, and description.

---

## Future Enhancements

- Add database connectivity using MySQL
- Create GUI interface using Java Swing or JavaFX
- Add user registration feature
- Store permanent transaction history
- Generate account statements

---

## Author

**Anjum Misbah Z**

