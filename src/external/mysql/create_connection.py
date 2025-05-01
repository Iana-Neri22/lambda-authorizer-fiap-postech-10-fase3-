import os
import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MySQLConnection:
    _instance = None
    _pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MySQLConnection, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if self._pool is None:
            self._initialize_pool()

    def _initialize_pool(self):
        try:
            db_config = {
                'host': os.getenv('MYSQL_HOST'),
                'user': os.getenv('MYSQL_USER'),
                'password': os.getenv('MYSQL_PASSWORD'),
                'database': os.getenv('MYSQL_DATABASE'),
                'port': int(os.getenv('MYSQL_PORT')),
                'pool_name': 'mypool',
                'pool_size': int(os.getenv('MYSQL_POOL_SIZE', 5)),
                'pool_reset_session': True
            }

            self._pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)
            logger.info("MySQL connection pool initialized successfully")
        except Error as e:
            logger.error(f"Error initializing MySQL connection pool: {e}")
            raise

    def get_connection(self):
        try:
            connection = self._pool.get_connection()
            return connection
        except Error as e:
            logger.error(f"Error getting connection from pool: {e}")
            raise

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
