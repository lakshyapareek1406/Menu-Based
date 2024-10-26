#!/usr/bin/python3

import cgi

print("Content-Type: text/html")
print()

# Get form data
form = cgi.FieldStorage()
number1 = float(form.getvalue('number1'))
number2 = float(form.getvalue('number2'))
operation = form.getvalue('operation')

# Initialize result variable
result = None

# Perform calculation based on the selected operation
if operation == 'add':
    result = number1 + number2
elif operation == 'subtract':
    result = number1 - number2
elif operation == 'multiply':
    result = number1 * number2
elif operation == 'divide':
    if number2 != 0:
        result = number1 / number2
    else:
        result = "Error: Division by zero is not allowed."

# Display the result
print(f"<html><body>")
if isinstance(result, str):  # Check if result is an error message
    print(f"<h1>{result}</h1>")
else:
    print(f"<h1>Result: {result}</h1>")
print(f"<a href='/index.html'>Go back to menu</a>")
print(f"</body></html>")