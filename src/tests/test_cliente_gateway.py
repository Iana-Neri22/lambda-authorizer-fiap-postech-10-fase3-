from ..gateway.cliente_gateway import get_cliente_by_cpf
from ..external.mysql.create_connection import MySQLConnection
import os

def setup_test_database():
    mysql_conn = MySQLConnection()
    # Read and execute create tables SQL
    with open(os.path.join(os.path.dirname(__file__), '../sql/create_tables.sql'), 'r') as f:
        create_tables_sql = f.read()
    
    # Read and execute insert test data SQL
    with open(os.path.join(os.path.dirname(__file__), '../sql/insert_test_data.sql'), 'r') as f:
        insert_data_sql = f.read()
    
    try:
        mysql_conn.execute_query(create_tables_sql)
        mysql_conn.execute_query(insert_data_sql)
        print("Test database setup completed successfully")
    except Exception as e:
        print(f"Error setting up test database: {str(e)}")

def test_get_cliente_by_cpf():
    setup_test_database()

    # Test case 1: Valid CPF that exists in database
    try:
        cpf = "12345678901"
        result = get_cliente_by_cpf(cpf)
        assert result is not None, "Cliente should be found"
        assert result['cpf'] == cpf, "CPF should match"
        assert result['nome'] == "Test User 1", "Nome should match"
        print(f"Test 1 - Valid CPF passed: {result}")
    except Exception as e:
        print(f"Test 1 failed: {str(e)}")

    # Test case 2: CPF that doesn't exist in database
    try:
        cpf = "99999999999"
        result = get_cliente_by_cpf(cpf)
        assert result is None, "Should return None for non-existent CPF"
        print("Test 2 - Non-existent CPF passed")
    except Exception as e:
        print(f"Test 2 failed: {str(e)}")

    # Test case 3: Invalid CPF format
    try:
        cpf = "123"  # Invalid CPF format
        result = get_cliente_by_cpf(cpf)
        print("Test 3 - Invalid CPF format passed")
    except Exception as e:
        print(f"Test 3 failed: {str(e)}")

if __name__ == "__main__":
    test_get_cliente_by_cpf() 