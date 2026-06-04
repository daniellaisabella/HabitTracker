import os
import streamlit as st
import requests
from datetime import date

from stats import build_dataframe, completion_rate, completion_mean, plot_bar_chart
from ai_advice import get_ai_advice

API_BASE = os.getenv("API_BASE")

with open("frontend/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True) #bruger min css fil i frontend modul



st.title("🌱 Habit Tracker")
st.caption("Build better habits, one day at a time")
st.divider()

# get_all habits
habits = requests.get(f"{API_BASE}/habits").json()

# hent 7-dages data for alle habits
all_logs = []
for habit in habits:
    logs = requests.get(f"{API_BASE}/habits/{habit['id']}/7days").json()
    for log in logs:
        all_logs.append({
            "habit_id": habit["id"],
            "habit": habit["name"],
            "log_date": log["log_date"]
        })
        
        
df = build_dataframe(all_logs)
rates = completion_rate(df, habits)

################### MOTIVATION ####################

st.caption("*Your daily motivation*")
if rates:
    with st.spinner("Consulting your AI coach..."):
        try:
            advice = get_ai_advice(rates)
            st.write(advice)
        except RuntimeError as e:
            st.warning(f"Could not load advice: {e}")
    st.caption("AI-generated advice. Always use your own judgement — no guarantee of accuracy.")

################### STATS ####################

with st.expander("See your stats ❤️"):
    st.subheader("Your week in a glance")
    st.pyplot(plot_bar_chart(df, num_habits=len(habits)))
    if rates:
        st.subheader("Completion rate last 7 days")
        st.metric("Average completion rate", f"{completion_mean(rates)}%")
        for name, rate in rates.items():
            st.progress(int(rate), text=f"{name}: {rate}%")


################### HABITS ####################

grid_cols = st.columns(2)
for i, habit in enumerate(habits):
    done_today = requests.get(f"{API_BASE}/habits/{habit['id']}/today").json()["done"]

    with grid_cols[i % 2]:
        inner_col1, inner_col2 = st.columns([1, 4], vertical_alignment="center")
        with inner_col1:
            if st.button("🗑️", key=f"delete_{habit['id']}"):
                requests.delete(f"{API_BASE}/habits/{habit['id']}")
                st.rerun()
        with inner_col2:
            label = f"✅ {habit['name']}" if done_today else f"⬜️ {habit['name']}"
            if st.button(label, key=f"toggle_{habit['id']}", use_container_width=False):
                if done_today:
                    requests.delete(f"{API_BASE}/habits/{habit['id']}/log/today")
                else:
                    requests.post(f"{API_BASE}/habits/{habit['id']}/log", json={"log_date": date.today().isoformat()})
                st.rerun()

################### ADD HABIT ####################

with st.form("add_habit_form", clear_on_submit=True):
    new_habit = st.text_input("What habit do you want to track?")
    submitted = st.form_submit_button("Add Habit")

    if submitted and new_habit:
        response = requests.post(f"{API_BASE}/habits", json={"name": new_habit})
        if response.ok:
            st.rerun()
        else:
            st.error(response.json().get("error", "Something went wrong."))
    elif submitted:
        st.warning("Habit name cannot be empty.")