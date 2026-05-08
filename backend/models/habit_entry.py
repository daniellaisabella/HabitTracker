class HabitEntry:
    def __init__(
        self,
        id: int,
        habit_id: int,
        date: str,
        completed: bool,
        notes: str = "",
        performed_amount: float = 0.0,
    ):
        self.id = id
        self.habit_id = habit_id
        self.date = date
        self.completed = completed
        self.notes = notes
        self.performed_amount = performed_amount


