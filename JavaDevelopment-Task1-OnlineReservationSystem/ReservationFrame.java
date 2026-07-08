import javax.swing.*;
import java.sql.*;

public class ReservationFrame extends JFrame {

    JTextField passengerName;
    JTextField trainNumber;
    JTextField journeyDate;
    JTextField source;
    JTextField destination;

    JComboBox<String> trainName;
    JComboBox<String> classType;

    ReservationFrame() {

        setTitle("Train Reservation");

        JLabel l1 = new JLabel("Passenger Name");
        JLabel l2 = new JLabel("Train Number");
        JLabel l3 = new JLabel("Train Name");
        JLabel l4 = new JLabel("Class Type");
        JLabel l5 = new JLabel("Journey Date");
        JLabel l6 = new JLabel("Source");
        JLabel l7 = new JLabel("Destination");

        passengerName = new JTextField();
        trainNumber = new JTextField();
        journeyDate = new JTextField();
        source = new JTextField();
        destination = new JTextField();

        trainName = new JComboBox<>();

        trainName.addItem("Chennai Express");
        trainName.addItem("Pandian Express");
        trainName.addItem("Rajdhani Express");

        classType = new JComboBox<>();

        classType.addItem("Sleeper");
        classType.addItem("AC");
        classType.addItem("General");

        JButton bookButton = new JButton("Book Ticket");

        int y = 30;

        JLabel[] labels = {
                l1, l2, l3, l4, l5, l6, l7
        };

        JComponent[] fields = {
                passengerName,
                trainNumber,
                trainName,
                classType,
                journeyDate,
                source,
                destination
        };

        for (int i = 0; i < labels.length; i++) {

            labels[i].setBounds(30, y, 120, 30);

            fields[i].setBounds(160, y, 180, 30);

            add(labels[i]);
            add(fields[i]);

            y += 40;
        }

        bookButton.setBounds(80, 330, 130, 35);

        add(bookButton);

        JButton cancelButton = new JButton("Cancel Ticket");

        cancelButton.setBounds(230, 330, 130, 35);

        add(cancelButton);

        cancelButton.addActionListener(e -> {

            new CancellationFrame();

        });
        bookButton.addActionListener(e -> {

            try {

                if (passengerName.getText().isEmpty()
                        || trainNumber.getText().isEmpty()
                        || journeyDate.getText().isEmpty()
                        || source.getText().isEmpty()
                        || destination.getText().isEmpty()) {

                    JOptionPane.showMessageDialog(
                            null,
                            "Please fill all fields");

                    return;

                }

                Integer.parseInt(trainNumber.getText());

                Connection con = DatabaseConnection.connect();

                if (con == null) {

                    JOptionPane.showMessageDialog(
                            null,
                            "Database connection failed");

                    return;
                }

                String sql = "INSERT INTO reservations(passenger,train_no,train_name,class_type,journey_date,source,destination) VALUES(?,?,?,?,?,?,?)";

                PreparedStatement ps = con.prepareStatement(
                        sql,
                        Statement.RETURN_GENERATED_KEYS);

                ps.setString(1,
                        passengerName.getText());

                ps.setInt(2,
                        Integer.parseInt(trainNumber.getText()));

                ps.setString(3,
                        trainName.getSelectedItem().toString());

                ps.setString(4,
                        classType.getSelectedItem().toString());

                ps.setString(5,
                        journeyDate.getText());

                ps.setString(6,
                        source.getText());

                ps.setString(7,
                        destination.getText());

                ps.executeUpdate();

                ResultSet rs = ps.getGeneratedKeys();

                if (rs.next()) {

                    JOptionPane.showMessageDialog(
                            null,
                            "Reservation Successful\nYour PNR Number: "
                                    + rs.getInt(1));

                }

            } catch (NumberFormatException ex) {

                JOptionPane.showMessageDialog(
                        null,
                        "Train number must be numeric");

            } catch (Exception ex) {

                JOptionPane.showMessageDialog(
                        null,
                        ex.getMessage());

            }

        });

        setSize(450, 500);
        setLayout(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);

    }

}
