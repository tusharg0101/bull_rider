# test_db_connection.py

import pymysql
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

host = os.getenv('SINGLESTORE_HOST')
user = os.getenv('SINGLESTORE_USER')
password = os.getenv('SINGLESTORE_PASSWORD')
database = os.getenv('SINGLESTORE_DB')
port = os.getenv('SINGLESTORE_PORT')

print("Testing database connection with the following parameters:")
print(f"Host: {host}")
print(f"Port: {port}")
print(f"User: {user}")
print(f"Database: {database}")

def get_ssl_cert_path():
    project_root = os.path.dirname(os.path.abspath(__file__))
    cert_path = os.path.join(project_root, 'certs', 'singlestore_bundle.pem')
    print(f"SSL cert path: {cert_path}")
    if not os.path.isfile(cert_path):
        print("ERROR: SSL certificate file not found at the specified path.")
    return cert_path

try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=int(port),
        ssl={
            'ca': get_ssl_cert_path()
        }
    )
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print(f"Database connection failed: {e}")
    print("Exception type:", type(e))
    print("Exception args:", e.args)
    traceback.print_exc()
