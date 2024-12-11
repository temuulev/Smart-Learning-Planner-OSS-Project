def generate_schedule(tasks, hours_available):

    sorted_tasks = sorted(tasks, key=lambda x: -x['priority'])
    schedule = {}
    current_time = 9

    for task in sorted_tasks:
        if hours_available <= 0:
            break
        if task['duration'] <= hours_available:
            schedule[f"{current_time}:00"] = task['task']
            current_time += task['duration']
            hours_available -= task['duration']

    return schedule
