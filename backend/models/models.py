from datetime import date
class Habit:
    # __init__ (konstruktor) method to initialize the habit object, self er ligesom this i Java
    def __init__ (self, id: int, name: str):
        self.id = id
        self.name = name

    
class HabitLog:
    def __init__ (self, id: int, habit_id: int, log_date: date):
        self.id = id
        self.habit_id = habit_id
        self.log_date = log_date