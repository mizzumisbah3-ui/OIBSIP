import javax.swing.*;

public class LoginFrame extends JFrame {

    JTextField username;
    JPasswordField password;

    LoginFrame() {

        setTitle("Online Reservation System - Login");

        JLabel userLabel = new JLabel("Username");
        JLabel passLabel = new JLabel("Password");

        username = new JTextField();
        password = new JPasswordField();

        JButton loginButton = new JButton("Login");

        userLabel.setBounds(40, 50, 100, 30);
        username.setBounds(150, 50, 150, 30);

        passLabel.setBounds(40, 100, 100, 30);
        password.setBounds(150, 100, 150, 30);

        loginButton.setBounds(120, 160, 100, 30);

        add(userLabel);
        add(username);

        add(passLabel);
        add(password);

        add(loginButton);

        loginButton.addActionListener(e -> {

            String user = username.getText();
            String pass = String.valueOf(password.getPassword());

            if (user.equals("admin") && pass.equals("1234")) {

                JOptionPane.showMessageDialog(
                        null,
                        "Login Successful");

                new ReservationFrame();

                dispose();

            } else {

                JOptionPane.showMessageDialog(
                        null,
                        "Invalid Username or Password");

            }

        });

        setSize(350, 250);
        setLayout(null);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setVisible(true);

    }

}
