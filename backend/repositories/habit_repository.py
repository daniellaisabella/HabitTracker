from backend.models.models import Habit
from backend.db import get_db_connection

def get_all():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id,name FROM habits")
    rows= cursor.fetchall()

    cursor.close()
    connection.close()
    
    return [Habit(id=row[0], name=row[1]) for row in rows] #pythons list comprehension

def create(name: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO habits (name) VALUES (%s) RETURNING id", (name,))
    row = cursor.fetchone()
    assert row is not None,"Failed to create habit"
    habit_id = row[0]
    connection.commit()

    cursor.close()
    connection.close()

    return Habit(id=habit_id, name=name)
 

def delete(id: int):
  connection = get_db_connection()
  cursor = connection.cursor()
  cursor.execute("DELETE FROM habits WHERE id = %s",(id,))
  connection.commit()

  cursor.close()
  connection.close()