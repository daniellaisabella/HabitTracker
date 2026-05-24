from flask import Flask, jsonify, request
from datetime import date, timedelta


from backend.models import init_db
from backend.services.habit_service import HabitService


def register_routes(app: Flask) -> None:
    init_db()

    # -------------------------
    # GET all habits
    # -------------------------
    @app.get("/habits")
    def get_habits():
        db = SessionLocal()
        habits = db.query(Habit).all()
        result = [{"id": h.id, "name": h.name} for h in habits]
        db.close()
        return jsonify(result)

    # -------------------------
    # CREATE habit
    # -------------------------
    @app.post("/habits")
    def create_habit():
        db = SessionLocal()
        payload = request.get_json(force=True)

           result = HabitService.list_habits()
           return jsonify(result)
        habit = Habit(name=name)
        db.add(habit)

        try:
            db.commit()
        except IntegrityError:
            db.close()
            return jsonify({"error": "Habit already exists"}), 400

        result = {"id": habit.id, "name": habit.name}
        return jsonify(result), 201

           result = HabitService.create_habit(name)
           if "error" in result:
              return jsonify(result), 400
           return jsonify(result), 201

    # -------------------------
    # MARK HABIT DONE TODAY
    # -------------------------
    @app.post("/habits/<habit_name>/done")
    def mark_habit_done(habit_name):

           result = HabitService.mark_done(habit_name)
           if "error" in result:
              return jsonify(result), 404
           return jsonify(result)

        if not habit:
            db.close()
            return jsonify({"error": "Habit not found"}), 404

        today = date.today()

           result = HabitService.delete_habit(habit_name)
           if "error" in result:
              return jsonify(result), 404
           return jsonify(result)
            db.query(HabitEntry)
            .filter_by(habit_id=habit.id, date=today)
            .first()
        )

        if existing:
            db.close()
            return jsonify({
                "status": "already done",
                "habit": habit_name,
                "date": str(today)
            })

        entry = HabitEntry(
            habit_id=habit.id,
            date=today,
            completed=True
        )

        db.add(entry)
        db.commit()
        db.close()

        return jsonify({
            "status": "ok",
            "habit": habit_name,
            "date": str(today)
        })

    # -------------------------
    # DELETE HABIT (BY NAME)
    # -------------------------
    @app.delete("/habits/<habit_name>")
    def delete_habit(habit_name):
        db = SessionLocal()
        habit = db.query(Habit).filter_by(name=habit_name).first()

        if not habit:
            db.close()
            return jsonify({"error": "Habit not found"}), 404

        db.delete(habit)
        db.commit()
        db.close()

        return jsonify({"status": "deleted", "habit": habit_name})

    # -------------------------
    # MISSED HABITS (LAST 7 DAYS)
    # -------------------------
    @app.get("/habits/missed")
    def get_missed_habits():
        db = SessionLocal()
        today = date.today()

        habits = db.query(Habit).all()
        missed = []

        for habit in habits:
            for i in range(7):
                d = today - timedelta(days=i)

                entry = (
                    db.query(HabitEntry)
                    .filter_by(habit_id=habit.id, date=d)
                    .first()
                )

                if not entry:
                    missed.append({
                        "habit": habit.name,
                        "date": str(d)
                    })

        db.close()
        return jsonify(missed)

    # -------------------------
    # CREATE HABIT ENTRY (GENERIC)
    # -------------------------
    @app.post("/habit_entries")
    def create_habit_entry():
        db = SessionLocal()
        payload = request.get_json(force=True)

        entry = HabitEntry(
            habit_id=payload["habit_id"],
            date=payload["date"],
            completed=payload.get("completed", False),
            notes=payload.get("notes", ""),
            performed_amount=float(payload.get("performed_amount", 0.0)),
        )

        db.add(entry)
        db.commit()

        result = {
            "id": entry.id,
            "habit_id": entry.habit_id,
            "date": str(entry.date),
            "completed": entry.completed,
            "notes": entry.notes,
            "performed_amount": entry.performed_amount,
        }

        db.close()
        return jsonify(result), 201

    # -------------------------
    # DELETE HABIT ENTRY
    # -------------------------
    @app.delete("/habit_entries/<int:entry_id>")
    def delete_habit_entry(entry_id):
        db = SessionLocal()

        entry = db.query(HabitEntry).filter_by(id=entry_id).first()

        if not entry:
            db.close()
            return jsonify({"error": "Habit entry not found"}), 404

        db.delete(entry)
        db.commit()
        db.close()

        return "", 204