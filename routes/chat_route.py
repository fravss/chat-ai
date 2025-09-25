from flask import request, jsonify
from contollers.chat_controller import chat_controller
from main import app

@app.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    return chat_controller(data)
