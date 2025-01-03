import mysql.connector

# Configure database connection
DB_CONFIG = {
    'host': 'localhost',       # MySQL host
    'user': 'root',            # MySQL user
    'password': '',  # MySQL password
    'database': 'book_store'   # MySQL database name
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        raise
