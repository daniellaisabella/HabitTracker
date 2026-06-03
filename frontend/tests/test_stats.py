import pandas as pd
from datetime import date
from frontend.stats import completion_rate



def test_completion_rate_full_week():
    today = date.today()
    logs = [{"habit_id": 1, "log_date": today} for _ in range(7)]
    df = pd.DataFrame(logs)
    habits = [{"id": 1, "name": "Sport", "created_at": "2020-01-01T00:00:00"}]
    rates = completion_rate(df, habits)
    assert rates["Sport"] == 100.0
