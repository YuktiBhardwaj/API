# Import necessary modules for handling HTTP requests and subprocesses
from flask import Flask, render_template, request
import subprocess
app = Flask(__name__)

# Replace this API key with your own. This key is used for authentication with OpenAI API.
OPENAI_API_KEY = 'API'

# Define the route for the root URL ('/'). This route handles both GET and POST requests.
@app.route('/', methods=['GET', 'POST'])
def indx():
    if request.method == 'POST':
        # If the request method is POST, retrieve user input from the form
        user_input = request.form['user_input']
        # Call the function to get OpenAI completion/response
        response = get_openai_completion(user_input)
        # Render the HTML template with user input and OpenAI response
        return render_template('indx.html', user_input=user_input, response=response)
    # If the request method is GET, render the HTML template without user input or response
    return render_template('indx.html')

# Function to get completion/response from OpenAI API
def get_openai_completion(input_text):
    # Construct a JSON string representing the request payload for the OpenAI API
    json_string = f'''{{
        "model": "gpt-3.5-turbo",
        "messages": [{{"role": "user", "content": "{input_text}"}}],
        "temperature": 0.7
    }}'''

    # Run the curl command to send a POST request to OpenAI API and capture the output
    result = subprocess.run(['curl', 'https://api.openai.com/v1/chat/completions',
                            '-H', 'Content-Type: application/json',
                            '-H', f'Authorization: Bearer {OPENAI_API_KEY}',
                            '-d', json_string], capture_output=True, text=True)

    # If the curl command executed successfully, return the stdout (response from OpenAI)
    if result.returncode == 0:
        return result.stdout
    # If there was an error in executing the curl command, return an error message
    else:
        return "Error: Failed to get response from OpenAI."

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)
