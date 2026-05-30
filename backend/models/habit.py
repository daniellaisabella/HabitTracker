from datetime import date


class Habit:
    # __init__ (konstruktor) method to initialize the habit object, self er ligesom this i Java
    def __init__(self, id: int, name: str, created_at: date):
        self.id = id
        self.name = name
        self.created_at = created_at
