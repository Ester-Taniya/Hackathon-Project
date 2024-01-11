import psycopg2
import os
from dotenv import load_dotenv

def get_db_connection():
    load_dotenv()
    db_name = os.getenv('DB_name')
    db_user = os.getenv('DB_user')
    db_password = os.getenv('DB_password')
    db_host = os.getenv('DB_host')
    db_port = os.getenv('DB_port')

    conn = psycopg2.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    return conn

if __name__ == "__main__":
    get_db_connection()