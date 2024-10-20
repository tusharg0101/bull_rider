import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Function to get the absolute path of the PEM file relative to the project root
def get_ssl_cert_path():
    # Get the absolute path of the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    # Return the path to the PEM file relative to the current script
    return os.path.join(project_root, '../certs/singlestore_bundle.pem')

# Function to create a connection to SingleStore with SSL
def get_singlestore_connection():
    print(f"Connecting to host: {os.getenv('SINGLESTORE_HOST')}")
    connection = pymysql.connect(
        host=os.getenv('SINGLESTORE_HOST'),
        user=os.getenv('SINGLESTORE_USER'),
        password=os.getenv('SINGLESTORE_PASSWORD'),
        database=os.getenv('SINGLESTORE_DB'),
        port=int(os.getenv('SINGLESTORE_PORT', 3306)),  # Use the correct port for SingleStore (typically 3306)
        cursorclass=pymysql.cursors.DictCursor,
        ssl={
            'ca': get_ssl_cert_path()  # Use relative path to the PEM file
        }
    )
    return connection

# Function to create the users table
def create_users_table():
    connection = get_singlestore_connection()
    try:
        with connection.cursor() as cursor:
            # SQL command to create the users table
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                voice_hash_1 VARCHAR(255) NOT NULL,
                voice_hash_2 VARCHAR(255) NOT NULL,
                voice_hash_3 VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            cursor.execute(sql)
            connection.commit()
            print("Users table created successfully.")
    finally:
        connection.close()

# Example function to test the connection
def test_singlestore_connection():
    connection = get_singlestore_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            result = cursor.fetchone()
            print(f"Connected to database: {result['DATABASE()']}")
    finally:
        connection.close()

# Call this function to create the users table
if __name__ == "__main__":
    create_users_table()
    test_singlestore_connection()
