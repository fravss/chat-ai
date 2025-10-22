from getpass import getpass
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
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
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    TextLoader,
)

load_dotenv()


if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")


uri = "mongodb+srv://anaflaviamartins56:123@chat-ai.x3m3goj.mongodb.net/?retryWrites=true&w=majority&appName=CHAT-AII"

client = MongoClient(uri)
try:
    client.admin.command("ping")
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
    relevance_score_fn="cosine",
)

print(
    "Pinged your deployment. You successfully connected to MongoDB!222 ", vector_store
)

llm = init_chat_model("gemini-2.5-flash", model_provider="google_genai")


loader = PyPDFLoader("/home/amartins11/chat-ai/1-s2.0-S1877050924021860-main.pdf")

docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

_ = vector_store.add_documents(documents=all_splits)
