from langgraph.graph import START, StateGraph

from graphs.state import State
from services.rag_service import generate, retrieve

def getGraph():
    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()
    
    return graph