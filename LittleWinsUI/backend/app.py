from flask import Flask, jsonify
from flask_cors import CORS
import json
from ai_helper import analyze_tasks

app = Flask(__name__)
CORS(app)


def load_tasks():
    with open("sample_tasks.json", "r") as file:
        return json.load(file)


@app.route("/")
def home():
    return jsonify({"message": "LittleWins AI backend is running"})


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = load_tasks()
    return jsonify(tasks)


@app.route("/analyze", methods=["GET"])
def analyze():
    tasks = load_tasks()
    result = analyze_tasks(tasks)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)