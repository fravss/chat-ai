uri = "mongodb+srv://anaflaviamartins56:123@chat-ai.x3m3goj.mongodb.net/?retryWrites=true&w=majority&appName=CHAT-AII"
from getpass import getpass

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain.chat_models import init_chat_model



import os
from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader
)


if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

client = MongoClient(uri)
try:
    client.admin.command("ping")

except Exception as e:
    print(e)

db = client["chat"]
collection = db["embedding"]


load_dotenv()

source = os.getenv("SOURCE")

loader = PyPDFLoader(source)
docs = loader.load()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

vector_store = MongoDBAtlasVectorSearch(
    embedding=embeddings,
    collection=collection,
    index_name="default",
    relevance_score_fn="cosine",
)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = text_splitter.split_documents(docs)

_ = vector_store.add_documents(documents=all_splits)






