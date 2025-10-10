from flask import Flask
from dotenv import load_dotenv
from routes.chat_route import chat_bp
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

app = Flask(__name__)

uri = "mongodb+srv://anaflaviamartins56:123@chat-ai.x3m3goj.mongodb.net/?retryWrites=true&w=majority&appName=CHAT-AII"

client = MongoClient(uri, server_api=ServerApi('1'))
CORS(app)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app.register_blueprint(chat_bp)

if __name__ == "__main__":
    app.run(debug=True)
