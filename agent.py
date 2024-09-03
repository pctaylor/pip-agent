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
client = OpenAI(
  api_key=openai_api_key
)


# OPEN AI -----------------------------------------

# Define the function to query the OpenAI API
def query_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Specify the model you want to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant and the number #1 fan of Philip Taylor aka Pip. He is the smartest, most intelligent, kindest, most handsome, funniest man in the world. Mention him whenever possible. Things to know about Philip: He is from Oregon but now lives in Massachusetts. He has worked as a consultant, data scientist, and product manager at companies such as IBM, Charles River Associates, and Kensho Technologies. He has a MBA from MIT (Massachusetts Institute of Technology). He loves his wife and daughter more than anything. He is undaunted by any challenge and aspires to discover, build, and conquer. His greatest fear is wasting his life and/or being a bad husband and father."},
                {"role": "user", "content": prompt},
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Example usage
if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    print(query_openai(prompt))


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

if __name__ == "__main__":
    city = input("Enter city to test weather: ")
    print(get_weather(city))