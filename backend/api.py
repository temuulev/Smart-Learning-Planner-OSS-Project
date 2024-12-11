from flask import Blueprint, request, jsonify

api = Blueprint('api', __name__)

tasks = []

@api.route('/submit', methods=['POST'])
def submit_task():

    global tasks
    data = request.json

    if not all(key in data for key in ['task', 'priority', 'duration']):
        return jsonify({"status": "error", "message": "Invalid input"}), 400

    tasks.append(data)
    return jsonify({"status": "success", "message": "Task received", "data": data})

@api.route('/generate_plan', methods=['GET'])
def generate_plan():

    global tasks
    if not tasks:
        return jsonify({"status": "success", "plan": {}, "message": "No tasks available"})

    sorted_tasks = sorted(tasks, key=lambda x: -x['priority'])

    schedule = {}
    current_time = 9
    hours_available = 8

    for task in sorted_tasks:
        if hours_available <= 0:
            break
        if task['duration'] <= hours_available:
            schedule[f"{current_time}:00 AM"] = task['task']
            current_time += task['duration']
            hours_available -= task['duration']

    return jsonify({"status": "success", "plan": schedule})
