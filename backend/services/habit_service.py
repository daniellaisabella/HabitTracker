from backend.repositories.habit_repository import HabitRepository, HabitEntryRepository
from backend.models import SessionLocal
from sqlalchemy.exc import IntegrityError

class HabitService:
    @staticmethod
    def list_habits():
        db = SessionLocal()
        habits = HabitRepository.get_all(db)
        result = [{"id": h.id, "name": h.name} for h in habits]
        db.close()
        return result

    @staticmethod
    def create_habit(name: str):
        db = SessionLocal()
        try:
            habit = HabitRepository.create(db, name)
            db.commit()
            result = {"id": habit.id, "name": habit.name}
        except IntegrityError:
            db.rollback()
            result = {"error": "Habit already exists"}
        finally:
            db.close()
        return result

    @staticmethod
    def delete_habit(name: str):
        db = SessionLocal()
        habit = HabitRepository.get_by_name(db, name)
        if not habit:
            db.close()
            return {"error": "Habit not found"}
        HabitRepository.delete(db, habit)
        db.commit()
        db.close()
        return {"status": "deleted", "habit": name}

    @staticmethod
    def mark_done(name: str):
        db = SessionLocal()
        habit = HabitRepository.get_by_name(db, name)
        if not habit:
            db.close()
            return {"error": "Habit not found"}
        HabitEntryRepository.create_or_update_done(db, habit.id, done=True)
        db.commit()
        db.close()
        return {"status": "ok", "habit": name}
