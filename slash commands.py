import os
from pathlib import Path
from dotenv import load_dotenv
import requests
from flask import Flask, request, jsonify
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler


# Initialize Flask app and Slack app
app = Flask(__name__)
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
slack_app = App(
                token=os.environ['BOT_TOKEN'],
                signing_secret=os.environ['SIGNING_SECRET']
            )


# Route for handling slash command requests
@app.route("/slack/command", methods=["POST"])
def command():
    # Parse request body data
    data = request.form

    # Call the appropriate function based on the slash command
    if data["command"] == "/joke":
        message = get_joke()
    else:
        message = f"Invalid command: {data['command']}"

    # Return response to Slack
    return jsonify({"text": message})


# Function for getting a random joke from the icanhazdadjoke API
def get_joke():
    url = "https://icanhazdadjoke.com/"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers, timeout=5)
    joke = response.json()["joke"]
    return joke


# Initialize SlackRequestHandler to handle requests from Slack
handler = SlackRequestHandler(slack_app)

if __name__ == "__main__":
    # Start the Flask app on port 5000
    app.run(port=5000, debug=True)
