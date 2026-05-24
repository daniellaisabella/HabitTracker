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



# Hent alle habits
try:
    response = requests.get(f"{API_BASE}/habits")
    if response.status_code == 200:
        habits = response.json()
    else:
        st.error(f"Cannot load habits (status {response.status_code})")
except requests.RequestException as e:
    st.error(f"Cannot load habits: {e}")

# Hent dagens fuldførte habits
def get_done_habits():
    try:
        # Vi antager at habit_entries ikke har et endpoint for dagens, så vi bruger mark_habit_done og lokal filtrering
        # Alternativt kunne backend udvides med et endpoint for dagens status
        # Her antager vi at /habits/missed returnerer alle ikke-fuldførte for de sidste 7 dage, så vi bruger kun /habits og /habits/<habit>/done
        # For demo: Vi markerer habits som fuldført hvis de har været markeret i dag
        # Vi laver et endpoint i backend senere hvis nødvendigt
        return []
    except Exception:
        return []

# Vis habits og mulighed for at markere som fuldført eller slette
if habits:
    st.subheader("Your daily goals")

    for habit in habits:
        cols = st.columns([6, 2, 2])

        with cols[0]:
            st.markdown(f"**{habit['name']}**")

        with cols[1]:
            done_key = f"done_{habit['id']}"

            if st.button("✔️ done", key=done_key):
                try:
                    r = requests.post(f"{API_BASE}/habits/{habit['name']}/done")

                    if r.status_code == 200:
                        st.success(f"{habit['name']} markeret som fuldført!")
                        st.rerun()
                    else:
                        st.error("Kunne ikke markere som fuldført")
                except Exception as e:
                    st.error(f"Fejl: {e}")

        with cols[2]:
            del_key = f"del_{habit['id']}"

            if st.button("🗑️", key=del_key):
                try:
                    r = requests.delete(f"{API_BASE}/habits/{habit['name']}")

                    if r.status_code == 200:
                        st.success(f"{habit['name']} slettet!")
                        st.rerun()
                    else:
                        st.error("Kunne ikke slette habit")
                except Exception as e:
                    st.error(f"Fejl: {e}")
else:
    st.write("Ingen vaner endnu")

# TODO: Visning af dagens fuldførte habits øverst (kræver evt. backend endpoint)


# Add Habit — simple form
with st.expander("➕ Add Habit"):
    with st.form("add_habit"):
        habit_name = st.text_input("What habit do you want to track?", max_chars=50)
        submitted = st.form_submit_button("Add Habit")
        if submitted and habit_name:
            try:
                response = requests.post(f"{API_BASE}/habits", json={"name": habit_name})
                if response.status_code == 201:
                    st.success("Habit added!")
                    st.rerun()
                else:
                    st.error("Failed to add habit")
            except Exception as e:
                st.error(f"Error: {e}")
