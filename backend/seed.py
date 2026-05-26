import random
from backend.db import get_db_connection, init_pool
from datetime import date, timedelta

def seed():
    conn = get_db_connection()
    cursor = conn.cursor()

    # ryd eksisterende data
    cursor.execute("DELETE FROM habit_log")
    cursor.execute("DELETE FROM habits")

    # opret habits
    habits = ["Sport for 1h", "Drink water", "Study for 2h", "Meditation", "Sleep 8h"]
    habit_ids = []

    for name in habits:
        cursor.execute("INSERT INTO habits (name, created_at) VALUES (%s, NOW() - INTERVAL '7 days') RETURNING id", (name,))
        habit_ids.append(cursor.fetchone()[0])

    # opret logs for de sidste 7 dage
    for habit_id in habit_ids:
        for i in range(7):
            log_date = date.today() - timedelta(days=i)
            if random.random() > 0.3:  # 70% chance for done
                cursor.execute(
                    "INSERT INTO habit_log (habit_id, log_date) VALUES (%s, %s)",
                    (habit_id, log_date)
                )

    conn.commit()
    cursor.close()
    conn.close()
    print("Seed done!")

if __name__ == "__main__":
    init_pool()
    seed()