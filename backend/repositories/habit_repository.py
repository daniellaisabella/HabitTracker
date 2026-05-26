from backend.models.models import Habit
from backend.db import get_db_connection, release_connection

def get_all():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, created_at FROM habits")
        rows = cursor.fetchall()
        cursor.close()
        return [Habit(id=row[0], name=row[1], created_at=row[2]) for row in rows]
    finally:
        release_connection(connection)

def create(name: str):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO habits (name) VALUES (%s) RETURNING id, created_at", (name,))
        row = cursor.fetchone()
        if row is None:
            raise RuntimeError("Failed to create habit")
        connection.commit()
        cursor.close()
        return Habit(id=row[0], name=name, created_at=row[1])
    finally:
        release_connection(connection)

def delete(id: int):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM habits WHERE id = %s", (id,))
        connection.commit()
        cursor.close()
    finally:
        release_connection(connection)