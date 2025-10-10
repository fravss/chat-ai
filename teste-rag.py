from getpass import getpass
import os
from dotenv import load_dotenv
from langchain_google_genai import  GoogleGenerativeAIEmbeddings
from langchain import hub
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.graph import START, StateGraph
from pymongo import MongoClient
from typing_extensions import List, TypedDict
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.chat_models import init_chat_model
import bs4

load_dotenv() 


if not os.environ.get("GOOGLE_API_KEY"):
  os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


uri = "mongodb+srv://anaflaviamartins56:123@chat-ai.x3m3goj.mongodb.net/?retryWrites=true&w=majority&appName=CHAT-AII"

client = MongoClient(uri)
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["chat"]            
collection = db["embedding"]  

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=collection,     
    index_name="default",        
    relevance_score_fn="cosine"
)

print("Pinged your deployment. You successfully connected to MongoDB!222 ", vector_store)

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")



    loader = WebBaseLoader(
        web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    all_splits = text_splitter.split_documents(docs)

    _ = vector_store.add_documents(documents=all_splits)


    prompt = hub.pull("rlm/rag-prompt")

    class State(TypedDict):
        question: str
        context: List[Document]
        answer: str



    def retrieve(state: State):
        print("aqui 111111111")
        retrieved_docs = vector_store.similarity_search(state["question"])
        return {"context": retrieved_docs}


    def generate(state: State):
        print("aqui 2222222222")
        docs_content = "\n\n".join(doc.page_content for doc in state["context"])
        messages = prompt.invoke({"question": state["question"], "context": docs_content})
        response = llm.invoke(messages)
        return {"answer": response.content}


    graph_builder = StateGraph(State).add_sequence([retrieve, generate])
    graph_builder.add_edge(START, "retrieve")
    graph = graph_builder.compile()

    response = graph.invoke({"question": "What is 'Hello' in portuguese?"})
    print(response["answer"])

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}

def classify(state: State):
    if "?" in state["messages"][0].content:
        state["type"] = "knowledge"
    else:
        state["type"] = "chat"
    return state


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("classify", classify)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "classify")
graph_builder.add_edge("classify", END)

graph = graph_builder.compile()

def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [{"role": "user", "content": user_input}]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)


while True:
    try:
        user_input = input("User: ")
        stream_graph_updates(user_input)
    except:
     
        user_input = "What do you know about LangGraph?"
        print("User: " + user_input)
        stream_graph_updates(user_input)
        break