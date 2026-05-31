import os
import streamlit as st
import requests
from datetime import date

from stats import build_dataframe, completion_rate, plot_bar_chart
from ai_advice import get_ai_advice

API_BASE = os.getenv("API_BASE", "http://backend:5000") #api base fra .env filen, eller fall back 5000

with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) #bruger min css fil i frontend modul

st.title("🌱 Habit Tracker")
st.caption("Build better habits, one day at a time")
st.divider()

# initialiser session state caches - hentes kun én gang fra API
if "habits" not in st.session_state:
    st.session_state.habits = requests.get(f"{API_BASE}/habits").json()
if "logs_cache" not in st.session_state:
    st.session_state.logs_cache = {}
if "today_cache" not in st.session_state:
    st.session_state.today_cache = {}

habits = st.session_state.habits

# hent 7-dages data for alle habits (cached per habit_id)
all_logs = []
for habit in habits:
    if habit["id"] not in st.session_state.logs_cache:
        logs = requests.get(f"{API_BASE}/habits/{habit['id']}/7days").json()
        st.session_state.logs_cache[habit["id"]] = logs
    for log in st.session_state.logs_cache[habit["id"]]:
        all_logs.append({
            "habit_id": habit["id"],
            "habit": habit["name"],
            "log_date": log["log_date"]
        })

# i stats.py har  jeg en hjælpefunktion der bygger en dataframe (tabeldata) med pandas bibliotek
df = build_dataframe(all_logs)

# STATISTIK
# gemmer completion rate i en variabel som modtager df og listen af habits
rates = completion_rate(df, habits)

st.caption("*Your daily motivation*")
# hvis rates ik er null
if rates:
    # streamlit spinner
    with st.spinner("Consulting your AI coach..."):
        # try except hvis der er fejl i kaldet
        try:
            # hent advice fra metoden i ai_advice.py og giv den rates med som argument
            advice = get_ai_advice(rates)
            # streamlit markdown
            st.write(advice)
        except RuntimeError as e:
            st.warning(f"Could not load advice: {e}")
    st.caption("AI-generated advice. Always use your own judgement — no guarantee of accuracy.")

# streamlit expander er en drop down
with st.expander("See your stats ❤️"):
    st.subheader("Your week in a glance")
    # returnerer figur fra stats og pyplot er streamlit funktion til at vise en matplotlib figur
    st.pyplot(plot_bar_chart(df, num_habits=len(habits)))
    if rates:
        st.subheader("Completion rate last 7 days")
        # for loop over rates dict
        for name, rate in rates.items():
            # streamlit progress bar tager int værdi mellem 0 og 100
            st.progress(int(rate), text=f"{name}: {rate}%")

# liste af habits + done + delete (2 per række)
grid_cols = st.columns(2)
for i, habit in enumerate(habits):
    # hent today status (cached per habit_id)
    if habit["id"] not in st.session_state.today_cache:
        today = requests.get(f"{API_BASE}/habits/{habit['id']}/today").json()
        st.session_state.today_cache[habit["id"]] = today["done"]
    done_today = st.session_state.today_cache[habit["id"]]

    with grid_cols[i % 2]:
        inner_col1, inner_col2 = st.columns([1, 4], vertical_alignment="center")
        with inner_col1:
            if st.button("🗑️", key=f"delete_{habit['id']}"):
                requests.delete(f"{API_BASE}/habits/{habit['id']}")
                # opdater session state direkte uden nyt API-kald
                # behold alle habits borset fra dette id
                st.session_state.habits = [h for h in habits if h["id"] != habit["id"]]
                st.session_state.logs_cache.pop(habit["id"], None)
                st.session_state.today_cache.pop(habit["id"], None)
                st.rerun()
        with inner_col2:
            label = f"✅ {habit['name']}" if done_today else f"⬜️ {habit['name']}"
            if st.button(label, key=f"toggle_{habit['id']}", use_container_width=False):
                if done_today:
                    requests.delete(f"{API_BASE}/habits/{habit['id']}/log/today")
                    st.session_state.today_cache[habit["id"]] = False
                else:
                    requests.post(f"{API_BASE}/habits/{habit['id']}/log", json={"log_date": date.today().isoformat()})
                    st.session_state.today_cache[habit["id"]] = True
                # invalider logs cache for denne habit så stats opdateres
                st.session_state.logs_cache.pop(habit["id"], None)
                st.rerun()

# add habit form
with st.form("add_habit_form", clear_on_submit=True):
    new_habit = st.text_input("What habit do you want to track?")
    submitted = st.form_submit_button("Add Habit")

    if submitted and new_habit:
        # brug response direkte til at tilføje til cache uden nyt GET kald
        response = requests.post(f"{API_BASE}/habits", json={"name": new_habit})
        st.session_state.habits.append(response.json())
        st.rerun()
