import streamlit as st 
import requests # to call my Flaks backend
import os

st.set_page_config(
    page_title="Habit Tracker",
    page_icon="🌱",
    layout="wide"
)

#backend url where Flask app runs - all API calls use this base URL

API_BASE = os.getenv("API_BASE", "http://127.0.0.1:5000")
habits = []



# Load CSS from .streamlit/style.css
_css_path = os.path.join(os.path.dirname(__file__), ".streamlit", "style.css")
with open(_css_path) as _f:
    st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)

#Page title
st.title("Changing your lifestyle, day by day 🌱")

# Overview of habits — rendered as card grid
try:
    response = requests.get(f"{API_BASE}/habits")
    if response.status_code == 200:
        habits = response.json()
        if habits:
            COLS = 5  # cards per row
            rows = [habits[i:i+COLS] for i in range(0, len(habits), COLS)]
            for row in rows:
                cols = st.columns(COLS)
                for col, habit in zip(cols, row):
                    frequency = habit.get("frequency", "daily")
                    target_days = habit.get("target_days_per_week", 7)
                    target_amount = habit.get("target_amount", 1.0)
                    unit = habit.get("unit", "times")
                    target_text = f"{target_days} days/week" if frequency == "weekly" else "daily"
                    desc = habit.get("description", "")
                    with col:
                        st.html(f"""
<div class="habit-card">
  <div class="habit-card-title">{habit['name']}</div>
  <div class="habit-card-meta">{desc + '<br>' if desc else ''}🗓 {target_text} &bull; 🎯 {target_amount} {unit}</div>
</div>
""")
                        _, delete_col = st.columns([4, 1])
                        if delete_col.button("✕", key=f"del_habit_{habit['id']}", help="Delete habit"):
                            try:
                                delete_response = requests.delete(f"{API_BASE}/habits/{habit['id']}")
                                if delete_response.status_code == 204:
                                    st.rerun()
                                else:
                                    st.error(f"Failed to delete habit (status {delete_response.status_code})")
                            except requests.RequestException as e:
                                st.error(f"Cannot delete habit: {e}")
        else:
            st.write("No habits yet")
    else:
        st.error(f"Cannot load habits (status {response.status_code})")
except requests.RequestException as e:
    st.error(f"Cannot load habits: {e}")


# Add Habit — collapsible expander below the cards
with st.expander("➕ Add Habit"):
    with st.form("add_habit"):
        habit_name = st.text_input("What habit do you want to track?", max_chars=50)
        habit_description = st.text_area("Description")
        st.write("Weekdays")
        day_col1, day_col2, day_col3, day_col4, day_col5, day_col6, day_col7 = st.columns(7)
        monday = day_col1.checkbox("Monday", value=True)
        tuesday = day_col2.checkbox("Tuesday")
        wednesday = day_col3.checkbox("Wednesday")
        thursday = day_col4.checkbox("Thursday")
        friday = day_col5.checkbox("Friday")
        saturday = day_col6.checkbox("Saturday")
        sunday = day_col7.checkbox("Sunday")
        target_amount = st.slider("Target amount", min_value=0.0, max_value=20.0, value=1.0, step=0.1)
        st.write("Unit")
        unit_col1, unit_col2, unit_col3, unit_col4, unit_col5 = st.columns(5)
        unit_times = unit_col1.checkbox("Times", value=True)
        unit_hours = unit_col2.checkbox("Hours", value=False)
        unit_liters = unit_col3.checkbox("Liters", value=False)
        unit_minutes = unit_col4.checkbox("Minutes", value=False)
        unit_km = unit_col5.checkbox("Km", value=False)
        submitted = st.form_submit_button("Add Habit")

        if submitted and habit_name:
            try:
                selected_days = []
                if monday:
                    selected_days.append("monday")
                if tuesday:
                    selected_days.append("tuesday")
                if wednesday:
                    selected_days.append("wednesday")
                if thursday:
                    selected_days.append("thursday")
                if friday:
                    selected_days.append("friday")
                if saturday:
                    selected_days.append("saturday")
                if sunday:
                    selected_days.append("sunday")

                if not selected_days:
                    st.error("Choose at least one weekday.")
                    st.stop()

                selected_units = []
                if unit_times:
                    selected_units.append("times")
                if unit_hours:
                    selected_units.append("hours")
                if unit_liters:
                    selected_units.append("liters")
                if unit_minutes:
                    selected_units.append("minutes")
                if unit_km:
                    selected_units.append("km")

                if len(selected_units) != 1:
                    st.error("Choose exactly one unit.")
                    st.stop()

                frequency = "weekly"
                target_days_per_week = len(selected_days)
                unit = selected_units[0]

                response = requests.get(f"{API_BASE}/habits")
                habits = response.json() if response.status_code == 200 else []
                next_id = max([h['id'] for h in habits], default=0) + 1
                payload = {
                    "id": next_id,
                    "name": habit_name,
                    "description": habit_description,
                    "frequency": frequency,
                    "target_days_per_week": target_days_per_week,
                    "target_amount": target_amount,
                    "unit": unit,
                }
                response = requests.post(f"{API_BASE}/habits", json=payload)
                if response.status_code == 201:
                    st.success("Habit added!")
                    st.rerun()
                else:
                    st.error("Failed to add habit")
            except Exception as e:
                st.error(f"Error: {e}")
