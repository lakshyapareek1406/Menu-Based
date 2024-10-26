#!/usr/bin/env python3

import os
import boto3
import cgi
import json

# Set AWS credentials as environment variables (You can also configure this using AWS CLI or IAM roles)
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# Initialize the EC2 client
ec2 = boto3.client('ec2', region_name='ap-south-1')

# Set the response header
print("Content-Type: application/json")  # Set the content type to JSON
print()  # Blank line required between headers and content

# Get form data
form = cgi.FieldStorage()
action = form.getvalue('action')

# Launch EC2 instance
def launch_instance():
    instance_type = form.getvalue('instance_type')
    ami_id = form.getvalue('ami_id')
    key_name = form.getvalue('key_name')
    security_group = form.getvalue('security_group')

    try:
        response = ec2.run_instances(
            InstanceType=instance_type,
            ImageId=ami_id,
            KeyName=key_name,
            SecurityGroupIds=[security_group],
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        return json.dumps({"message": f"Instance launched successfully! Instance ID: {instance_id}"}), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 400

# Route actions based on the request
if action == 'launch_instance':
    response, status_code = launch_instance()
else:
    response = json.dumps({"error": "Invalid action!"})
    status_code = 400

# Print the response
print(f"Status: {status_code}")
print(response)