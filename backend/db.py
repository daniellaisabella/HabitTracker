import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def create_tables():
    connection = get_db_connection()    
    cursor = connection.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS habits (
                   id SERIAL PRIMARY KEY, 
                   name TEXT NOT NULL
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
    connection.close()