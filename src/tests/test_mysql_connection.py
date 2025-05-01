from ..external.mysql.create_connection import MySQLConnection

def test_connection():
    try:
        # Initialize connection
        mysql_conn = MySQLConnection()
        
        # Test a simple query
        result = mysql_conn.execute_query("SELECT 1")
        print("Connection successful! Query result:", result)
        
    except Exception as e:
        print("Connection failed:", str(e))

if __name__ == "__main__":
    test_connection() 