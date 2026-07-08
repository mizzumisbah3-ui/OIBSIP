# Online Reservation System

## Overview

The **Online Reservation System** is a GUI-based desktop application developed using **Java Swing** and **SQLite Database**. The project is designed to simplify the process of train ticket booking and cancellation through an easy-to-use graphical interface.

The application allows users to securely log in, enter passenger details, select train information, book tickets, generate a unique PNR number, view reservation details, and cancel bookings using the generated PNR number.

This project demonstrates the practical implementation of **Java GUI development, JDBC database connectivity, SQL operations, and event-driven programming**.

---

## Objectives

- To develop a user-friendly railway reservation system using Java Swing.
- To implement database connectivity using JDBC and SQLite.
- To store and manage passenger reservation details efficiently.
- To generate unique PNR numbers automatically for each booking.
- To provide ticket cancellation functionality using PNR numbers.

---

## Features

### User Login Authentication
- Provides a login interface with username and password fields.
- Allows access only for valid credentials.
- Prevents unauthorized access to the reservation system.

### Ticket Reservation
- Allows users to enter passenger information.
- Accepts train number, train name, class type, journey date, source, and destination details.
- Stores reservation data securely in the SQLite database.

### Automatic PNR Generation
- Generates a unique PNR number automatically after successful booking.
- Displays booking confirmation along with the generated PNR number.

### Booking Confirmation
- Shows a success message after ticket reservation.
- Provides the user with booking reference details.

### Ticket Cancellation
- Allows users to enter their PNR number.
- Retrieves complete booking details from the database.
- Provides confirmation before cancelling the ticket.
- Removes the reservation record after successful cancellation.

### Database Integration
- Uses SQLite database for storing reservation records.
- Implements JDBC for communication between Java application and database.
- Uses SQL queries for inserting, retrieving, and deleting records.

---

## Technologies Used

### Programming Language
- Java

### GUI Framework
- Java Swing

### Database
- SQLite

### Database Connectivity
- JDBC (Java Database Connectivity)

### Development Environment
- Visual Studio Code

### Java Version
- JDK 21

---

## Project Structure
OnlineReservationSystem

│
├── src
│ ├── Main.java
│ ├── DatabaseConnection.java
│ ├── LoginFrame.java
│ ├── ReservationFrame.java
│ └── CancellationFrame.java
│
├── lib
│ └── sqlite-jdbc.jar
│
└── reservation.db


## The table stores:

- PNR Number
- Passenger Name
- Train Number
- Train Name
- Class Type
- Journey Date
- Source Station
- Destination Station

---

## Learning Outcomes

Through this project, I gained practical experience in:

- Java Swing GUI development
- JDBC database connectivity
- SQLite database management
- SQL queries and CRUD operations
- Exception handling
- Event-driven programming
- Building desktop applications using Java

---

## Future Enhancements

- Add online payment integration.
- Add admin dashboard for managing reservations.
- Add train search functionality.
- Add user registration system.
- Improve UI design with JavaFX.

---

## Author

**Anjum Misbah Z**
