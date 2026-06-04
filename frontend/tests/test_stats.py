import pandas as pd
from datetime import date
from frontend.stats import completion_rate


# test completion rate function
def test_full_completion_rate():
    today = date.today()
    logs = [{"habit_id": 1, "log_date": today}]
    df = pd.DataFrame(logs)
    habits = [{"id": 1, "name": "Sport", "created_at": today.isoformat()}]
    rates = completion_rate(df, habits)
    assert rates["Sport"] == 100.0
