import pymysql
import os

# Function to get the absolute path of the PEM file relative to the project root
def get_ssl_cert_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(project_root, 'certs/singlestore_bundle.pem')

    if not os.path.exists(cert_path):
        print("ERROR: SSL certificate not found.")
    return cert_path

# Function to create a connection to SingleStore with SSL
def get_singlestore_connection():
    host = os.getenv('SINGLESTORE_HOST')
    user = os.getenv('SINGLESTORE_USER')
    password = os.getenv('SINGLESTORE_PASSWORD')
    database = os.getenv('SINGLESTORE_DB')
    port = os.getenv('SINGLESTORE_PORT')
    
    # Check for missing environment variables
    missing_vars = []
    for var_name, var_value in [('SINGLESTORE_HOST', host), ('SINGLESTORE_USER', user),
                                ('SINGLESTORE_PASSWORD', password), ('SINGLESTORE_DB', database),
                                ('SINGLESTORE_PORT', port)]:
        if not var_value:
            missing_vars.append(var_name)
    if missing_vars:
        raise ValueError(f"Missing environment variables: {', '.join(missing_vars)}")

    port = int(port)  # Convert port to integer

    # Create a connection to SingleStore
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
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
            sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                voice_hash_1 LONGTEXT NOT NULL,
                voice_hash_2 LONGTEXT NOT NULL,
                voice_hash_3 LONGTEXT NOT NULL,
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
