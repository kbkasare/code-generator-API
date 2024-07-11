from flask import Flask, request, jsonify, render_template
from openai_util import generate_chat_response
import subprocess
import tempfile
import os
import openai
import re

# Define a regex pattern to extract code blocks from the OpenAI response
pattern = r'```(?:\w+)?\n([\s\S]*?)\n```'

# Initialize the Flask application
app = Flask(__name__)

# Define the root route to render the index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Define a route to execute the provided Python code
@app.route('/api/execute', methods=['POST'])
def execute_code():
    data = request.json
    code = data.get('code')
    
    # Create a temporary file with the provided code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name
    
    try:
        # Run the Python code in the temporary file and capture the output
        result = subprocess.run(
            ['python3', temp_file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,  # Set a timeout to prevent long-running processes
            check=True  # Raise an error if the command exits with a non-zero status
        )
        print(result.stdout.decode('utf-8'))
        return jsonify(output=result.stdout.decode('utf-8'))
    
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode('utf-8'))
        return jsonify(error=e.stderr.decode('utf-8')), 400
    
    except subprocess.TimeoutExpired:
        return jsonify(error="Code execution timed out"), 400
    
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


        

# Define a route to generate a response using the OpenAI API
@app.route('/api/generate', methods=['POST', 'GET'])
def generate():
    try:
        # Parse the request JSON to get the prompt and optional parameters
        data = request.json
        prompt = data.get('prompt')
        temperature = data.get('temperature', 0.7)
        max_tokens = data.get('max_tokens', 150)
        top_p = data.get('top_p', 1.0)
        frequency_penalty = data.get('frequency_penalty', 0.0)
        presence_penalty = data.get('presence_penalty', 0.0)

        # Generate the chat response using the OpenAI API
        response = generate_chat_response(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty
        )

        # Extract the code block from the response using the regex pattern
        match = re.search(pattern, response)
        if match:
            response_code = match.group(1)
        else:
            response_code = 'No code generated'
        
        # Return the response code as a JSON object
        print(response_code)
        return jsonify({'response': response_code}), 200

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 400

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
