class Habit:
    def __init__(
        self,
        id: int,
        name: str,
        description: str = "",
        frequency: str = "daily",
        target_days_per_week: int = 7,
        target_amount: float = 1.0,
        unit: str = "times",
    ):
        self.id = id
        self.name = name
        self.description = description
        self.frequency = frequency
        self.target_days_per_week = target_days_per_week
        self.target_amount = target_amount
        self.unit = unit
