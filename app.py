from flask import Flask, request, render_template, jsonify
from agent import query_openai, get_weather
from utils.markdown_utils import clean_markdown
import logging

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.logger.setLevel(logging.DEBUG)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/', methods=['GET'])
def index():
    app.logger.info("Accessing index page")
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_agent():
    app.logger.info("Received POST request to /ask")
    data = request.json
    prompt = data.get("prompt")
    app.logger.info(f"Received prompt: {prompt}")

    # Simple command parsing to check for weather queries
    if "weather in" in prompt.lower():
        city_name = prompt.split("in", 1)[1].strip()
        response = get_weather(city_name)
    else:
        response = query_openai(prompt)
    
    # Convert the response to HTML
    cleaned_html = clean_markdown(response)
    
    app.logger.info(f"Sending response: {cleaned_html[:100]}...")  # Log first 100 chars of response
    return jsonify({"response": cleaned_html})

@app.after_request
def after_request(response):
    app.logger.info(f"Sending response with status code: {response.status_code}")
    return response

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('images/favicon.ico')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
