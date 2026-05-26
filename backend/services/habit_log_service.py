import backend.repositories.habit_log_repository as habit_log_repository 
from datetime import date

def log_habit(habit_id: int, log_date: str):
    habit_log_repository.create(habit_id, date.fromisoformat(log_date))
    
def get_last_7_days(habit_id: int):
    return habit_log_repository.get_last_7_days(habit_id)

def get_today(habit_id: int):
    return habit_log_repository.get_today(habit_id)

def delete_today(habit_id: int):
    habit_log_repository.delete_today(habit_id)
    