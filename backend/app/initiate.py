# initiate.py
import mysql.connector
from os import getenv
import logging
import time

MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def create_connection(host_name, user_name, user_password, db_name=None):
    connection = None
    for attempt in range(MAX_RETRIES):
        try:
            connection = mysql.connector.connect(
                host=host_name,
                port=3307,
                user=user_name,
                password=user_password,
                database=db_name
            )
            if connection.is_connected():
                logging.info("Connection to MySQL DB successful")
                return connection
        except mysql.connector.Error as e:
            logging.error(f"Attempt {attempt + 1}: The Exception '{e}' occurred")
            if e.errno == 1049:  # Error: Unknown database
                logging.info(f"Database '{db_name}' not found yet. Retrying in {RETRY_DELAY} seconds...")
            time.sleep(RETRY_DELAY)
        if attempt == MAX_RETRIES - 1:
            raise mysql.connector.Error(f"Unable to connect to database after {MAX_RETRIES} attempts.")
    return connection

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

def retrieve_connection():
    host_name = getenv('MYSQL_HOST', '127.0.0.1')
    user_name = getenv('MYSQL_USER', 'root')
    user_password = getenv('MYSQL_PASSWORD', 'password')
    db_name = getenv('MYSQL_DATABASE', 'attendance_db')
    return create_connection(host_name, user_name, user_password, db_name)

if __name__ == '__main__':
    students = [
    (1, 'ANURAG SAISH'), (2, 'VIVEK KUMAR PANDEY'), (3, 'NAVYAA KABRA'), (4, 'ISHAN GAUTAM'),
    (5, 'MOLIK JAIN'), (6, 'PRIYANSH GOEL'), (7, 'PARTH RAI'), (8, 'REETIKA AGRAWAL'),
    (9, 'HAMZA IKRAM'), (10, 'PRANAV TYAGI'), (11, 'MAURVI GUPTA'), (12, 'ADITYA SINGH'),
    (13, 'DIVYENDU SINGH BHATI'), (14, 'HARSHIT RASTOGI'), (15, 'SPARSH GARG'), (16, 'GAURAV KUMAR'),
    (17, 'ANAHAT GILL'), (18, 'SHIVANK GOEL'), (19, 'ARNAV KAWATRA'), (20, 'JIYA GUPTA'),
    (21, 'ARNAV JAIN'), (22, 'SHIVANSH PRADHAN'), (23, 'RISHITA RAI'), (24, 'ARVIND NAIR'),
    (25, 'YASH KUMAR'), (26, 'ANUSHKA PAWAR'), (27, 'ANJANEY'), (28, 'YUVRAJ SINGH ROPERIA'),
    (29, 'AADRIAN ROUTH'), (30, 'DAKSH SHARMA'), (31, 'TAARUSH KATHURIA'), (32, 'ARYAN BALODI'),
    (33, 'TALLURI MEHER LAKSHMI KANTH'), (34, 'VEDANT NARANG'), (35, 'ANSH BHARADWAJ'), 
    (36, 'ROHAN RAJ'), (37, 'ABHINAV CHAUDHRY'), (38, 'ANUSHKA SANJAY JHA'), 
    (39, 'KSHITIJ SINGH PATHANIA'), (40, 'SHIVEN AGARWAL'), (41, 'HARMANN SINGH BHOMRAH'), 
    (42, 'DHEERAJ KUMAR'), (43, 'PRANIT KHANDELWAL'), (44, 'AYUSH YADAV'), 
    (45, 'SRIVATSA VENKATA SAI PALEPU'), (46, 'ABHINAV MISHRA'), (47, 'AAYUSH BHUSHAN DNYANE'), 
    (48, 'SAUMYA RISHIKESH'), (49, 'KARAN KAPOOR'), (50, 'MALI SWARAJ VINOD'), 
    (51, 'ISHAAN MANISH DHAWAN'), (52, 'MOHIT SOLANKI'), (53, 'ARYAN CHAWLA'), 
    (54, 'VEDIC VARMA'), (55, 'KHUSHI PARWAL'), (56, 'SAUMITRA JAI PRAKASH SRIVASTAVA'), 
    (57, 'TAANYA VIPUL TAPKE'), (58, 'MAYANK MAHESHWARI'), (59, 'RAGHAV AGARWAL'), 
    (60, 'A AAKASH'), (61, 'NISHANT TIWARI')
]
    connection = retrieve_connection()

    execute_query(connection,"""CREATE DATABASE IF NOT EXISTS attendance_db;""")
    execute_query(connection, "USE attendance_db;")
    # Create Students table
    create_students_table = """
    CREATE TABLE IF NOT EXISTS Students (
        student_id INT PRIMARY KEY AUTO_INCREMENT,
        student_name VARCHAR(40) NOT NULL,
        attendance BOOLEAN NOT NULL DEFAULT 0
    );
    """
    execute_query(connection, create_students_table)
    # Create the AttendanceIP table to track IPs
    execute_query(connection, """
                  CREATE TABLE IF NOT EXISTS AttendanceIP (
                      ip_address VARCHAR(45) PRIMARY KEY,
                      mark_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  );
                  """)

    # Clear IP tracking table on restart
    execute_query(connection, "TRUNCATE TABLE AttendanceIP;")

    insert_student_query = "INSERT INTO Students (student_id, student_name) VALUES (%s, %s)"
    try:
        for student in students:
            execute_query(connection, insert_student_query, student)
        logging.info("Inserted all students with IDs into the Students table")
    except Exception as e:
        logging.error(f"Error inserting students: {e}")
    finally:
        connection.close()


    logging.info("Database and tables are set up")
    connection.close()
