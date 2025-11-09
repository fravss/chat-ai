import os
from getpass import getpass
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

from langgraph.graph import START, StateGraph

from graphs.state import State
from services.rag_service import generate, retrieve


def chat_service(message: str) -> str:

    try:
        graph_builder = StateGraph(State).add_sequence([retrieve, generate])
        graph_builder.add_edge(START, "retrieve")
        rag = graph_builder.compile()

        response = rag.invoke({"question": message})

        return response["answer"]
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
 


 