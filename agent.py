from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import requests


# API KEYS -----------------------------------------
# Load environment variables from .env file
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)


# Get the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
openweather_api_key = os.getenv('OPENWEATHER_API_KEY')



# Instantiate the OpenAI client with the API key
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))


# Define the read_prompt_from_markdown function first
def read_prompt_from_markdown(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"An error occurred while reading the file: {str(e)}"

# Define the function to query the OpenAI API
def query_openai(prompt, system_content, previous_interaction=None):
    try:
        messages = [
            {"role": "system", "content": system_content},
        ]
        
        if previous_interaction:
            messages.extend([
                {"role": "user", "content": previous_interaction["prompt"]},
                {"role": "assistant", "content": previous_interaction["response"]}
            ])
        
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Get the weather
def get_weather(city_name):
    api_key = openweather_api_key  # Replace with your actual API key
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    # Construct the full API URL
    full_url = f"{base_url}?q={city_name}&appid={api_key}&units=metric"
    
    try:
        # Make the HTTP request to the API
        response = requests.get(full_url)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        
        # Parse the JSON response
        data = response.json()
        
        # Extract relevant information from the response
        if data["cod"] != "404":
            main = data["main"]
            weather_desc = data["weather"][0]["description"]
            temp = main["temp"]
            humidity = main["humidity"]
            city = data["name"]

            # Construct a response string
            weather_report = (
                f"Weather in {city}:\n"
                f"Temperature: {temp}°C\n"
                f"Humidity: {humidity}%\n"
                f"Description: {weather_desc.capitalize()}"
            )
        else:
            weather_report = f"City {city_name} not found."
        
    except requests.exceptions.HTTPError as http_err:
        weather_report = f"HTTP error occurred: {http_err}"
    except Exception as err:
        weather_report = f"Other error occurred: {err}"
    
    return weather_report

# Example usage
if __name__ == "__main__":
    # Instructions for creating and saving the markdown file
    print("Before running this script, please create a markdown file with your system instructions.")
    print("Recommended location: Create a 'prompts' folder in the same directory as this script.")
    print("Recommended filename: system_instructions.md")
    print("Full path example: ./prompts/system_instructions.md")
    print("Make sure to save your system instructions in this file.")
    print()

    while True:
        markdown_file = input("Enter the path to the markdown file containing the system message: ")
        if os.path.exists(markdown_file):
            break
        else:
            print(f"File not found: {markdown_file}")
            print("Please enter a valid file path.")

    system_content = read_prompt_from_markdown(markdown_file)
    print("System content loaded from:", markdown_file)
    
    initial_prompt = input("Enter your initial prompt: ")
    initial_response = query_openai(initial_prompt, system_content)
    print("Initial response:", initial_response)
    
    previous_interaction = {
        "prompt": initial_prompt,
        "response": initial_response
    }
    
    while True:
        follow_up = input("Enter a follow-up question (or 'quit' to exit): ")
        if follow_up.lower() == 'quit':
            break
        
        response = query_openai(follow_up, system_content, previous_interaction)
        print("Response:", response)
        
        previous_interaction = {
            "prompt": follow_up,
            "response": response
        }

    # Weather test
    city = input("Enter city to test weather: ")
    print(get_weather(city))