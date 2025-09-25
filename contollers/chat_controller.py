from flask import jsonify
from services.chat_service import chat_service


def chat_controller(data):
    message = data["message"]

    response = chat_service(message)
    return jsonify({"response": response})