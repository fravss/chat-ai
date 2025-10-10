from flask import Blueprint, request
from contollers.chat_controller import chat_controller

chat_bp = Blueprint('chat', __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    data = request.get_json()
    return chat_controller(data)
