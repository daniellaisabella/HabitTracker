import os
import streamlit as st
import requests
from datetime import date

from stats import build_dataframe, completion_rate, plot_bar_chart
from ai_advice import get_ai_advice

API_BASE = os.getenv("API_BASE", "http://backend:5000")

with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🌱 Habit Tracker")

st.caption("Build better habits, one day at a time")
st.divider()


habits = requests.get(f"{API_BASE}/habits").json()

# hent 7-dages data for alle habits
all_logs = []
for habit in habits:
    logs = requests.get(f"{API_BASE}/habits/{habit['id']}/7days").json()
    for log in logs:
        all_logs.append({
            "habit": habit["name"],
            "log_date": log["log_date"]
        })

df = build_dataframe(all_logs)

# statistik
rates = completion_rate(df, habits)


st.caption("*You daily motivation*")
if rates:
    with st.spinner("Generating advice..."):
        try:
            advice = get_ai_advice(rates)
            st.write(advice)
        except RuntimeError as e:
            st.warning(f"Could not load advice: {e}")
    st.caption("AI-generated advice. Always use your own judgement — no guarantee of accuracy.")



with st.expander("See your stats ❤️"):
    st.subheader("Your week in a glance")
    st.pyplot(plot_bar_chart(df, num_habits=len(habits)))
    if rates:
        st.subheader("Completion rate last 7 days")
        for name, rate in rates.items():
            st.progress(int(rate), text=f"{name}: {rate}%")




# liste af habits + done + delete (2 per række)
grid_cols = st.columns(2)
for i, habit in enumerate(habits):
    today = requests.get(f"{API_BASE}/habits/{habit['id']}/today").json()
    done_today = today["done"]

    with grid_cols[i % 2]:
        inner_col1, inner_col2 = st.columns([4, 1], vertical_alignment="center")
        with inner_col1:
            label = f"✅ {habit['name']}" if done_today else f"⬜️ {habit['name']}"
            if st.button(label, key=f"toggle_{habit['id']}", use_container_width=True):
                if done_today:
                    requests.delete(f"{API_BASE}/habits/{habit['id']}/log/today")
                else:
                    requests.post(f"{API_BASE}/habits/{habit['id']}/log", json={"log_date": date.today().isoformat()})
                st.rerun()
        with inner_col2:
            if st.button("🗑️", key=f"delete_{habit['id']}"):
                requests.delete(f"{API_BASE}/habits/{habit['id']}")
                st.rerun()

# add habit form
with st.form("add_habit_form", clear_on_submit=True):
    new_habit = st.text_input("What habit do you want to track?")
    submitted = st.form_submit_button("Add Habit")

    if submitted and new_habit:
        requests.post(f"{API_BASE}/habits", json={"name": new_habit})
        st.rerun()
