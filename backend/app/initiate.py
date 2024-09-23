import mysql.connector
from faker import Faker
from os import getenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Establish connection to the MySQL server
def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if connection.is_connected():
            logging.info("Connection to MySQL DB successful")
            return connection
        else:
            raise mysql.connector.Error("Connection to MySQL DB failed")
    except mysql.connector.Error as e:
        logging.error(f"The Exception '{e}' occurred")
        raise

# Execute a query
def execute_query(connection, query, data=None):
    if connection is None:  # Check if connection is valid
        logging.error("No valid connection. Cannot execute query.")
        return None
    cursor = connection.cursor()
    try:
        if data is None:
            cursor.execute(query)
        elif isinstance(data[0], tuple):
            cursor.executemany(query, data)
        else:
            cursor.execute(query, data)

        if cursor.with_rows:  # Check if the query has a result set
            result = cursor.fetchall()
            return result
        
        connection.commit()
        status_message = {
            "message": "Query OK",
            "rows_matched": cursor.rowcount,  # Rows matched would be the same as affected in most cases
            "warnings": [] if cursor.warning_count else cursor.warnings,  # Fetch warnings, if any
            "query": query.strip().replace('\n', ' ').strip(),
            "data": data
        }
        return status_message
    except Exception as e:
        logging.error("While executing"+query.strip().replace('\n', ' ').strip()[:100])
        logging.error(f"The Exception '{e}' occurred")
        raise
    finally:
        cursor.close()  # Ensure the cursor is closed after use

def retrieve_connection(
    host_name=getenv('MYSQL_HOST','127.0.0.1'),  # Use 'mysql' as hostname within Docker network
    user_name=getenv('MYSQL_USER','root'),
    user_password=getenv('MYSQL_PASSWORD','password'),
    db_name=getenv('MYSQL_DATABASE','hospital_db')
):
    connection = create_connection(host_name, user_name, user_password, db_name)
    if connection.is_connected():
        return connection
    else:
        raise mysql.connector.Error("Connection to MySQL DB failed")

if __name__ == '__main__':

    connection = retrieve_connection()
    
    # Create Database
    execute_query(connection, "CREATE DATABASE IF NOT EXISTS attendance_db")
    execute_query(connection, "USE attendance_db")
    execute_query(connection, """
                  CREATE TABLE IF NOT EXISTS attendance
                  """)
    
    connection.close()
