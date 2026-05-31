from flask import Blueprint, request, jsonify
import backend.services.habit_log_service as habit_log_service

habit_log_blueprint = Blueprint('habit_logs', __name__) #___name__ er modulsti svarende til ./

@habit_log_blueprint.route('/habits/<int:habit_id>/today', methods=['GET'])
def get_today(habit_id):
    done = habit_log_service.get_today(habit_id)
    return jsonify({"done": done})

@habit_log_blueprint.route('/habits/<int:habit_id>/log', methods=['POST'])
def log_habit(habit_id):
    data = request.get_json()
    habit_log_service.log_habit(habit_id, data.get('log_date') if data else None)
    return '', 201

@habit_log_blueprint.route('/habits/<int:habit_id>/7days', methods=['GET'])
def get_last_7_days(habit_id):
    logs = habit_log_service.get_last_7_days(habit_id)
    return jsonify([{"id": log.id,
                     "habit_id": log.habit_id,
                     "log_date": log.log_date.isoformat()}
                    for log in logs])

@habit_log_blueprint.route('/habits/<int:habit_id>/log/today', methods=['DELETE'])
def delete_today_log(habit_id):
    habit_log_service.delete_today(habit_id)
    return '', 204
