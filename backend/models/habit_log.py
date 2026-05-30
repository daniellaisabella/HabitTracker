from datetime import date


class HabitLog:
    def __init__(self, id: int, habit_id: int, log_date: date):
        self.id = id
        self.habit_id = habit_id
        self.log_date = log_date
