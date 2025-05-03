import os
import pymysql
from pymysql import Error
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection is None:
            self._initialize_connection()

    def _initialize_connection(self):
        try:
            self._connection = pymysql.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE'),
                port=int(os.getenv('MYSQL_PORT')),
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=5
            )
            logger.info("MySQL connection initialized successfully")
        except Error as e:
            logger.error(f"Error initializing MySQL connection: {e}")
            raise

    def get_connection(self):
        if not self._connection or not self._connection.open:
            self._initialize_connection()
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            self._connection = None

    def execute_query(self, query, params=None):
        connection = None
        cursor = None
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            connection.commit()
            return cursor.rowcount
        except Error as e:
            if connection:
                connection.rollback()
            logger.error(f"Error executing query: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# Example usage:
# mysql_conn = MySQLConnection()
# result = mysql_conn.execute_query("SELECT * FROM your_table")
