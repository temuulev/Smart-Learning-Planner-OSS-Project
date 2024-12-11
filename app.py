from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder='frontend')

# Global list to store tasks
tasks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_task():
    global tasks
    data = request.json

    # Append the received task to the global list
    tasks.append(data)
    return jsonify({"status": "success", "message": "Task received", "data": data})

@app.route('/generate_plan', methods=['GET'])
def generate_plan():
    global tasks

    if not tasks:
        return jsonify({"status": "success", "plan": {}, "message": "No tasks available"})

    # Sort tasks by priority (highest priority first)
    sorted_tasks = sorted(tasks, key=lambda x: -x['priority'])

    schedule = []
    current_time = 9  # Start time at 9:00 AM
    hours_available = 8  # Total available hours

    for task in sorted_tasks:
        if hours_available <= 0:
            break  # Stop scheduling if no hours are left
        if task['duration'] <= hours_available:
            schedule.append({"time": f"{current_time}:00 AM", "task": task['task']})
            current_time += task['duration']  # Increment time by task duration
            hours_available -= task['duration']  # Deduct task duration from available hours

    # Sort the schedule by time (to ensure it is in chronological order)
    schedule.sort(key=lambda x: int(x['time'].split(":")[0]))  # Sorting based on the hour

    return jsonify({"status": "success", "plan": schedule})

if __name__ == '__main__':
    app.run(debug=True)
