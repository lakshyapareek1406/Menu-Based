#!/usr/bin/env python3

import os
import boto3
import cgi
import json

# Set AWS credentials as environment variables (You can also configure this using AWS CLI or IAM roles)
os.environ['AWS_ACCESS_KEY_ID'] = ''
os.environ['AWS_SECRET_ACCESS_KEY'] = ''

# Initialize the S3 client
s3 = boto3.client('s3', region_name='ap-south-1')

# Set the response header
print("Content-Type: application/json")  # Set the content type to JSON
print()  # Blank line required between headers and content

# Get form data
form = cgi.FieldStorage()
action = form.getvalue('action')

# Create S3 bucket
def create_bucket():
    bucket_name = form.getvalue('bucket_name')
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            ACL='private',
            CreateBucketConfiguration={
                'LocationConstraint': 'ap-south-1'
            }
        )
        return json.dumps({"message": "Bucket created successfully!"}), 200
        except Exception as e:
        return json.dumps({"error": str(e)}), 400

# Upload file to S3 bucket
def upload_file():
    bucket_name = form.getvalue('bucket_name')
    fileitem = form['file']

    try:
        # Save the file temporarily
        file_path = "/tmp/" + fileitem.filename  # Use a temporary path
        with open(file_path, 'wb') as f:
            f.write(fileitem.file.read())

        # Upload the file
        s3.upload_file(file_path, bucket_name, fileitem.filename)
        os.remove(file_path)  # Remove the file after uploading
        return json.dumps({"message": "File uploaded successfully!"}), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 400

# List files in S3 bucket
def list_files():
    bucket_name = form.getvalue('bucket_name')

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        files = [content['Key'] for content in response.get('Contents', [])] if 'Contents' in response else []
        return json.dumps({"files": files}), 200
    except Exception as e:
        return json.dumps({"error": str(e)}), 400

# Route actions based on the request
if action == 'create_bucket':
    response, status_code = create_bucket()
elif action == 'upload_file':
    response, status_code = upload_file()
elif action == 'list_files':
    response, status_code = list_files()
else:
    response = json.dumps({"error": "Invalid action!"})
    status_code = 400

# Print the response
print(f"Status: {status_code}")
print(response)