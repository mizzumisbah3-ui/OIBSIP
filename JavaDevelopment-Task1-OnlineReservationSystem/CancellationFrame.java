import javax.swing.*;
import java.sql.*;

public class CancellationFrame extends JFrame {

    JTextField pnrField;
    JTextArea details;

    CancellationFrame() {

        setTitle("Cancel Reservation");

        JLabel label = new JLabel("Enter PNR Number");

        pnrField = new JTextField();

        JButton fetchButton = new JButton("Fetch");

        JButton cancelButton = new JButton("Cancel Ticket");

        details = new JTextArea();

        details.setEditable(false);

        label.setBounds(30, 30, 130, 30);

        pnrField.setBounds(160, 30, 120, 30);

        fetchButton.setBounds(300, 30, 80, 30);

        details.setBounds(50, 90, 300, 120);

        cancelButton.setBounds(120, 250, 150, 35);

        add(label);
        add(pnrField);
        add(fetchButton);
        add(details);
        add(cancelButton);

        fetchButton.addActionListener(e -> {

            try {

                Connection con = DatabaseConnection.connect();

                if (con == null) {
                    return;
                }

                String sql = "SELECT * FROM reservations WHERE pnr=?";

                PreparedStatement ps = con.prepareStatement(sql);

                ps.setInt(
                        1,
                        Integer.parseInt(pnrField.getText()));

                ResultSet rs = ps.executeQuery();

                if (rs.next()) {

                    details.setText(
                            "PNR: " + rs.getInt("pnr")
                                    + "\nPassenger: " + rs.getString("passenger")
                                    + "\nTrain Number: " + rs.getInt("train_no")
                                    + "\nTrain Name: " + rs.getString("train_name")
                                    + "\nClass: " + rs.getString("class_type")
                                    + "\nDate: " + rs.getString("journey_date")
                                    + "\nFrom: " + rs.getString("source")
                                    + "\nTo: " + rs.getString("destination"));

                } else {

                    JOptionPane.showMessageDialog(
                            null,
                            "PNR not found");

                }

                rs.close();
                ps.close();
                con.close();

            } catch (Exception ex) {

                JOptionPane.showMessageDialog(
                        null,
                        ex.getMessage());

            }

        });

        cancelButton.addActionListener(e -> {

            int choice = JOptionPane.showConfirmDialog(
                    null,
                    "Are you sure you want to cancel?",
                    "Confirmation",
                    JOptionPane.YES_NO_OPTION);

            if (choice == JOptionPane.YES_OPTION) {

                try {

                    Connection con = DatabaseConnection.connect();

                    if (con == null) {
                        return;
                    }

                    String sql = "DELETE FROM reservations WHERE pnr=?";

                    PreparedStatement ps = con.prepareStatement(sql);

                    ps.setInt(
                            1,
                            Integer.parseInt(pnrField.getText()));

                    int result = ps.executeUpdate();

                    if (result > 0) {

                        JOptionPane.showMessageDialog(
                                null,
                                "Ticket Cancelled Successfully");

                        details.setText("");

                    } else {

                        JOptionPane.showMessageDialog(
                                null,
                                "PNR not found");

                    }

                    ps.close();
                    con.close();

                } catch (Exception ex) {

                    JOptionPane.showMessageDialog(
                            null,
                            ex.getMessage());

                }

            }

        });

        setSize(450, 350);
        setLayout(null);
        setLocationRelativeTo(null);
        setVisible(true);

    }

}
