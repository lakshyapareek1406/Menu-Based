import cgi
import subprocess
import json

print("Content-type: text/html\n")

# Get form data
form = cgi.FieldStorage()

# Function to execute Docker commands
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return {"status": "success", "output": result.stdout.strip()}
        else:
            return {"status": "error", "output": result.stderr.strip()}
    except Exception as e:
        return {"status": "error", "output": str(e)}

# Handling different actions based on form data
action = form.getvalue("action")

# Actions to handle Docker operations
if action == "pull_image":
    image_name = form.getvalue("imageName")
    if image_name:
        output = run_command(f"docker pull {image_name}")
        print(json.dumps(output))
    else:
        print(json.dumps({"status": "error", "output": "Image name is required"}))                elif action == "get_all_images":
    output = run_command("docker images")
    print(json.dumps(output))

    elif action == "show_running_containers":
    output = run_command("docker ps")
    print(json.dumps(output))

elif action == "show_all_containers":
    output = run_command("docker ps -a")
    print(json.dumps(output))

elif action == "launch_container":
    container_name = form.getvalue("containerName")
    image_name = form.getvalue("imageName")
    if container_name and image_name:
        output = run_command(f"docker run -d --name {container_name} {image_name}")
        print(json.dumps(output))
    else:
        print(json.dumps({"status": "error", "output": "Both container name and image name are required"}))

elif action == "start_container":
    container_name = form.getvalue("containerName")
    if container_name:
        output = run_command(f"docker start {container_name}")
        print(json.dumps(output))
    else:
        print(json.dumps({"status": "error", "output": "Container name is required"}))

elif action == "stop_container":
    container_name = form.getvalue("containerName")
    if container_name:
        output = run_command(f"docker stop {container_name}")                    print(json.dumps(output))
    else:
        print(json.dumps({"status": "error", "output": "Container name is required"}))

elif action == "docker_volume":
    output = run_command("docker volume ls")
    print(json.dumps(output))

elif action == "docker_network":
    output = run_command("docker network ls")
    print(json.dumps(output))

else:
    print(json.dumps({"status": "error", "output": "Invalid action"}))
