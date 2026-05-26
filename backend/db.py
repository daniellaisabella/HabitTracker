from psycopg2 import pool
import os
from dotenv import load_dotenv
load_dotenv()

_pool: pool.SimpleConnectionPool | None = None

def init_pool():
    global _pool
    _pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def get_db_connection():
    if _pool is None:
        raise RuntimeError("Database pool is not initialized. Call init_pool() first.")
    return _pool.getconn()

def release_connection(conn):
    if _pool is not None:
        _pool.putconn(conn)

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS habits (
                   id SERIAL PRIMARY KEY,
                   name TEXT NOT NULL,
                   created_at TIMESTAMP DEFAULT NOW()
                   );
                     """)
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS habit_log (
                   id SERIAL PRIMARY KEY,
                   habit_id INTEGER REFERENCES habits(id) ON DELETE CASCADE,
                   log_date DATE NOT NULL
                   );
                     """)

    connection.commit()
    cursor.close()
    release_connection(connection)