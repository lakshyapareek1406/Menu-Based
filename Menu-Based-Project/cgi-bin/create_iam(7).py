#!/usr/bin/python3

import boto3
import cgi
import sys
import traceback

# Print headers for the response
print("Access-Control-Allow-Origin: *")
print("Access-Control-Allow-Methods: POST, GET, OPTIONS")
print("Content-type: text/html\n")

try:
    # Read form data
    form = cgi.FieldStorage()
    name = form.getvalue("name")
    action = form.getvalue("action")

    # Debugging output for testing
    print(f"Received name: {name}<br>")
    print(f"Received action: {action}<br>")

    if not name or not action:
        print("Error: Name and action are required.<br>")
        sys.exit(1)

    # AWS credentials (ensure these are kept secure in a production environment)
    access_key = ''
    secret_key = ''

    # Initialize a session using the specified credentials
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
         region_name='ap-south-1'
    )

    iam_client = session.client('iam')

    if action == "create":
        # Create IAM user
        try:
            iam_client.create_user(UserName=name)
            print(f"IAM user '{name}' created successfully!<br>")
        except iam_client.exceptions.EntityAlreadyExistsException:
            print(f"Error: IAM user '{name}' already exists.<br>")
        except Exception as e:
            print(f"Error creating IAM user: {e}<br>")
            traceback.print_exc(file=sys.stdout)

    elif action == "delete":
        # Delete IAM user
        try:
            iam_client.delete_user(UserName=name)
            print(f"IAM user '{name}' deleted successfully!<br>")
        except iam_client.exceptions.NoSuchEntityException:
            print(f"Error: IAM user '{name}' does not exist.<br>")
        except Exception as e:
            print(f"Error deleting IAM user: {e}<br>")
            traceback.print_exc(file=sys.stdout)

    else:
        print("Error: Invalid action specified. Use 'create' or 'delete'.<br>")

except Exception as e:
    print(f"General error: {e}<br>")
    traceback.print_exc(file=sys.stdout)