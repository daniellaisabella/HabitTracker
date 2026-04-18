class HabitEntry:
    def __init__(self, habit_id: int, date: str, completed: bool, notes: str = ""):
        self.habit_id = habit_id
        self.date = date
        self.completed = completed
        self.notes = notes


