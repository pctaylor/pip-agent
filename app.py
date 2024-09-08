from flask import Flask, request, render_template, jsonify, session
from agent import query_openai, get_weather
from utils.markdown_utils import clean_markdown
import logging
import uuid
from datetime import datetime, timezone
from db_logger import DatabaseLogger
from models import Session, UserSession, UserAction, APICall, ErrorLog
from sqlalchemy import func
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
db_handler = DatabaseLogger()
logger.addHandler(db_handler)

@app.errorhandler(Exception)
def handle_exception(e):
    # Log the error and stacktrace
    app.logger.error('An error occurred: %s', str(e))
    app.logger.error(traceback.format_exc())
    return jsonify(error=str(e)), 500

@app.before_request
def before_request():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        db_session = Session()
        user_session = UserSession(
            session_id=session['session_id'],
            start_time=datetime.now(timezone.utc),
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string
        )
        db_session.add(user_session)
        db_session.commit()
        db_session.close()

@app.route('/', methods=['GET'])
def index():
    try:
        logger.info("Accessing index page", extra={'action_type': 'page_view', 'session_id': session['session_id']})
        return render_template('index.html')
    except Exception as e:
        app.logger.error('Error in index route: %s', str(e))
        app.logger.error(traceback.format_exc())
        return jsonify(error=str(e)), 500

@app.route('/ask', methods=['POST'])
def ask_agent():
    start_time = datetime.now(timezone.utc)
    data = request.json
    prompt = data.get("prompt")
    previous_interaction = session.get('previous_interaction')
    
    try:
        if "weather in" in prompt.lower():
            city_name = prompt.split("in", 1)[1].strip()
            response = get_weather(city_name)
        else:
            with open('prompts/system_instructions.md', 'r') as file:
                system_content = file.read()
            response = query_openai(prompt, system_content, previous_interaction)
        
        end_time = datetime.now(timezone.utc)
        response_time = (end_time - start_time).total_seconds()
        
        # Truncate the response if it's too long for logging
        truncated_response = response[:1000] + '...' if len(response) > 500 else response
        
        logger.info(
            "User action",
            extra={
                'action_type': 'submit_prompt',
                'session_id': session['session_id'],
                'prompt': prompt,
                'response': truncated_response,
                'response_length': len(response),
                'response_time': response_time
            }
        )
        
        # Store the current interaction for the next round
        session['previous_interaction'] = {
            "prompt": prompt,
            "response": response
        }
        
        cleaned_html = clean_markdown(response)
        return jsonify({"response": cleaned_html})
    except Exception as e:
        logger.error(
            f"Error processing prompt: {str(e)}",
            exc_info=True,
            extra={
                'session_id': session['session_id'],
                'prompt': prompt,
                'error_type': type(e).__name__
            }
        )
        return jsonify({"error": "An error occurred processing your request"}), 500

@app.route('/admin/logs')
def view_logs():
    db_session = Session()
    user_actions = db_session.query(UserAction).order_by(UserAction.timestamp.desc()).limit(100).all()
    api_calls = db_session.query(APICall).order_by(APICall.timestamp.desc()).limit(100).all()
    errors = db_session.query(ErrorLog).order_by(ErrorLog.timestamp.desc()).limit(100).all()
    db_session.close()
    return render_template('logs.html', user_actions=user_actions, api_calls=api_calls, errors=errors)

@app.route('/admin/stats')
def view_stats():
    db_session = Session()
    total_prompts = db_session.query(UserAction).count()
    avg_prompt_length = db_session.query(func.avg(UserAction.prompt_length)).scalar()
    avg_response_time = db_session.query(func.avg(UserAction.response_time)).scalar()
    db_session.close()
    return render_template('stats.html', total_prompts=total_prompts, avg_prompt_length=avg_prompt_length, avg_response_time=avg_response_time)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
