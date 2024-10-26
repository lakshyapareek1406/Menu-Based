#!/usr/bin/python3

import cgi
import cgitb
import json
import os

# Enable debugging
cgitb.enable()

# Print the content type header required for a CGI script
print("Content-Type: text/html")
print()

# File to store tasks
task_file = '/var/www/html/tasks.json'

# Load existing tasks
def load_tasks():
    if os.path.exists(task_file):
        try:
            with open(task_file, 'r') as file:
                return json.load(file)  # Return the loaded tasks
        except json.JSONDecodeError:
            return {"tasks": []}  # Return an empty task list if there's a decoding error
    return {"tasks": []}  # Return an empty task list if file doesn't exist

# Save tasks to a file
def save_tasks(tasks):
    with open(task_file, 'w') as file:
        json.dump(tasks, file, indent=4)  # Write tasks with indentation for readability

# Get the form data
form = cgi.FieldStorage()
action = form.getvalue('action')

# Load existing tasks
tasks = load_tasks()

if action == 'add':
    task_description = form.getvalue('task')
    if task_description:
        new_task = {
            "id": len(tasks["tasks"]) + 1,  # Auto-increment ID for each task
            "task": task_description,
            "completed": False
        }
        tasks["tasks"].append(new_task)  # Append the new task
        save_tasks(tasks)  # Save the updated tasks
        print("<html><body><h1>Task Added Successfully!</h1><a href='/path/to/your/index.html'>Go Back</a></body></html>")
    else:
        print("<html><body><h1>Error: Task cannot be empty.</h1><a href='/path/to/your/index.html'>Go Back</a></body></html>")
elif action == 'list':
    # Output the current tasks
    print("<html><body><h1>Current To-Do List:</h1><ul>")
    for task in tasks["tasks"]:
        print(f"<li>{task['task']} (ID: {task['id']})</li>")
    print("</ul><a href='/path/to/your/index.html'>Go Back</a></body></html>")
else:
    print("<html><body><h1>Error: Invalid action.</h1><a href='/path/to/your/index.html'>Go Back</a></body></html>")