import openai
import os
from pathlib import Path
from dotenv import load_dotenv

# Define the base directory and load the .env file
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# Set your OpenAI API key (ensure this key is kept secure)
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_chat_response(prompt, model="gpt-3.5-turbo", temperature=0.7, max_tokens=150, top_p=1.0, frequency_penalty=0.0, presence_penalty=0.0):
    """
    This function generates a chat response using the OpenAI API's ChatCompletion endpoint.

    Parameters:
    - prompt (str): The input prompt for generating the response.
    - model (str): The model to use for generating the response.
    - temperature (float): The sampling temperature to use. Higher values mean the model will take more risks.
    - max_tokens (int): The maximum number of tokens to generate in the response.
    - top_p (float): The cumulative probability for nucleus sampling.
    - frequency_penalty (float): The penalty for repeated tokens in the response.
    - presence_penalty (float): The penalty for introducing new topics.

    Returns:
    - str: The generated response from the model.
    """
    try:
        # Call the OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a coding assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            n=1  # Number of responses to generate
        )
        
        # Extract the generated message content
        generated_message = response.choices[0].message['content'].strip()
        return generated_message

    except openai.error.OpenAIError as e:
        # Handle any errors that occur during the API call
        return f"An error occurred while generating the response: {e}"
