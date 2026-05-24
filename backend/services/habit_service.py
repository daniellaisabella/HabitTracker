import backend.repositories.habit_repository as habit_repository

def create(name:str):
    if not name:    
        raise ValueError("Write your desired habit")
    return habit_repository.create(name)

def get_all():
    return habit_repository.get_all()

def delete(habit_id: int):
    habit_repository.delete(habit_id)
    