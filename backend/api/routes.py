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

    # Get all habit entries endpoint
    @app.get("/habit_entries")
    def get_habit_entries():
        # Convert each entry object to a dictionary and return as JSON
        return jsonify([entry.__dict__ for entry in entries])

    # Create a new habit endpoint
    @app.post("/habits")
    def create_habit():
        # Get the JSON data from the request body
        payload = request.get_json(force=True)
        frequency = payload.get("frequency", "daily")
        if frequency not in ("daily", "weekly"):
            return jsonify({"error": "frequency must be 'daily' or 'weekly'"}), 400

        target_days_per_week = int(payload.get("target_days_per_week", 7))
        if target_days_per_week < 1 or target_days_per_week > 7:
            return jsonify({"error": "target_days_per_week must be between 1 and 7"}), 400

        # Create a new Habit instance with the data
        habit = Habit(
            id=payload["id"],  # Unique identifier for the habit
            name=payload["name"],  # Name of the habit
            description=payload.get("description", ""),  # Optional description
            frequency=frequency,
            target_days_per_week=target_days_per_week,
            target_amount=float(payload.get("target_amount", 1.0)),
            unit=payload.get("unit", "times"),
        )
        # Add the new habit to the in-memory list
        habits.append(habit)
        # Return the created habit as JSON with HTTP 201 (Created) status
        return jsonify(habit.__dict__), 201

    # Delete habit endpoint
    @app.delete("/habits/<int:habit_id>")
    def delete_habit(habit_id: int):
        # Find the habit by id and remove it if present.
        for index, habit in enumerate(habits):
            if habit.id == habit_id:
                del habits[index]
                # Also delete entries tied to this habit.
                entries[:] = [entry for entry in entries if entry.habit_id != habit_id]
                return "", 204
        return jsonify({"error": "Habit not found"}), 404

    # Create a new habit entry endpoint
    @app.post("/habit_entries")
    def create_habit_entry():
        # Get the JSON data from the request body
        payload = request.get_json(force=True)
        next_id = max((getattr(entry, "id", 0) for entry in entries), default=0) + 1
        # Create a new HabitEntry instance with the data
        entry = HabitEntry(
            id=next_id,
            habit_id=payload["habit_id"],  # Which habit this entry belongs to
            date=payload["date"],  # Date of the entry
            completed=payload["completed"],  # Whether the habit was completed
            notes=payload.get("notes", ""),  # Optional notes
            performed_amount=float(payload.get("performed_amount", 0.0)),
        )
        # Add the new entry to the in-memory list
        entries.append(entry)
        # Return the created entry as JSON with HTTP 201 (Created) status
        return jsonify(entry.__dict__), 201

    # Delete one habit entry endpoint
    @app.delete("/habit_entries/<int:entry_id>")
    def delete_habit_entry(entry_id: int):
        for index, entry in enumerate(entries):
            if getattr(entry, "id", None) == entry_id:
                del entries[index]
                return "", 204
        return jsonify({"error": "Habit entry not found"}), 404