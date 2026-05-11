import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;

public class RepairDb {
    public static void main(String[] args) {
        try {
            Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/near_miss", "postgres", "1234");
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("DELETE FROM flyway_schema_history WHERE version='3';");
            System.out.println("Deleted flyway schema history for version 3.");
            conn.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
