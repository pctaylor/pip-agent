import openai
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

#  Get the API key from environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')

def query_openai(prompt):
    openai.api_key = openai_api_key
    response = openai.ChatCompletion.create(
        model="gpt-4o",  
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response['choices'][0]['message']['content']


# Get the API key from environment variables
openweather_api_key = os.getenv('OPENWEATHER_API_KEY')

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
    city = input("Enter a city name to get the weather: ")
    print(get_weather(city))