import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from datetime import date, timedelta


def build_dataframe(all_logs: list) -> pd.DataFrame:
    if not all_logs:
        return pd.DataFrame(columns=["habit", "log_date"])
    df = pd.DataFrame(all_logs)
    df["log_date"] = pd.to_datetime(df["log_date"]).dt.date
    return df


def completion_rate(df: pd.DataFrame, habits: list) -> dict:
    rates = {}
    today = date.today()
    for habit in habits:
        name = habit["name"]
        created = date.fromisoformat(habit["created_at"][:10])
        days_active = min(7, (today - created).days + 1)
        if df.empty or name not in df["habit"].values:
            rates[name] = 0.0
        else:
            habit_df = df[(df["habit"] == name) & (df["log_date"] >= created)]
            completed = habit_df["log_date"].nunique()  # type: ignore[union-attr]
            rates[name] = float(np.round(completed / days_active * 100, 1))
    return rates


def plot_bar_chart(df: pd.DataFrame, num_habits: int = 1) -> Figure:
    today = date.today()
    last_7 = [today - timedelta(days=i) for i in range(6, -1, -1)]

    if df.empty:
        counts = [0] * 7
    else:
        counts = [int((df["log_date"] == d).sum()) for d in last_7]

    labels = [d.strftime("%a\n%d/%m") for d in last_7]

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(labels, counts, color="#AEF2B0")
    ax.set_ylabel("Habits completed")
    ax.set_title("Lasat 7 days")
    ax.set_ylim(0, max(num_habits, 1) + 0.5)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    return fig

