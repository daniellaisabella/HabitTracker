from flask import Blueprint, request, jsonify
import backend.services.habit_service as habit_service

habit_blueprint = Blueprint('habits', __name__)

@habit_blueprint.route('/habits', methods=['GET'])
def get_habits():
    habits = habit_service.get_all()
    return jsonify([{"id": h.id, "name": h.name, "created_at": h.created_at.isoformat()} for h in habits])

@habit_blueprint.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    habit = habit_service.create(data.get('name', '').strip() if data else '')
    return jsonify({"id": habit.id, "name": habit.name, "created_at": habit.created_at.isoformat()}), 201

@habit_blueprint.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit_service.delete(habit_id)
    return '', 204
