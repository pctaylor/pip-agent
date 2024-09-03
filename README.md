# Pip Agent Project

## Overview
This project is designed to create a Language Learning Model (LLM)-based agent capable of interacting with tools and serving responses via a web interface. The application is hosted on a Digital Ocean droplet, utilizing Flask, Gunicorn, and Nginx.

## Objectives
- **[*TODO*] Objectives:** design the product, i.e., non-technical, objectives of this project.
- **Develop a LLM Agent:** The agent can process user input, use tools, and respond using the OpenAI API.
    - **[*TODO*] Agent Framework** use something like Langchain to introduce enhanced functionality.
    - **[*TODO*] Relevant Tools** incorporate tools that are relevant to the user's query / agent's objective.
    - **[*TODO*] Conversationality** user chat history informs agent's response.
    - **[*TODO*] Textual RAG** user chat history informs agent's response.
        - **[*TODO*] BS Content** Any text will do just to stand it up.
        - **[*TODO*] Agent-specific content** reminder to explore impact of content metadata and networked content.
- **Web Interface:** A simple HTML/CSS/JS frontend that communicates with the backend via Flask.
    - **[*TODO*] Redesign** TBD but less shit. Visually much better. Greater interactivity.
    - **[*TODO*] Human-check** don't let bots use the site
- **Hosting:** The application is deployed on a Digital Ocean droplet with proper configuration for production, including SSL via Nginx.
    - **Secret management** secrets are stored in `.env` file and ignored by git.
    - **[*TODO*] Deployment** is continuous, updating the page after each push to the main branch using Github Actions.
    - **[*TODO*] Monitoring** basic logging and monitoring.
- **Security:** Basic security measures have been implemented, including HTTPS and input validation.

## Steps Completed

### 1. Initial Setup
- **Environment:** Mac with VSCode & Cursor, GitHub account.
- **Software Installed:**
  - Python 3, html, css, js, flask, nginx, git
  - venv created to manage environment dependencies.
  - requirements.txt created to replicate environment on server.
  - Keys stored in `.env` file and ignored by git.
  

### 2. LLM-Based Agent Development
- **Project Initialization:**
  - Created a new project directory and set up a Python virtual environment.
  - Initialized a Git repository and linked it to GitHub.
- **Agent Implementation:**
  - Developed the agent using OpenAI's API in `agent.py`.
  - Integrated tool functionalities like basic calculations.
- **Flask Backend:**
  - Created a Flask app in `app.py` to serve as the backend API for the web interface.
  - Set up routes to handle user input and return responses from the agent.

### 3. Web Interface
- **HTML/CSS/JS Frontend:**
  - Created a basic HTML page in `templates/index.html` with an input field for user queries.
  - Added styling with `static/styles.css` and functionality with `static/app.js`.
- **Integration:**
  - Connected the frontend to the Flask backend, allowing user input to be processed by the agent.

### 4. Deployment on Digital Ocean
- **Droplet Creation:**
  - Created a Digital Ocean droplet running Ubuntu 22.04.
- **Server Setup:**
  - Installed necessary software: Python 3, pip, virtualenv, Git, and Nginx.
  - Cloned the GitHub repository to the server.
  - Set up a Python virtual environment on the server and installed dependencies.
- **Gunicorn Configuration:**
  - Installed Gunicorn and configured it to serve the Flask application.
  - Tested the application locally on the server.
- **Nginx Configuration:**
  - Configured Nginx to proxy requests to Gunicorn.
  - Created a new server block for the application and tested the Nginx configuration.
- **SSL Configuration:**
  - Installed Certbot and obtained an SSL certificate for the domain.
  - Configured Nginx to enforce HTTPS.

### 5. Finalization
- **Service Management:**
  - Created a systemd service for Gunicorn to manage the app's process.
  - Enabled and started the service to ensure the app starts on boot.
- **Testing and Verification:**
  - Verified the application is running correctly via the domain or IP address.
  - Confirmed SSL is working and the application is secure.

## Notes
- **Droplet Configuration:** The droplet runs Ubuntu 22.04, with Nginx as the web server and Gunicorn as the WSGI server.
- **Environment Variables:** Store sensitive information like API keys in environment variables (`.env` file recommended).
- **Logs and Monitoring:** Use `journalctl` for logs related to the Gunicorn service and consider setting up additional monitoring tools.