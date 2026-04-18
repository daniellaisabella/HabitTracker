# Import Flask components for creating the app and handling requests/responses
from flask import Flask, jsonify, request
# Import the model classes to create instances
from backend.models.habit import Habit
from backend.models.habit_entry import HabitEntry
from backend.models.user import User

# In-memory storage for habits (list of Habit objects)
habits: list[Habit] = []
# In-memory storage for habit entries (list of HabitEntry objects)
entries: list[HabitEntry] = []
# In-memory storage for users (list of User objects)
users: list[User] = []

# Function to register all API routes with the Flask app
def register_routes(app: Flask) -> None:
    # Health check endpoint - returns server status
    @app.get("/health")
    def health():
        # Return a simple JSON response indicating the server is running
        return jsonify({"status": "ok"})

    # Get all habits endpoint
    @app.get("/habits")
    def get_habits():
        # Convert each habit object to a dictionary and return as JSON
        return jsonify([habit.__dict__ for habit in habits])

    # Create a new habit endpoint
    @app.post("/habits")
    def create_habit():
        # Get the JSON data from the request body
        payload = request.get_json(force=True)
        # Create a new Habit instance with the data
        habit = Habit(
            id=payload["id"],  # Unique identifier for the habit
            name=payload["name"],  # Name of the habit
            description=payload.get("description", ""),  # Optional description
        )
        # Add the new habit to the in-memory list
        habits.append(habit)
        # Return the created habit as JSON with HTTP 201 (Created) status
        return jsonify(habit.__dict__), 201

    # Create a new habit entry endpoint
    @app.post("/habit_entries")
    def create_habit_entry():
        # Get the JSON data from the request body
        payload = request.get_json(force=True)
        # Create a new HabitEntry instance with the data
        entry = HabitEntry(
            habit_id=payload["habit_id"],  # Which habit this entry belongs to
            date=payload["date"],  # Date of the entry
            completed=payload["completed"],  # Whether the habit was completed
            notes=payload.get("notes", ""),  # Optional notes
        )
        # Add the new entry to the in-memory list
        entries.append(entry)
        # Return the created entry as JSON with HTTP 201 (Created) status
        return jsonify(entry.__dict__), 201