from backend.db import get_db_connection
from datetime import date
from backend.models.models import HabitLog

def create(habit_id: int, log_date: date):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO habit_log (habit_id, log_date) VALUES (%s, %s)", (habit_id, log_date))
    connection.commit()

    cursor.close()
    connection.close()

def get_last_7_days(habit_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
                   SELECT id, habit_id, log_date 
                   FROM habit_log 
                   WHERE habit_id = %s 
                   AND log_date >= CURRENT_DATE - INTERVAL '7 days'
                   """, (habit_id,))
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [HabitLog(id=row[0], habit_id=row[1], log_date=row[2]) for row in rows]

def get_today(habit_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id FROM habit_log 
        WHERE habit_id = %s AND log_date = CURRENT_DATE
    """, (habit_id,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    return True if row else False

def delete_today(habit_id: int):    
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM habit_log 
        WHERE habit_id = %s AND log_date = CURRENT_DATE
    """, (habit_id,))
    connection.commit()
    cursor.close()
    connection.close()