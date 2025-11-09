from flask import Blueprint, request
from contollers.chat_controller import chat_controller

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/", methods=["POST"])
def chat():
    print("route")
    data = request.get_json()
    return chat_controller(data)

@chat_bp.route("/teste", methods=["GET"])
def test(): 
    return "OLÁ"
