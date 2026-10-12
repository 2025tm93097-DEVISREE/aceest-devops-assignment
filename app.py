from flask import Flask, jsonify, request

app = Flask(__name__)

PROGRAMS = {
    "fat-loss": ["Full Body HIIT", "Circuit Training", "Cardio and Weights"],
    "muscle-gain": ["Push Pull Legs", "Upper Lower Split", "Full Body Strength"],
    "beginner": ["Full Body 3x per week", "Light Strength and Mobility"],
}

clients = {}

@app.get("/")
def home():
    return jsonify(application="ACEest Fitness & Gym", status="running"), 200

@app.get("/health")
def health():
    return jsonify(status="healthy"), 200

@app.get("/programs")
def get_programs():
    return jsonify(PROGRAMS), 200

@app.post("/clients")
def create_client():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify(error="Client name is required"), 400
    if name in clients:
        return jsonify(error="Client already exists"), 409
    goal = str(data.get("goal", "beginner")).strip().lower()
    if goal not in PROGRAMS:
        return jsonify(error="Invalid goal", allowed_goals=list(PROGRAMS)), 400
    clients[name] = {"name": name, "goal": goal, "program": PROGRAMS[goal][0]}
    return jsonify(clients[name]), 201

@app.get("/clients/<name>")
def get_client(name):
    client = clients.get(name)
    if not client:
        return jsonify(error="Client not found"), 404
    return jsonify(client), 200

@app.delete("/clients/<name>")
def delete_client(name):
    if name not in clients:
        return jsonify(error="Client not found"), 404
    del clients[name]
    return "", 204

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
