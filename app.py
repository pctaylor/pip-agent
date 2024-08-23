from flask import Flask, render_template, request, jsonify
from agent import query_openai, get_weather

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_agent():
    data = request.json
    prompt = data.get("prompt")

    # Simple command parsing to check for weather queries
    if "weather in" in prompt.lower():
        city_name = prompt.split("in", 1)[1].strip()
        response = get_weather(city_name)
    else:
        response = query_openai(prompt)
    
    return jsonify({"response": response})


@app.route('/')
def index():
    return render_template('index.html')



if __name__ == "__main__":
    app.run(debug=True)
