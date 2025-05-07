from src.external.mysql.create_connection import MySQLConnection

def get_cliente_by_cpf(cpf: str):
    mysql_conn = MySQLConnection()
    connection = mysql_conn.get_connection()
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM Cliente WHERE cpfCliente = %s"
        cursor.execute(query, (cpf,))
        return cursor.fetchone()
    finally:
        cursor.close()
        connection.close()

