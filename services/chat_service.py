import os
from getpass import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from graphs.build import getGraph

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass("Enter API key for Google Gemini: ")

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")

graph = getGraph()

def chat_service(message: str) -> str:
    response = graph.invoke({"question": "What is Task Decomposition?"})
    print(response["answer"])

    return response.content.strip()
