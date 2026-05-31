import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from datetime import date, timedelta


# funktion der modtager all_logs som er en liste samlet i app.py
# hvis der ikke er logs, så retunerer den tomme kollonner 
# laver variabel df som er en pandas dataframe
def build_dataframe(all_logs: list) -> pd.DataFrame:
    if not all_logs:
        return pd.DataFrame(columns=["habit", "log_date"])
    df = pd.DataFrame(all_logs)
    # konerter log_date som er string til datetime format
    df["log_date"] = pd.to_datetime(df["log_date"]).dt.date
    return df


#modtager datafram fra app.py og listen af habitsog returnerer en dict
def completion_rate(df: pd.DataFrame, habits: list) -> dict:
    # opretter en tom dict til completion rates name:rate
    rates = {} 
    today = date.today()
    for habit in habits:
        name = habit["name"]
        # variabel med date og :10 tager kun de 10 første tegn i isoformat - og konverterer til date objekt
        created = date.fromisoformat(habit["created_at"][:10])
        # finder antal dage fra created til i dag men max 7 dage for at vise en uge
        #+ 1 fordi den trækker today fra : tænk oprettet i - today = 0 +1
        days_active = min(7, (today - created).days + 1)
        # hvis habit ik har logs = 0.0
        if df.empty or habit["id"] not in df["habit_id"].values:
            rates[name] = 0.0 #indsæt i dict
        else:
            #variabel der gemmer id  med dens logdate hvis log date er nyere end created hvis korrupt data i db
            habit_df = df[(df["habit_id"] == habit["id"]) & (df["log_date"] >= created)]
            # tæl for en habit hvor mange log_date den har
            completed = habit_df["log_date"].count() # type: ignore
            #opretter nøgle(name) værdi(rate) til rates dict
            #float konverterer numpy type til python float fordi vi afrunder med numpt round til 1 decimal
            rates[name] = float(np.round(completed / days_active * 100, 1))
    return rates


# mdtager df med alle logs, =1 er fall backs hvis der ik er nogle habits, returner en figure
def plot_bar_chart(df: pd.DataFrame, num_habits: int = 1) -> Figure:
    today = date.today()
    # denne genererer datoerne i en liste for de sidste 7 dage ved at tælle dem baglæns
    # datetime timedelta python funktion der kan trække dage fra today
    # today - 6 = 6 dage siden men det er 7 inklusiv i dag.
    # tæller fra 6 stop -1 (fordi den er ekslusiv, den stopper 0) , step 1 hver gang
    last_7 = [today - timedelta(days=i) for i in range(6, -1, -1)]

    if df.empty:
        # laver en df med 7 nuller til grafen for hver dag
        counts = [0] * 7
    else:
        # gemmer en liste af counts for hver log_date i listen last_7
        # pandas overskriver pyhon
        # den kigger i kolonnen log_date og tager dén date d og sammenligner med alle rækker 
        # og returner true hvis log_date == d, og den summere så count som en int
        counts = [int((df["log_date"] == d).sum()) for d in last_7]

    # labels til plot bar som skrievr d (dato fra last_y listen) om i string format 
    # som dag forkortelse, linjeskift og så dato og måned
    labels = [d.strftime("%a\n%d/%m") for d in last_7]

    #her bygges figuren 
    # den laver en tuple med en figur med en akse inden og sætter størrelsen
    fig, ax = plt.subplots(figsize=(8, 4))
    # det er figurens og aksens baggrundsfarve
    fig.patch.set_facecolor("#F8FAF5")
    ax.set_facecolor("#F8FAF5")
    # det er bar chartet x akse labels og y akse counts og grøn farve til baren 
    ax.bar(labels, counts, color="#52B788")
    # det er y akse titel
    ax.set_ylabel("Habits completed")
    # det er y aksen max værdi +0.5 som giver luft
    # starter på 0, og den er enten så høj som num_habits eller min 1 + 0.5
    ax.set_ylim(0, max(num_habits, 1) + 0.5)
    # den viser kun heltal i y aksen
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    # indbygget funktion til ikke at lade noget overlappe 
    plt.tight_layout()
    return fig

