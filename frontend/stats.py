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
        # timedelta objekt, .days henter antallet af dage som int
        days_active = min(7, (today - created).days + 1)
        if df.empty or habit["id"] not in df["habit_id"].values:
            rates[name] = 0.0
        else:
            habit_df = df[(df["habit_id"] == habit["id"]) & (df["log_date"] >= created)]
            completed = habit_df["log_date"].count()  # type: ignore
            rates[name] = float(np.round(completed / days_active * 100, 1))
    return rates


def completion_mean(rates: dict) -> float:
    values = list(rates.values())
    return float(np.round(np.mean(values), 1))
    


def plot_bar_chart(df: pd.DataFrame, num_habits: int = 1) -> Figure:
    today = date.today()
    
    # genererer en liste af de sidste 7 dage, inklusiv i dag, i formatet date
    last_7 = [today - timedelta(days=i) for i in range(6, -1, -1)]

    if df.empty:
        counts = [0] * 7
    else:
        counts = [int((df["log_date"] == d).sum()) for d in last_7]

    # formaterer dato til labels skrevet som en str
    labels = [d.strftime("%a\n%d/%m") for d in last_7]

    # Matplotlib objekter: fig = ydre figurramme, ax =  plot-område
    fig, ax = plt.subplots(figsize=(8, 4))
    fig.patch.set_facecolor("#F8FAF5")
    ax.set_facecolor("#F8FAF5")
    ax.bar(labels, counts, color="#52B788")
    ax.set_ylabel("Habits completed")
    ax.set_ylim(0, max(num_habits, 1) + 0.5)
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.tight_layout()
    return fig
