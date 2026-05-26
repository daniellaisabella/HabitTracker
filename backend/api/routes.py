from flask import Blueprint, request, jsonify
import backend.services.habit_service as habit_service
import backend.services.habit_log_service as habit_log_service

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('/habits', methods=['GET'])
def get_habits():
    habits = habit_service.get_all()
    return jsonify([{"id": h.id, "name": h.name, "created_at": h.created_at.isoformat()} for h in habits])

@api_blueprint.route('/habits', methods=['POST'])
def create_habit():
    data = request.get_json()
    if not data or not data.get('name', '').strip():
        return jsonify({"error": "name is required"}), 400
    habit = habit_service.create(data['name'].strip())
    return jsonify({"id": habit.id, "name": habit.name}), 201
  

@api_blueprint.route('/habits/<int:habit_id>', methods=['DELETE'])
def delete_habit(habit_id):
    habit_service.delete(habit_id)
    return '', 204

@api_blueprint.route('/habits/<int:habit_id>/today', methods=['GET'])
def get_today(habit_id):
    done = habit_log_service.get_today(habit_id)
    return jsonify({"done": done})


############################################
############################################


@api_blueprint.route('/habits/<int:habit_id>/log', methods=['POST'])
def log_habit(habit_id):
    data = request.get_json()
    if not data or not data.get('log_date'):
        return jsonify({"error": "log_date is required"}), 400
    habit_log_service.log_habit(habit_id, data['log_date'])
    return '', 201

@api_blueprint.route('/habits/<int:habit_id>/log/today', methods=['DELETE'])
def delete_today_log(habit_id):
    habit_log_service.delete_today(habit_id)
    return '', 204

@api_blueprint.route('/habits/<int:habit_id>/7days', methods=['GET'])
def get_last_7_days(habit_id):
    logs = habit_log_service.get_last_7_days(habit_id)
    return jsonify([{"id": log.id, 
                     "habit_id": log.habit_id,
                     "log_date": log.log_date.isoformat()} 
                    for log in logs])
    

############################################
############################################

