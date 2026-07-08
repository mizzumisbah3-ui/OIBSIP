import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class DatabaseConnection {

    private static final String URL = "jdbc:sqlite:reservation.db";

    public static Connection connect() {

        try {

            Class.forName("org.sqlite.JDBC");

            Connection con = DriverManager.getConnection(URL);

            Statement stmt = con.createStatement();

            String sql = "CREATE TABLE IF NOT EXISTS reservations (" +
                    "pnr INTEGER PRIMARY KEY AUTOINCREMENT," +
                    "passenger TEXT," +
                    "train_no INTEGER," +
                    "train_name TEXT," +
                    "class_type TEXT," +
                    "journey_date TEXT," +
                    "source TEXT," +
                    "destination TEXT" +
                    ")";

            stmt.execute(sql);

            System.out.println("Database Connected");

            stmt.close();
            
            return con;

        } catch (Exception e) {

            e.printStackTrace();

        }

        return null;
    }
}
