from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
CORS(app)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["webhookDB"]
collection = db["events"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"error": "No data received"}), 400

    event_type = request.headers.get('X-GitHub-Event', 'unknown')
    payload = {}

    if event_type == "push":
        payload = {
            "author": data["pusher"]["name"],
            "action": "PUSH",
            "from_branch": None,
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        }

    elif event_type == "pull_request":
        action = data["action"]
        if action in ["opened", "reopened"]:
            payload = {
                "author": data["pull_request"]["user"]["login"],
                "action": "PULL_REQUEST",
                "from_branch": data["pull_request"]["head"]["ref"],
                "to_branch": data["pull_request"]["base"]["ref"],
                "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
            }

    elif event_type == "pull_request" and data["action"] == "closed" and data["pull_request"]["merged"]:
        payload = {
            "author": data["pull_request"]["user"]["login"],
            "action": "MERGE",
            "from_branch": data["pull_request"]["head"]["ref"],
            "to_branch": data["pull_request"]["base"]["ref"],
            "timestamp": datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
        }

    if payload:
        collection.insert_one(payload)
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"message": "No relevant data to store"}), 204

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("_id", -1).limit(10))
    result = []

    for e in events:
        if e["action"] == "PUSH":
            result.append(f'{e["author"]} pushed to {e["to_branch"]} on {e["timestamp"]}')
        elif e["action"] == "PULL_REQUEST":
            result.append(f'{e["author"]} submitted a pull request from {e["from_branch"]} to {e["to_branch"]} on {e["timestamp"]}')
        elif e["action"] == "MERGE":
            result.append(f'{e["author"]} merged branch {e["from_branch"]} to {e["to_branch"]} on {e["timestamp"]}')

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
