from backend.models import SessionLocal, Habit, HabitEntry
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

# Habit repository
class HabitRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Habit).all()

    @staticmethod
    def get_by_name(db: Session, name: str):
        return db.query(Habit).filter_by(name=name).first()

    @staticmethod
    def get_by_id(db: Session, habit_id: int):
        return db.query(Habit).filter_by(id=habit_id).first()

    @staticmethod
    def create(db: Session, name: str):
        habit = Habit(name=name)
        db.add(habit)
        return habit

    @staticmethod
    def delete(db: Session, habit: Habit):
        db.delete(habit)

# HabitEntry repository
class HabitEntryRepository:
    @staticmethod
    def get_today_entry(db: Session, habit_id: int):
        today = date.today()
        return db.query(HabitEntry).filter_by(habit_id=habit_id, date=today).first()

    @staticmethod
    def create_or_update_done(db: Session, habit_id: int, done: bool = True):
        today = date.today()
        entry = db.query(HabitEntry).filter_by(habit_id=habit_id, date=today).first()
        if entry:
            entry.done = done
        else:
            entry = HabitEntry(habit_id=habit_id, date=today, done=done)
            db.add(entry)
        return entry

    @staticmethod
    def delete_all_for_habit(db: Session, habit_id: int):
        db.query(HabitEntry).filter_by(habit_id=habit_id).delete()
