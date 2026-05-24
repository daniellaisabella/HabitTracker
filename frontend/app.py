import streamlit as st
import requests
from datetime import date

st.title("🌱 Habit Tracker")
st.caption("Build better habits, one day at a time")


habits = requests.get("http://backend:5000/habits").json()

#liste af habits + done + delete
for habit in habits:
    today = requests.get(f"http://backend:5000/habits/{habit['id']}/today").json()
    done_today = today["done"]
    
    col1, col2, col3 = st.columns([4, 1, 1])
    
    with col1:
        if done_today:
            st.success(f"✅ {habit['name']}")
        else:
            st.write(habit["name"])
    with col2:
        if done_today:
            if st.button("↩️ Undo", key=f"undo_{habit['id']}"):
                requests.delete(f"http://backend:5000/habits/{habit['id']}/log/today")
                st.rerun()
        else:
            if st.button("Done", key=f"done_{habit['id']}"):
                requests.post(f"http://backend:5000/habits/{habit['id']}/log", json={
                    "log_date": date.today().isoformat()
                })
                st.rerun()
            
            
    with col3:
        if st.button("Delete", key=f"delete_{habit['id']}"):
            requests.delete(f"http://backend:5000/habits/{habit['id']}")
            st.rerun()
                
# add habit form               
with st.form("add_habit_form", clear_on_submit=True):
    new_habit = st.text_input("What habit do you want to track?")
    submitted = st.form_submit_button("Add Habit")
    
    if submitted and new_habit:
        requests.post("http://backend:5000/habits", json={"name": new_habit})
        st.rerun()
        
        
    
    
    
        
        