import os
import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

# Database connection utility for the user chat DB
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST")
    )

# Database connection utility for the Percieve DB
def get_percieve_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("POSTGRES_DB_PN"),
        user=os.getenv("PN_DB_USER"),
        password=os.getenv("PN_DB_PASSWORD"),
        host=os.getenv("PN_DB_HOST")
    )


def get_database_connection():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
